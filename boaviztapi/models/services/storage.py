from boaviztapi import config
from boaviztapi.models.boattribute import Boattribute
from boaviztapi.models.component import ComponentHDD, ComponentSSD
from boaviztapi.models.services.cloud_instance import Service
from boaviztapi.models.usage import ModelUsage
from boaviztapi.data.archetype import get_component_archetype, get_arch_component

# storage_type -> (component model, default archetype name, archetype key)
_STORAGE_TYPES = {
    "SSD": (ComponentSSD, config.default_ssd, "ssd"),
    "HDD": (ComponentHDD, config.default_hdd, "hdd"),
}


def _reference_archetype(storage_type: str) -> dict:
    _, default_name, archetype_key = _STORAGE_TYPES[storage_type]
    return get_component_archetype(default_name, archetype_key)


class ServiceStorage(Service):
    """Storage bought as a service, computed from a reference disk of the same type."""

    NAME = "STORAGE_AS_A_SERVICE"

    def __init__(self, storage_type: str = "SSD", **kwargs):
        if storage_type not in _STORAGE_TYPES:
            raise ValueError(f"Unsupported storage type: {storage_type}")
        archetype = _reference_archetype(storage_type)
        super().__init__(archetype=archetype, **kwargs)

        self.storage_type = storage_type
        self.manufacturer = Boattribute()
        self.storage = Boattribute(unit="GB")
        self.replication = Boattribute(default=1, min=1, max=1)
        self.reference_capacity = Boattribute(unit="GB")
        self.usage = ModelUsage(archetype=get_arch_component(archetype, "USAGE"))

    def reference_disk(self):
        """Disk of the same type that the per-GB impact is taken from."""
        disk_model, _, _ = _STORAGE_TYPES[self.storage_type]
        disk = disk_model(archetype=_reference_archetype(self.storage_type))
        # Fix the reference capacity: its archetype range (e.g. 100-5000 GB) would
        # otherwise widen the per-GB min/max bounds through the disk's own formula.
        if self.reference_capacity.has_value():
            disk.capacity.set_input(self.reference_capacity.value)
        else:
            disk.capacity.set_input(disk.capacity.value)
        if self.manufacturer.has_value():
            disk.manufacturer.set_input(self.manufacturer.value)
        disk.usage = self.usage
        return disk

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value
