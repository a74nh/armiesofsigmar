import copy
import re
from printoption import PrintOption

class Battalion(object):

    def __init__(self, unit_config, units_map):
        self.unit_config = unit_config
        self.units = []
        for unitname, unit in self.unit_config["units"].iteritems():
            self.units.append(copy.deepcopy(units_map[unitname]))

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
        line.append("\t\tPoints: {}".format(self.points()))

        unitline = []
        for unit in self.units:
            unitstr = unit.fullstr_battalion()
            if len(unitstr) > 0:
                unitline.append(unitstr)
        line.append("\n".join(sorted(unitline, key=lambda x: re.sub('[^A-Za-z]+', '', x).lower())))

        line.append("")
        return "\n".join(line)

    def __repr__(self):
        return str(self.units)

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


    def is_valid(self, rules_config, restrict_config, units_config, final=True, showfails=PrintOption.SILENT):

        if self.unitsize() == 0:
            return True

        #Find the rules for this battalion
        battalion_rules = {}
        for r in units_config["battalions"]:
            if r["name"] == self.name():
                battalion_rules = r
        if not battalion_rules:
            return False

        #Check units and count up roles
        for unit in self.units:

            rules_unit = battalion_rules["units"].get(unit.name(), None)
            if not rules_unit:
                return False

            # Check unit meets min restriction
            if final and unit.count < rules_unit["min"]:
                if showfails.value > PrintOption.SILENT.value:
                    print "FAIL MIN restrict {} {} {} : {}".format(unit.name(), rules_unit["min"], unit.count, self)
                return False
            # Check unit meets max restriction
            if rules_unit["max"] != -1 and unit.count >rules_unit["max"]:
                if showfails.value > PrintOption.SILENT.value:
                    print "FAIL MAX restrict {} {} {} : {}".format(unit.name(), rules_unit["max"], unit.count, self)
                return False

            if unit.count == 0:
                continue

        return True

