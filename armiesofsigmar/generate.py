from configloader import load_units, load_rules
from army import Army
import copy
from printoption import PrintOption

class ArmyGenerator(object):

    def __init__(self, restrict_config, printarmies=PrintOption.SILENT, showfails=PrintOption.SILENT):
        self.restrict_config = restrict_config
        self.units_config = load_units(restrict_config["rulebook"], restrict_config["unitlists"])
        self.rules_config = load_rules(restrict_config["rulebook"], restrict_config["size"])
        self.printarmies = printarmies
        self.showfails = showfails

    # Use the restrict config to cut down the number of units in units_config
    # Will speed up generation (due to less options to parse)
    def restrict_units(self, showfails=PrintOption.SILENT):
        #Check units
        newunits = []
        for unit in self.units_config["units"]:
            if self._check_unit_restrict(unit, showfails):
                newunits.append(unit)
        self.units_config["units"] = newunits

        # Check allies
        if self.restrict_config.get("max_allies", 0) == 0:
            self.units_config["allies"] = []
            if showfails.value > PrintOption.SILENT.value:
                print "ALLY RESTRICT allies max {}".format(self.restrict_config.get("max_allies", 0))
        else:
            newallies = []
            for unit in self.units_config["allies"]:
                if self._check_ally_restrict(unit, showfails):
                    newallies.append(unit)
            self.units_config["allies"] = newallies


    def _check_unit_restrict(self, unit, showfails):
        name = unit.get("name","")
        roles = unit.get("roles",[])
        keywords = unit.get("keywords",[])
        restrict_unit = self.restrict_config["units"].get(name, self.restrict_config["units"]["__Others"])

        # Check unit meets max restriction
        if restrict_unit["max"] == 0:
            if showfails.value > PrintOption.SILENT.value:
                print "UNIT RESTRICT MAX restrict {} {}".format(name, restrict_unit["max"])
            return False

        # Check unit meets max role restriction
        for role in roles:
            if self.rules_config["units"][role]["max"] == 0:
                if showfails.value > PrintOption.SILENT.value:
                    print "UNIT RESTRICT Role MAX {} {} {}".format(name, role, self.rules_config["units"][role]["max"])
                return False

        # Check keyword match
        for restrict_keyword in self.restrict_config["keywords"]:
            if not restrict_keyword in keywords:
                if showfails.value > PrintOption.SILENT.value:
                    print "UNIT RESTRICT Keyword restrict: {} {} {}".format(name, keywords, restrict_keyword)
                return False

        return True

    def _check_ally_restrict(self, unit, showfails):
        name = unit.get("name","")
        keywords = unit.get("keywords",[])
        # Check keyword match
        for restrict_keyword in self.restrict_config["allies_keywords"]:
            if not restrict_keyword in keywords:
                if showfails.value > PrintOption.SILENT.value:
                    print "ALLY RESTRICT Ally Keyword restrict: {} {} {}".format(name, keywords, restrict_keyword)
                return False
        return True

    def generate_army(self):
        self.finalarmies = []
        self._generate(Army(self.units_config), 0)
        return self.finalarmies

    def _generate(self, army, min_start_index):

        if not army.is_valid(self.rules_config, self.restrict_config, final=False, showfails=self.showfails):
            return

        if army.is_valid(self.rules_config, self.restrict_config, final=True, showfails=self.showfails):
            if self.printarmies == PrintOption.PRINT:
                print(army)
            if self.printarmies == PrintOption.VERBOSE:
                print(army.fullstr())
            self.finalarmies.append(copy.deepcopy(army))
            return

        for unitid in range(min_start_index, len(army)):
            army[unitid].inc(1)
            self._generate(army, unitid)
            army[unitid].inc(-1)





