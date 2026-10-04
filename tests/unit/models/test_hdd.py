from boaviztapi import config
from boaviztapi.data.archetype import get_component_archetype
from boaviztapi.models.component import ComponentHDD


def test_hdd_default_archetype_is_hdd():
    hdd = ComponentHDD()
    expected = get_component_archetype(config.default_hdd, "hdd")
    assert hdd.archetype == expected


def test_hdd_capacity_range_comes_from_min_and_max_columns():
    hdd = ComponentHDD(archetype=get_component_archetype(config.default_hdd, "hdd"))
    assert hdd.capacity.default == 500
    assert hdd.capacity.min == 100
    assert hdd.capacity.max == 2000
