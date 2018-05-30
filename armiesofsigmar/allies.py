from units import Units
from unit import Unit
from printoption import PrintOption
import re

class Allies(Units):

    def __init__(self, units_config):
        self.units_config = units_config
        self.units = []
        for c in units_config:
            self.units.append(Unit(c, "ally"))

    def fullstr(self):
        line = []
        unitline = []
        for unit in self.units:
            unitstr = unit.fullstr(tabs=2)
            if len(unitstr) > 0:
                unitline.append(unitstr)
        if unitline:
            line.append("\tAllies")
            line.append("\t\tTotal Points: {}".format(self.points()))
            line.append("\n".join(sorted(unitline, key=lambda x: re.sub('[^A-Za-z]+', '', x).lower())))
        return "\n".join(line)

    def is_valid(self, restrict_config, final=True, showfails=PrintOption.SILENT):
        for unit in self.units:
            restrict_unit = restrict_config["allies"].get(unit.name(), restrict_config["allies"]["__Others"])
            restrict_keywords = restrict_config.get("allies_keywords", [])
            if not unit.is_valid(restrict_unit, restrict_keywords, final, showfails):
                return False
        return True

