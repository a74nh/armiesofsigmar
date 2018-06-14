import re
from units import Units
from allies import Allies
from battalions import Battalions
from printoption import PrintOption
import itertools

class Army(object):

    def __init__(self, units_config):
        self.units_config = units_config
        self.units = Units(units_config["units"])
        self.allies = Allies(units_config["allies"])
        self.battalions = Battalions(units_config["battalions"])
        self.all = [self.units, self.allies, self.battalions]

    def __str__(self):
        line = []
        for u in self.all:
            s = str(u)
            if s:
                line.append(s)
        return "{}: {}".format(self.points(), ", ".join(line))

    def __repr__(self):
        return str(self.units)

    def __len__(self):
        return len(self.units) + len(self.allies) + len(self.battalions)

    def fullstr(self, rules_config={}):
        points = self.points()
        if rules_config:
            line = [("Points {} [{} to {}]".format(points, rules_config["points"] - points, rules_config["points"]))]
        else:
            line = [("Points {}".format(points))]
        line.append("\tWounds: {}, Models: {}, Bravery/Unit: {:.2f}, Save/Wound: {:.2f}+".format(
                                self.wounds(),
                                self.unitsize(),
                                self.avg_bravery_per_unit(),
                                self.avg_save_per_wound()))
        for u in self.all:
            s = u.fullstr()
            if s:
                line.append(s)
        line.append("Roles: {}".format(self.sum_roles_str(rules_config)))
        line.append("")
        return "\n".join(line)

    def __getitem__(self,index):
        for u in self.all:
            if index < len(u):
                return u[index]
            index = index - len(u)
        raise IndexError("index out of range")

    def __setitem__(self,index,item):
        for u in self.all:
            if index < len(u):
                u[index] = item
                return
            index = index - len(u)
        raise IndexError("index out of range")

    def add(self, name, unittype):
        if unittype == "unit":
            self.units.add(name)
        elif unittype == "ally":
            self.allies.add(name)
        elif unittype == "battalion":
            self.battalions.add(name)
        else:
            raise KeyError('Invalid unit type')

    def points(self):
        x=0
        for u in self.all:
            x = x + u.points()
        return x

    def unitsize(self):
        x=0
        for u in self.all:
            x = x + u.unitsize()
        return x

    def wounds(self):
        x=0
        for u in self.all:
            x = x + u.wounds()
        return x

    def _bravery_sum(self):
        x = 0
        for u in self.all:
            x = x + u._bravery_sum()
        return x

    def _save_mul_wounds_sum(self):
        x = 0
        for u in self.all:
            x = x + u._save_mul_wounds_sum()
        return x

    def avg_bravery_per_unit(self):
        count = self.unitsize()
        if count == 0:
            return 0
        return self._bravery_sum() / float(count)

    def avg_save_per_wound(self):
        count = self.wounds()
        if count == 0:
            return 0
        return self._save_mul_wounds_sum() / float(count)

    def sum_roles(self, rules_config={}):
        r = {}
        for rulename, ruleactions in rules_config.get("units",{}).iteritems():
            r[rulename] = 0
        for u in self.all:
            u.sum_roles(r)
        return r

    def sum_roles_str(self, rules_config={}):
        roles = self.sum_roles(rules_config)
        line = []
        for role, count in roles.iteritems():
            rule=rules_config.get("units",{}).get(role,{})
            if rule:
                if rule["max"] == -1:
                    line.append("{} {} [{}+]".format(count, role, rule["min"]))
                else:
                    line.append("{} {} [{}->{}]".format(count, role, rule["min"], rule["max"]))
            else:
                line.append("{} {}".format(count, role))
        return ", ".join(line)

    def __check_min_max(self, constraint, current_value, default_min, default_max, restrict_config, final, showfails):
        con_min = restrict_config.get("min_"+constraint, default_min)
        con_max = restrict_config.get("max_"+constraint, default_max)

        if (current_value > con_max and con_max != -1) or ( final and current_value < con_min):
            if showfails.value > PrintOption.SILENT.value:
                print "FAIL {}: {} {}->{} : {}".format(constraint, current_value, con_min, con_max, self)
            return False
        return True

    def is_valid(self, rules_config, restrict_config={}, final=True, showfails=PrintOption.SILENT):

        if not self.__check_min_max("points", self.points(), rules_config["points"], rules_config["points"], restrict_config, final, showfails):
            return False
        if not self.__check_min_max("wounds", self.wounds(), 0, -1, restrict_config, final, showfails):
            return False
        if not self.__check_min_max("models", self.unitsize(), 0, -1, restrict_config, final, showfails):
            return False
        if not self.__check_min_max("allies", self.allies.points(), 0, rules_config["allies"], restrict_config, final, showfails):
            return False

        #Default battalions to off until better support added
        if not self.__check_min_max("battalions", self.battalions.num(), 0, 0, restrict_config, final, showfails):
            return False

        for u in self.all:
            if not u.is_valid(restrict_config, final, showfails):
                return False

        # Check roles
        rules_check = self.sum_roles(rules_config)
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

        return True

