import os.path
import yaml
import sys

SELF_DIR = os.path.dirname(sys.modules[__name__].__file__)

RULEBOOK_LATEST="ghb2017"
DEFAULT_ARMY_SIZE="vanguard"

def load_units(rulebook=RULEBOOK_LATEST, unitlists=["all"]):
    ret = []
    for faction in unitlists:
        filename = os.path.join(SELF_DIR, "units", "{}_{}.yaml".format(rulebook, faction.replace(" ", "_")))
        with open(filename, 'r') as f:
            book = yaml.load(f)
            for sectionname, section in book.iteritems():
                if type(section) is str:
                    ret = ret + load_units(rulebook, [sectionname])
                else:
                    ret = ret + section
    return ret

def load_restictions(filename):
    with open(filename, 'r') as f:
        return yaml.load(f)

def load_rules(rulebook=RULEBOOK_LATEST, size=DEFAULT_ARMY_SIZE):
    filename = os.path.join(SELF_DIR, "rules", "{}_{}.yaml".format(rulebook, size))
    with open(filename, 'r') as f:
        return yaml.load(f)
