import re

class Unit(object):

    def __init__(self, unit_config):
        self.unit_config = unit_config
        self.count = 0

    def __str__(self):
        if self.count == 0:
            return ""
        if self.count > 1:
            return "{}*{}({})".format(self.count,
                                      self.name(),
                                      self.points())
        return "{}({})".format(self.name(),
                               self.points())

    def __repr__(self):
        return "{}*{}({})".format(self.count,
                                  self.name(),
                                  self.points())

    def fullstr(self):
        ret = []
        if self.count == 0:
            return ""
        ret.append("\t{} {}".format(self.unitsize(), self.name()))
        ret.append("\t\tPoints: {}".format(self.points()))
        ret.append("\t\tRoles: {}".format(", ".join(self.roles())))
        ret.append("\t\tM/W/S/B: {}/{}/{}/{}".format(self.move(), self.wounds(), self.save(), self.bravery()))
        return "\n".join(ret)

    def inc(self, num):
        self.count = self.count + num
        if self.count < 0:
            self.count = 0

    def unitsize(self):
        return self.unit_config["min"] * self.count

    def points(self):
        return self.unit_config["points"] * self.count

    def name(self):
        return self.unit_config["name"]

    def is_unique(self):
        return self.unit_config.get("unique", False)

    def roles(self):
        return self.unit_config.get("roles", [])

    def keywords(self):
        return self.unit_config.get("keywords", [])

    def move(self):
        return self.unit_config.get("move", 0)

    def wounds(self):
        return self.unit_config.get("wounds", 0) * self.count

    def save(self):
        return str(self.unit_config.get("save", 0))+"+"

    def bravery(self):
        return self.unit_config.get("bravery", 0)
