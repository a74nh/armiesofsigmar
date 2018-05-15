import argparse
from armiesofsigmar import ArmyGenerator, load_restictions, PrintOption

parser = argparse.ArgumentParser(description='Generate valid armies for Warhammer Age Of Sigmar')
parser.add_argument('configfile', metavar='config', type=str, nargs=1, help='config file to use')
parser.add_argument('-v','--verbose', help='Print armies in verbose mode', action='store_true')
parser.add_argument('-f','--fail', help='Show all failed armies', action='store_true')
args = parser.parse_args()

showfails = PrintOption.SILENT
if args.fail:
    showfails = PrintOption.PRINT

showarmies = PrintOption.PRINT
if args.verbose:
    showarmies = PrintOption.VERBOSE

restrict_config = load_restictions(args.configfile[0])
gen = ArmyGenerator(restrict_config, printarmies=showarmies, showfails=showfails)
armies = gen.generate_army()

### Alternatively, print after generating:
# gen = ArmyGenerator(restrict_config, printarmies=showarmies, showfails=PrintOption.SILENT)
# armies = gen.generate_army()
# for army in armies:
#     if args.verbose:
#         print army.fullstr()
#     else:
#         print army