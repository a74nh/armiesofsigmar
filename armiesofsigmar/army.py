import re

class Army(object):

    def __init__(self, units_config):
        self.units_config = units_config
        self.units = [0] * len(self.units_config)

    def __str__(self):
        points = self.count_points()
        unitline = []
        line = [("{}: ".format(points))]
        for unitid, count in enumerate(self.units):
            if count == 0:
                continue
            if count > 1:
                unitline.append("{}*{}({})".format(count,
                                                   self.units_config[unitid]["name"],
                                                   self.units_config[unitid]["points"]))
            else:
                unitline.append("{}({})".format(self.units_config[unitid]["name"],
                                                self.units_config[unitid]["points"]))
        line.append(", ".join(sorted(unitline, key=lambda x: re.sub('[^A-Za-z]+', '', x).lower())))
        return " ".join(line)

    def __repr__(self):
        return str(self.units)

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

    def copy(self):
        ret = Army(self.units_config)
        ret.units = list(self.units)
        return ret

    def indexValid(self,index):
        return index >= 0  and index < len(self.units)

    def count_points(self):
        points = 0
        for unitid, count in enumerate(self.units):
            points = points + (count * self.units_config[unitid]["points"])
        return points

    def is_valid(self, rules_config, restrict_config, final=True, showfails=False):
        #Check points
        min_points = restrict_config.get("min_points", rules_config["points"])
        max_points = restrict_config.get("max_points", rules_config["points"])
        points = self.count_points()
        if points > max_points or ( final and points < min_points):
            if showfails:
                print "FAIL maxpoints {} {} {} : {}".format(points, min_points, max_points, self)
            return False
        
        #Create empty rules dict
        rules_check = {}
        for rulename, ruleactions in rules_config["units"].iteritems():
            rules_check[rulename] = 0

        #Check units and count up roles
        for unitid, count in enumerate(self.units):

            restrict_unit = restrict_config["units"].get(self.units_config[unitid]["name"], restrict_config["units"]["__Others"])
            # Check unit meets min restriction
            if final and count < restrict_unit["min"]:
                if showfails:
                    print "FAIL MIN restrict {} {} {} : {}".format(self.units_config[unitid]["name"], restrict_unit["min"], count, self)
                return False
            # Check unit meets max restriction
            if restrict_unit["max"] != -1 and count >restrict_unit["max"]:
                if showfails:
                    print "FAIL MAX restrict {} {} {} : {}".format(self.units_config[unitid]["name"], restrict_unit["max"], count, self)
                return False

            if count == 0:
                continue

            # Only allow 1 of each unique model
            if self.units_config[unitid].get("unique", False) and count > 1 :
                if showfails:
                    print "FAIL unique {} {} : {}".format(self.units_config[unitid]["name"], count, self)
                return False

            # Count all roles for model
            for role in self.units_config[unitid].get("roles", []):
                rules_check[role] = rules_check.get(role,0) + count

            # Check keyword match
            for restrict_keyword in restrict_config["keywords"]:
                if not restrict_keyword in self.units_config[unitid]["keywords"]:
                    if showfails:
                        print "FAIL Keyword restrict: {} {} {} : {}".format(self.units_config[unitid]["name"], self.units_config[unitid]["keywords"], restrict_keyword, self)
                    return False

        # Check roles
        for role, count in rules_check.iteritems():
            # Check role meets min requirements
            if final and count < rules_config["units"][role]["min"]:
                if showfails:
                    print "FAIL Role MIN {} {} {} : {}".format(role, rules_config["units"][role]["min"], count, self)
                return False
            # Check role meets max requirements
            if rules_config["units"][role]["max"] != -1 and count >rules_config["units"][role]["max"]:
                if showfails:
                    print "FAIL Role MAX {} {} {} : {}".format(role, rules_config["units"][role]["max"], count, self)
                return False

        return True

