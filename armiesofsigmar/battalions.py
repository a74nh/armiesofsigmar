from units import Units
from battalion import Battalion
from printoption import PrintOption
import re

class Battalions(Units):

    #Each "unit" in a Battalions is a Battalion

    def __init__(self, units_config):
        self.units_config = units_config
        self.units = []
        for c in units_config:
            self.units.append(Battalion(c))

    def sum_roles(self, roles):
        for unit in self.units:
            if unit.unitsize() > 0:
                unit.sum_roles(roles)

    def is_valid(self, restrict_config, final=True, showfails=PrintOption.SILENT):
        for unit in self.units:
            restrict_unit = self._restrict_unit(restrict_config, unit.name(), "battalions")
            if not unit.is_valid(restrict_unit, restrict_config, final, showfails):
                return False
        return True

    # Number of enabled battalions
    def num(self):
        x = 0
        for u in self.units:
            if u.unitsize() > 0:
                x = x + 1
        return x
