import os.path
import yaml
import sys
import itertools

SELF_DIR = os.path.dirname(sys.modules[__name__].__file__)

RULEBOOK_LATEST="ghb2017"
DEFAULT_ARMY_SIZE="vanguard"

def load_units(rulebook=RULEBOOK_LATEST, unitlists=["all"], recursive=False):
    ret = {"units":[], "allies":[], "battalions": []}
    retdict = {}
    for faction in unitlists:
        filename = os.path.join(SELF_DIR, "units", "{}_{}.yaml".format(rulebook, faction.replace(" ", "_")))
        try:
            with open(filename, 'r') as f:
                book = yaml.load(f)
                for sectionname, section in book.iteritems():
                    if type(section) is str:
                        loadedsection = load_units(rulebook, [sectionname], recursive)
                        ret["units"] = ret["units"] + loadedsection["units"]
                    else:
                        filenamew = os.path.join(SELF_DIR, "units", "warscrolls_{}.yaml".format(sectionname.replace(" ", "_")))
                        with open(filenamew, 'r') as fw:
                            fbook = yaml.load(fw)
                            for sectiontype in ["units", "battalions"]:
                                fsection = fbook[sectionname].get(sectiontype, [])
                                for unit in section.get(sectiontype, []):
                                    for funit in fsection:
                                        if funit["name"] == unit["name"]:
                                            # print funit["name"]
                                            unit.update(funit)
                                ret[sectiontype] = ret[sectiontype] + section.get(sectiontype,[])
                            if not recursive:
                                ret["allies"] = ret["allies"] + section["allies"]
        except IOError:
            pass
    if not recursive:
        ret["allies"] = load_units(rulebook, ret["allies"], True)["units"]
        for battalion in ret["battalions"]:
            new_units = []
            for name, config in battalion["units"].iteritems():
                for u in itertools.chain(ret["units"], ret["allies"]):
                    if u["name"] == name:
                        config.update(u)
                        new_units.append(config)
                        continue
            battalion["units"]=new_units
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
