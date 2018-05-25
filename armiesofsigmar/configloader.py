import os.path
import yaml
import sys

SELF_DIR = os.path.dirname(sys.modules[__name__].__file__)

RULEBOOK_LATEST="ghb2017"
DEFAULT_ARMY_SIZE="vanguard"

def load_units(rulebook=RULEBOOK_LATEST, unitlists=["all"], recursive=False):
    ret = {"units":[], "allies":[]}
    retdict = {}
    for faction in unitlists:
        filename = os.path.join(SELF_DIR, "units", "{}_{}.yaml".format(rulebook, faction.replace(" ", "_")))
        with open(filename, 'r') as f:
            book = yaml.load(f)
            for sectionname, section in book.iteritems():
                if type(section) is str:
                    loadedsection = load_units(rulebook, [sectionname], True)
                    ret["units"] = ret["units"] + loadedsection["units"]
                else:
                    filenamew = os.path.join(SELF_DIR, "units", "warscrolls_{}.yaml".format(sectionname.replace(" ", "_")))
                    with open(filenamew, 'r') as fw:
                        fbook = yaml.load(fw)
                        fsection = fbook[sectionname]
                        for unit in section["units"]:
                            for funit in fsection:
                                if funit["name"] == unit["name"]:
                                    # print funit["name"]
                                    unit.update(funit)
                        ret["units"] = ret["units"] + section["units"]
                        if not recursive:
                            ret["allies"] = ret["allies"] + section["allies"]
                        #             print section
                        # print fsection
                        # print section
                        # for fsectionname, fsection in fbook.iteritems():
                        #     print fsection
                        #     print section
    # print ret
    return ret

def load_restictions(filename):
    with open(filename, 'r') as f:
        return yaml.load(f)

def load_rules(rulebook=RULEBOOK_LATEST, size=DEFAULT_ARMY_SIZE):
    filename = os.path.join(SELF_DIR, "rules", "{}_{}.yaml".format(rulebook, size))
    with open(filename, 'r') as f:
        return yaml.load(f)

def load_warscrolls(unitlists=["all"]):
    ret = []
    for faction in unitlists:
        filename = os.path.join(SELF_DIR, "units", "warscrolls_{}.yaml".format(faction.replace(" ", "_")))
        with open(filename, 'r') as f:
            book = yaml.load(f)
            for sectionname, section in book.iteritems():
                if type(section) is str:
                    ret = ret + load_warascolls(rulebook, [sectionname])
                else:
                    ret = ret + section
    return ret
