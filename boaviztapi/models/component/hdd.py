from boaviztapi import config
from boaviztapi.models.boattribute import Boattribute
from boaviztapi.models.component.component import Component
from boaviztapi.data.archetype import get_component_archetype, get_arch_value


class ComponentHDD(Component):
    NAME = "HDD"

    def __init__(
        self, archetype=get_component_archetype(config.default_hdd, "hdd"), **kwargs
    ):
        super().__init__(archetype=archetype, **kwargs)

        self.capacity = Boattribute(
            unit="GB",
            default=get_arch_value(archetype, "capacity", "default"),
            min=get_arch_value(archetype, "capacity", "min"),
            max=get_arch_value(archetype, "capacity", "max"),
        )
