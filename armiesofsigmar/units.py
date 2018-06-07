import copy
import re
from printoption import PrintOption
from unit import Unit

class Units(object):

    def __init__(self, units_config):
        self.units_config = units_config
        self.units = []
        for c in units_config:
            self.units.append(Unit(c, "unit"))

    def __str__(self):
        unitline = []
        for unit in self.units:
            unitstr = str(unit)
            if len(unitstr) > 0:
                unitline.append(str(unit))
        return ", ".join(sorted(unitline, key=lambda x: re.sub('[^A-Za-z]+', '', x).lower()))

    def __repr__(self):
        return str(self.units)

    def __len__(self):
        return len(self.units)

    def fullstr(self):
        unitline = []
        for unit in self.units:
            unitstr = unit.fullstr()
            if len(unitstr) > 0:
                unitline.append(unitstr)
        return "\n".join(sorted(unitline, key=lambda x: re.sub('[^A-Za-z]+', '', x).lower()))

    def __getitem__(self,index):
        if index < len(self.units):
            return self.units[index]
        raise IndexError("index out of range")

    def __setitem__(self,index,item):
        if index < len(self.units):
            self.units[index] = item
            return
        raise IndexError("index out of range")

    def add(self, name):
        for u in self.units:
            if u.name() == name:
                u.inc(1)
                return
        raise KeyError('Unknown unit: {}'.format(name))

    def unitsize(self):
        size = 0
        for unit in self.units:
            size = size + unit.unitsize()
        return size

    def points(self):
        if self.unitsize() == 0:
            return 0
        points = 0
        for unit in self.units:
            points = points + unit.points()
        return points

    def wounds(self):
        wounds = 0
        for unit in self.units:
            wounds = wounds + unit.total_wounds()
        return wounds

    def _bravery_sum(self):
        x = 0
        for u in self.units:
            x = x + (u.unitsize() * u.bravery())
        return x

    def _save_mul_wounds_sum(self):
        x = 0
        for u in self.units:
            x = x + (u.total_wounds() * u.save())
        return x

    def _restrict_unit(self, restrict_config, name, unittype):
        default = { "min": 0, "max": -1 }
        #TODO: Battalions restrict by default until better support
        if unittype == "battalions":
            default = { "min": 0, "max": 0 }
        return restrict_config[unittype].get(name, restrict_config[unittype].get("__Others", default))

    def sum_roles(self, roles):
        for unit in self.units:
            if unit.count > 0:
                for r in unit.roles():
                    roles[r] = roles.get(r,0) + unit.count

    def is_valid(self, restrict_config, final=True, showfails=PrintOption.SILENT):
        for unit in self.units:
            restrict_unit = self._restrict_unit(restrict_config, unit.name(), "units")
            restrict_keywords = restrict_config.get("keywords", [])
            if not unit.is_valid(restrict_unit, restrict_keywords, final, showfails):
                return False
        return True
