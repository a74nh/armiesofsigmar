import re
from unit import Unit
from printoption import PrintOption

class Army(object):

    def __init__(self, units_config):
        self.units_config = units_config
        self.units = []
        for c in units_config:
            self.units.append(Unit(c))

    def __str__(self):
        unitline = []
        line = [("{}: ".format(self.points()))]
        for unit in self.units:
            unitstr = str(unit)
            if len(unitstr) > 0:
                unitline.append(str(unit))
        line.append(", ".join(sorted(unitline, key=lambda x: re.sub('[^A-Za-z]+', '', x).lower())))
        return " ".join(line)

    def __repr__(self):
        return str(self.units)

    def fullstr(self):
        unitline = []
        line = [("Points {}".format(self.points()))]
        line.append("Wounds: {}, Models: {}, Bravery/Unit: {:.2f}, Save/Wound: {:.2f}+".format(
                                self.wounds(),
                                self.unitsize(),
                                self.avg_bravery_per_unit(),
                                self.avg_save_per_wound()))
        for unit in self.units:
            unitstr = unit.fullstr()
            if len(unitstr) > 0:
                unitline.append(unitstr)
        line.append("\n".join(sorted(unitline, key=lambda x: re.sub('[^A-Za-z]+', '', x).lower())))
        line.append("")
        return "\n".join(line)

    def __getitem__(self,index):
        if self.indexValid(index):
            return self.units[index]
        else:
            raise IndexError("index out of range")

    def __setitem__(self,index,item):
        if self.indexValid(index):
            self.units[index] = item
        else:
            raise IndexError("index out of range")

    def indexValid(self,index):
        return index >= 0  and index < len(self.units)

    def points(self):
        points = 0
        for unit in self.units:
            points = points + unit.points()
        return points

    def unitsize(self):
        size = 0
        for unit in self.units:
            size = size + unit.unitsize()
        return size

    def wounds(self):
        wounds = 0
        for unit in self.units:
            wounds = wounds + unit.total_wounds()
        return wounds

    def avg_bravery_per_unit(self):
        avg_bravery = 0
        count = 0
        for unit in self.units:
            count = count + unit.unitsize()
            avg_bravery = avg_bravery + (unit.unitsize() * unit.bravery())
        return avg_bravery / float(count)

    def avg_save_per_wound(self):
        avg_save = 0
        count = 0
        for unit in self.units:
            count = count + unit.total_wounds()
            avg_save = avg_save + (unit.total_wounds() * unit.save())
        return avg_save / float(count)


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

        #Create empty rules dict
        rules_check = {}
        for rulename, ruleactions in rules_config["units"].iteritems():
            rules_check[rulename] = 0

        #Check units and count up roles
        for unit in self.units:

            restrict_unit = restrict_config["units"].get(unit.name(), restrict_config["units"]["__Others"])
            # Check unit meets min restriction
            if final and unit.count < restrict_unit["min"]:
                if showfails.value > PrintOption.SILENT.value:
                    print "FAIL MIN restrict {} {} {} : {}".format(unit.name(), restrict_unit["min"], unit.count, self)
                return False
            # Check unit meets max restriction
            if restrict_unit["max"] != -1 and unit.count >restrict_unit["max"]:
                if showfails.value > PrintOption.SILENT.value:
                    print "FAIL MAX restrict {} {} {} : {}".format(unit.name(), restrict_unit["max"], unit.count, self)
                return False

            if unit.count == 0:
                continue

            # Only allow 1 of each unique model
            if unit.is_unique() and unit.count > 1 :
                if showfails.value > PrintOption.SILENT.value:
                    print "FAIL unique {} {} : {}".format(unit.name(), count, self)
                return False

            # Count all roles for model
            for role in unit.roles():
                rules_check[role] = rules_check.get(role,0) + unit.count

            # Check keyword match
            for restrict_keyword in restrict_config["keywords"]:
                if not restrict_keyword in unit.keywords():
                    if showfails.value > PrintOption.SILENT.value:
                        print "FAIL Keyword restrict: {} {} {} : {}".format(unit.name(), unit.keywords(), restrict_keyword, self)
                    return False

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

        return True

