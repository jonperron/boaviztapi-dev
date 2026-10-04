import pytest

from boaviztapi.compute.impacts_computation import (
    storage_as_a_service_impact_embedded,
)
from boaviztapi.models.services.storage import ServiceStorage

DURATION = 8760


def _storage(storage_type="SSD", storage=1000, replication=1):
    service = ServiceStorage(storage_type=storage_type)
    service.storage.set_input(storage)
    service.replication.set_input(replication)
    return service


def _embedded(service):
    value, min_value, max_value, warnings = storage_as_a_service_impact_embedded(
        "gwp", DURATION, service
    )
    return value, min_value, max_value, warnings


@pytest.mark.parametrize("storage_type", ["SSD", "HDD"])
def test_impact_is_linear_in_stored_capacity(storage_type):
    single, _, _, _ = _embedded(_storage(storage_type, storage=1000))
    double, _, _, _ = _embedded(_storage(storage_type, storage=2000))
    assert double == pytest.approx(2 * single)


@pytest.mark.parametrize("storage_type", ["SSD", "HDD"])
def test_impact_is_linear_in_replication(storage_type):
    single, _, _, _ = _embedded(_storage(storage_type, replication=1))
    triple, _, _, _ = _embedded(_storage(storage_type, replication=3))
    assert triple == pytest.approx(3 * single)


def test_per_gb_impact_is_reference_disk_impact_over_its_capacity():
    service = _storage("SSD", storage=1000)
    reference_capacity = service.reference_disk().capacity.value
    value, _, _, _ = _embedded(service)

    per_gb = _embedded(_storage("SSD", storage=1))[0]
    assert value == pytest.approx(per_gb * 1000)
    assert per_gb == pytest.approx(
        _embedded(_storage("SSD", storage=reference_capacity))[0] / reference_capacity
    )


def test_hdd_carries_flat_impact_warning():
    _, _, _, warnings = _embedded(_storage("HDD"))
    assert any("HDD impact does not vary with capacity" in w for w in warnings)


def test_ssd_has_no_flat_impact_warning():
    _, _, _, warnings = _embedded(_storage("SSD"))
    assert not any("HDD impact does not vary" in w for w in warnings)


def test_unsupported_storage_type_is_rejected():
    with pytest.raises(ValueError):
        ServiceStorage(storage_type="S3")
