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





