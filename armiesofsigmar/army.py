import re
from unit import Unit
from units import Units
from allies import Allies
from battalion import Battalion
from printoption import PrintOption
import itertools

class Army(object):

    def __init__(self, units_config):
        self.units_config = units_config
        self.units = []
        self.allies = []
        self.battalions = []
        self.map = {}
        # for u in itertools.chain(units_config["units"], units_config["allies"]):
        #     self.map[u["name"]] = u
        self.units = Units(units_config["units"])
        self.allies = Allies(units_config["allies"])
        for c in units_config["battalions"]:
            self.battalions.append(Battalion(c))
        #Combination of all units and allies and battalions
        self.all = [self.units, self.allies, self.battalions]
        # print self.units
        # print self.allies
        # print self.battalions

    def __str__(self):
        unitsline = []
        for u in [str(self.units), str(self.allies)]:
            if u:
                unitsline.append(u)

        unitline = []
        for unit in self.battalions:
            unitstr = str(unit)
            if len(unitstr) > 0:
                unitline.append(unitstr)
        if unitline:
            unitsline.append(", ".join(sorted(unitline, key=lambda x: re.sub('[^A-Za-z]+', '', x).lower())))

        return "{}: {}".format(self.points(), ", ".join(unitsline))

    def __repr__(self):
        return str(self.units)

    def __len__(self):
        return len(self.units) + len(self.allies) + len(self.battalions)

    def fullstr(self):
        line = [("Points {}".format(self.points()))]
        line.append("\tWounds: {}, Models: {}, Bravery/Unit: {:.2f}, Save/Wound: {:.2f}+".format(
                                self.wounds(),
                                self.unitsize(),
                                self.avg_bravery_per_unit(),
                                self.avg_save_per_wound()))
        line.append(self.units.fullstr())
        line.append(self.allies.fullstr())

        unitline = []
        for unit in self.battalions:
            unitstr = unit.fullstr()
            if len(unitstr) > 0:
                unitline.append(unitstr)
        if unitline:
            line.append("\n".join(sorted(unitline, key=lambda x: re.sub('[^A-Za-z]+', '', x).lower())))

        line.append("")
        return "\n".join(line)

    def __getitem__(self,index):
        if index < len(self.units):
            return self.units[index]
        index = index - len(self.units)
        if index < len(self.allies):
            return self.allies[index]
        index = index - len(self.allies)
        if index < len(self.battalions):
            return self.battalions[index]
        raise IndexError("index out of range")

    def __setitem__(self,index,item):
        if index < len(self.units):
            self.units[index] = item
            return
        index = index - len(self.units)
        if index < len(self.allies):
            self.allies[index] = item
            return
        index = index - len(self.allies)
        if index < len(self.battalions):
            self.battalions[index] = item
            return
        raise IndexError("index out of range")

    def points(self):
        return self.units.points() + self.allies.points() + self.battalion_points()

    def battalion_points(self):
        points = 0
        for unit in self.battalions:
            points = points + unit.points()
        return points

    def unitsize(self):
        size = self.units.unitsize() + self.allies.unitsize()
        for unit in self.battalions:
            size = size + unit.unitsize()
        return size

    def wounds(self):
        wounds = self.units.wounds() + self.allies.wounds()
        for unit in self.battalions:
            wounds = wounds + unit.total_wounds()
        return wounds

    def avg_bravery_per_unit(self):
        #TODO: Add battalions
        return self.units.avg_bravery_per_unit() + self.allies.avg_bravery_per_unit()

    def avg_save_per_wound(self):
        #TODO: Add battalions
        return self.units.avg_save_per_wound() + self.allies.avg_save_per_wound()


    def __check_min_max(self, constraint, current_value, default_min, default_max, restrict_config, final, showfails):
        con_min = restrict_config.get("min_"+constraint, default_min)
        con_max = restrict_config.get("max_"+constraint, default_max)

        if (current_value > con_max and con_max != -1) or ( final and current_value < con_min):
            if showfails.value > PrintOption.SILENT.value:
                print "FAIL {}: {} {}->{} : {}".format(constraint, current_value, con_min, con_max, self)
            return False
        return True

    def is_valid(self, rules_config, restrict_config, final=True, showfails=PrintOption.SILENT):
        
        if not self.__check_min_max("points", self.points(), rules_config["points"], rules_config["points"], restrict_config, final, showfails):
            return False
        if not self.__check_min_max("wounds", self.wounds(), 0, -1, restrict_config, final, showfails):
            return False
        if not self.__check_min_max("models", self.unitsize(), 0, -1, restrict_config, final, showfails):
            return False
        if not self.__check_min_max("allies", self.allies.points(), 0, rules_config["allies"], restrict_config, final, showfails):
            return False


        #Create empty rules dict
        rules_check = {}
        for rulename, ruleactions in rules_config["units"].iteritems():
            rules_check[rulename] = 0

        if not self.units.is_valid(restrict_config, final, showfails):
            return False

        if not self.allies.is_valid(restrict_config, final, showfails):
            return False

        # Count all roles for models (TODO: ADD BATTALIONS!!)
        for unit in itertools.chain(self.units, self.allies):
            for role in unit.roles():
                rules_check[role] = rules_check.get(role,0) + unit.count

        # Check roles
        for role, count in rules_check.iteritems():
            # Check role meets min requirements
            if final and count < rules_config["units"][role]["min"]:
                if showfails.value > PrintOption.SILENT.value:
                    print "FAIL Role MIN {} {} {} : {}".format(role, rules_config["units"][role]["min"], count, self)
                return False
            # Check role meets max requirements
            if rules_config["units"][role]["max"] != -1 and count >rules_config["units"][role]["max"]:
                if showfails.value > PrintOption.SILENT.value:
                    print "FAIL Role MAX {} {} {} : {}".format(role, rules_config["units"][role]["max"], count, self)
                return False

        # Check battalions
        for b in self.battalions:
            if not b.is_valid(restrict_config, final, showfails):
                return False

        return True

