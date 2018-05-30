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

    #TODO: Needs checking and fixing
    def avg_bravery_per_unit(self):
        if self.unitsize() == 0:
            return 0
        avg_bravery = 0
        count = 0
        for unit in self.units:
            count = count + unit.unitsize()
            avg_bravery = avg_bravery + (unit.unitsize() * unit.bravery())
        if count == 0:
            return 0
        return avg_bravery / float(count)

    #TODO: Needs checking and fixing
    def avg_save_per_wound(self):
        if self.unitsize() == 0:
            return 0
        avg_save = 0
        count = 0
        for unit in self.units:
            count = count + unit.total_wounds()
            avg_save = avg_save + (unit.total_wounds() * unit.save())
        if count == 0:
            return 0
        return avg_save / float(count)


    def is_valid(self, restrict_config, final=True, showfails=PrintOption.SILENT):
        for unit in self.units:
            restrict_unit = restrict_config["units"].get(unit.name(), restrict_config["units"]["__Others"])
            restrict_keywords = restrict_config.get("keywords", [])
            if not unit.is_valid(restrict_unit, restrict_keywords, final, showfails):
                return False
        return True
