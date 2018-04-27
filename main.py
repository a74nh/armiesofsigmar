import sys
from armiesofsigmar import ArmyGenerator, load_restictions

if len(sys.argv) != 2:
    print "Usage: {} restriction_config.yaml".format(sys.argv[0])
    exit(2)

config = sys.argv[1]

restrict_config = load_restictions(config)

gen = ArmyGenerator(restrict_config)

armies = gen.generate_army(printarmies=True)
