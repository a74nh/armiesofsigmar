import copy
import re
from printoption import PrintOption
from unit import Unit

class Battalion(object):

    def __init__(self, unit_config):
        self.unit_config = unit_config
        self.units = []
        for c in self.unit_config["units"]:
            self.units.append(Unit(c, "unit"))

    def __str__(self):
        if self.unitsize() == 0:
            return ""

        line = [("{}({}):[".format(self.name(), self.points()))]

        unitline = []
        for unit in self.units:
            unitstr = unit.str_battalion()
            if len(unitstr) > 0:
                unitline.append(unitstr)
        line.append(", ".join(sorted(unitline, key=lambda x: re.sub('[^A-Za-z]+', '', x).lower())))
        line.append("]")
        return " ".join(line)

    def fullstr(self):
        if self.unitsize() == 0:
            return ""

        line = [("\t{} (Warscroll Battalion)".format(self.name()))]
        line.append("\t\tTotal Points: {}".format(self.points()))

        unitline = []
        for unit in self.units:
            unitstr = unit.fullstr(tabs=2)
            if len(unitstr) > 0:
                unitline.append(unitstr)
        line.append("\n".join(sorted(unitline, key=lambda x: re.sub('[^A-Za-z]+', '', x).lower())))

        line.append("")
        return "\n".join(line)

    def __repr__(self):
        return "{}:{}".format(self.name(),str(self.units))

    def __len__(self):
        return len(self.units)

    def __getitem__(self,index):
        if index < len(self.units):
            return self.units[index]
        raise IndexError("index out of range")

    def __setitem__(self,index,item):
        if index < len(self.units):
            self.units[index] = item
            return
        raise IndexError("index out of range")

    def is_type(self, unittype):
        return "battalion" == unittype

    def unitsize(self):
        size = 0
        for unit in self.units:
            size = size + unit.unitsize()
        return size

    #Points of just the battalion (no units)
    def battalion_points(self):
        return self.unit_config.get("points", 0)

    def points(self):
        if self.unitsize() == 0:
            return 0
        points = self.battalion_points()
        for unit in self.units:
            points = points + unit.points()
        return points


    def name(self):
        return self.unit_config["name"]


    def is_unique(self):
        return False
        # return self.unit_config.get("unique", False)

    def roles(self):
        return self.unit_config.get("roles", [])

    def keywords(self):
        return []
        # return self.unit_config.get("keywords", [])

    def move(self, wounds_suffered=0):
        move = self.unit_config.get("move", 0)
        if type(move) is not dict:
            return move
        if wounds_suffered > self.wounds_per_unit():
            wounds_suffered = self.wounds_per_unit()
        while wounds_suffered > 0 and move.get(wounds_suffered, None) == None:
            wounds_suffered = wounds_suffered - 1
        return "{}*".format(move.get(wounds_suffered, 0))

    def wounds_per_unit(self):
        return self.unit_config.get("wounds", 0)

    # Total number of wounds across all units
    def total_wounds(self):
        return self.wounds_per_unit() * self.unitsize()

    def wounds_str(self):
        wounds = self.wounds_per_unit()
        if self.unitsize() == 1:
            return str(wounds)
        return "{}({})".format(wounds, wounds * self.unitsize())

    def save(self):
        save = self.unit_config.get("save", 0)
        if type(save) is str and save == "-":
            return 6
        return save

    def save_str(self):
        save = self.unit_config.get("save", 0)
        if type(save) is str:
            return save
        return "{}+".format(save)

    def bravery(self):
        return self.unit_config.get("bravery", 0)

    def sum_roles(self, roles):
        for unit in self.units:
            if unit.count > 0:
                for r in unit.roles():
                    roles[r] = roles.get(r,0) + unit.count

    def is_valid(self, restrict_battalion, restrict_config, final=True, showfails=PrintOption.SILENT):

        #TODO: Currently only support 1 or 0 instances of a single battalion
        count = 0
        if self.unitsize() > 0:
            count = 1

        # Check unit meets min restriction
        if final and count < restrict_battalion["min"]:
            if showfails.value > PrintOption.SILENT.value:
                print "FAIL MIN restrict {} {} {} : {}".format(self.name(), restrict_battalion["min"], count, self)
            return False

        if self.unitsize() == 0:
            return True

        # Check unit meets max restriction
        if restrict_battalion["max"] != -1 and count >restrict_battalion["max"]:
            if showfails.value > PrintOption.SILENT.value:
                print "FAIL MAX restrict {} {} {} : {}".format(self.name(), restrict_battalion["max"], count, self)
            return False

        #Check units and count up roles
        for unit in self.units:

            #TODO: Restrict from both restrict config and unit_config !!!
            restrict_unit = unit.unit_config
            restrict_keywords = []
            if not unit.is_valid(restrict_unit, restrict_keywords, final, showfails):
                return False

        return True

