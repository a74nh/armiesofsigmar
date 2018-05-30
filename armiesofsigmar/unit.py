import re

# A unit consists of a number of instances of a single model.

class Unit(object):

    def __init__(self, unit_config, unittype):
        # Dictionary holding all the stats for a unit
        self.unit_config = unit_config
        # The number of multiples of a minimum sized unit.
        # For example, Drayds has a minimum unit size of 10.
        # Therefore, 20 Dryads would have a count of 2.
        # Technically, you could have 18 Dryads in a unit, but
        # the cost would still be the same as 20. Therefore this
        # system disallows that.
        self.count = 0
        # Type of the unit. Main unit, ally or battalion
        self.unittype = unittype

    def __str__(self):
        if self.count == 0:
            return ""
        if self.count > 1:
            return "{} {} ({})".format(self.unitsize(),
                                      self.name(),
                                      self.points())
        return "{} ({})".format(self.name(),
                               self.points())

    def __repr__(self):
        return "{} {} ({})".format(self.unitsize(),
                                  self.name(),
                                  self.points())

    def fullstr(self):
        ret = []
        if self.count == 0:
            return ""
        ret.append("\t{} {}".format(self.unitsize(), self.name()))
        ret.append("\t\tPoints: {}".format(self.points()))
        ret.append("\t\tRoles: {}".format(", ".join(self.roles())))
        ret.append("\t\tM/W/S/B: {}/{}/{}/{}".format(self.move(),
                                                    self.wounds_str(),
                                                    self.save_str(),
                                                    self.bravery()))
        return "\n".join(ret)


    def str_battalion(self):
        if self.count == 0:
            return ""
        if self.count > 1:
            return "{}*{}".format(self.count, self.name())
        return "{}".format(self.name())

    def fullstr_battalion(self):
        ret = []
        if self.count == 0:
            return ""
        ret.append("\t\t{} {}".format(self.unitsize(), self.name()))
        if self.roles():
            ret.append("\t\t\tRoles: {}".format(", ".join(self.roles())))
        ret.append("\t\t\tM/W/S/B: {}/{}/{}/{}".format(self.move(),
                                                    self.wounds_str(),
                                                    self.save_str(),
                                                    self.bravery()))
        return "\n".join(ret)


    # Increase the multiples of minimum size in the unit
    def inc(self, num):
        self.count = self.count + num
        if self.count < 0:
            self.count = 0


    def is_type(self, unittype):
        return self.unittype == unittype

    # The number of individual figures in the unit.
    # Always a multiple of unit minimum size.
    def unitsize(self):
        return self.unit_config["min"] * self.count

    def points(self):
        # Config points are per minimum unit
        return self.unit_config["points"] * self.count

    def name(self):
        return self.unit_config["name"]

    def is_unique(self):
        return self.unit_config.get("unique", False)

    def roles(self):
        return self.unit_config.get("roles", [])

    def keywords(self):
        return self.unit_config.get("keywords", [])

    def move(self, wounds_suffered=0):
        move = self.unit_config.get("move", 0)
        if type(move) is not dict:
            return move
        if wounds_suffered > self.wounds_per_unit():
            wounds_suffered = self.wounds_per_unit()
        while wounds_suffered > 0 and move.get(wounds_suffered, None) == None:
            wounds_suffered = wounds_suffered - 1
        return "{}*".format(move.get(wounds_suffered, 0))

    def wounds_per_unit(self):
        return self.unit_config.get("wounds", 0)

    # Total number of wounds across all units
    def total_wounds(self):
        return self.wounds_per_unit() * self.unitsize()

    def wounds_str(self):
        wounds = self.wounds_per_unit()
        if self.unitsize() == 1:
            return str(wounds)
        return "{}({})".format(wounds, wounds * self.unitsize())

    def save(self):
        save = self.unit_config.get("save", 0)
        if type(save) is str and save == "-":
            return 6
        return save

    def save_str(self):
        save = self.unit_config.get("save", 0)
        if type(save) is str:
            return save
        return "{}+".format(save)

    def bravery(self):
        return self.unit_config.get("bravery", 0)
