from typing import Optional

from boaviztapi.dto import BaseDTO
from boaviztapi.dto.usage.usage import Usage, mapper_usage
from boaviztapi.models.services.storage import ServiceStorage


class StorageConfiguration(BaseDTO):
    storage_type: str = "SSD"
    capacity: Optional[float] = None
    manufacturer: Optional[str] = None
    replication: Optional[int] = None


class StorageUsage(BaseDTO):
    storage: Optional[float] = None
    hours_electrical_consumption: Optional[float] = None
    usage_location: Optional[str] = None


class StorageService(BaseDTO):
    configuration: StorageConfiguration = StorageConfiguration()
    usage: StorageUsage = StorageUsage()


def mapper_storage(storage_dto: StorageService) -> ServiceStorage:
    configuration = storage_dto.configuration
    usage = storage_dto.usage

    storage = ServiceStorage(storage_type=configuration.storage_type.upper())
    storage.usage = mapper_usage(
        Usage(
            use_time_ratio=(
                usage.hours_electrical_consumption / 24
                if usage.hours_electrical_consumption is not None
                else None
            ),
            usage_location=usage.usage_location,
        ),
        archetype=storage.usage.archetype,
    )

    if configuration.capacity is not None:
        storage.reference_capacity.set_input(configuration.capacity)
    if configuration.manufacturer is not None:
        storage.manufacturer.set_input(configuration.manufacturer)
    if configuration.replication is not None:
        storage.replication.set_input(configuration.replication)
    if usage.storage is not None:
        storage.storage.set_input(usage.storage)

    return storage
