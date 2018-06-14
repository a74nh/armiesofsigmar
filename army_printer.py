import argparse
import yaml
from armiesofsigmar import Army, load_units, load_rules

parser = argparse.ArgumentParser(description='Print Warhammer Age Of Sigmar army')
parser.add_argument('configfile', metavar='config', type=str, nargs=1, help='config file to use')
parser.add_argument('-v','--verbose', help='Print army in verbose mode', action='store_true')
args = parser.parse_args()

#Open the configfile
configlist = []
with open(args.configfile[0], 'r') as f:
  configlist = yaml.load(f)

#Get list of all possible units
units_config = load_units(unitlists=configlist.get("config", []))

#Create an empty army
army = Army(units_config)

#Add all our units to the army
for u in configlist.get("units",[]):
    army.add(u, "unit")
for u in configlist.get("allies",[]):
    army.add(u, "ally")
for u in configlist.get("battalions",[]):
    army.add(u, "battalion")

#Load the rulebook

try:
    rules_config = load_rules(configlist["rulebook"], configlist["size"])
except:
    rules_config = {}

if args.verbose:
    print army.fullstr(rules_config)
else:
    print army

# if rules_config:
#     if army.is_valid(rules_config, {}):
#         print "Army is valid"
#     else:
#         print "Army is NOT valid"
