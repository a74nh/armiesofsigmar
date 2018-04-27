import os.path
import yaml
from configloader import load_units, load_rules
from army import Army

class ArmyGenerator(object):

    def __init__(self, restrict_config):
        self.restrict_config = restrict_config
        self.units_config = load_units(restrict_config["rulebook"], restrict_config["unitlists"])
        self.rules_config = load_rules(restrict_config["rulebook"], restrict_config["size"])

    def generate_army(self, printarmies=False):
        self.finalarmies = []
        self._generate(Army(self.units_config), 0, printarmies)
        return self.finalarmies

    def _generate(self, army, min_start_index, printarmies=False):

        if not army.is_valid(self.rules_config, self.restrict_config, final=False, showfails=False):
            return

        if army.is_valid(self.rules_config, self.restrict_config, final=True, showfails=False):
            if printarmies:
                print(army)
            self.finalarmies.append(army.copy())
            return

        for unitid in range(min_start_index, len(self.units_config)):
            army[unitid] = army[unitid] + 1
            self._generate(army, unitid, printarmies)
            army[unitid] = army[unitid] - 1





