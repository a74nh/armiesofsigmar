import argparse
from armiesofsigmar import Army, load_restictions, PrintOption, load_units
import yaml

parser = argparse.ArgumentParser(description='Print Warhammer Age Of Sigmar army')
parser.add_argument('configfile', metavar='config', type=str, nargs=1, help='config file to use')
parser.add_argument('-v','--verbose', help='Print army in verbose mode', action='store_true')
args = parser.parse_args()

showarmies = PrintOption.PRINT
if args.verbose:
    showarmies = PrintOption.VERBOSE

configlist = []
with open(args.configfile[0], 'r') as f:
  configlist = yaml.load(f)

units_config = load_units(unitlists=configlist.get("config", []))

army = Army(units_config)


for u in configlist.get("units",[]):
    army.add(u, "unit")
for u in configlist.get("allies",[]):
    army.add(u, "ally")
for u in configlist.get("battalions",[]):
    army.add(u, "battalion")

if args.verbose:
    print army.fullstr()
else:
    print army
