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

    def is_valid(self, restrict_config, final=True, showfails=PrintOption.SILENT):
        for unit in self.units:
            if not unit.is_valid(restrict_config, final, showfails):
                return False
        return True

