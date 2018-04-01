"""
Skills module.

Provides HasSkills class for things that have skills.
"""


import sw.const.skill as skill


class HasSkills():
    """ A thing that can have skills. """

    def __init__(self):
        self.base_skills = empty_skill_dict()
        self.total_skills = empty_skill_dict()

    def upgrade_skill(self, which):
        """ Increase skill's level by one. """
        self.base_skills[which] += 1


#--------- convenience things ---------#


def empty_skill_dict():
    """ Return a dict with all skills set to zero. """
    res = {s: 0 for s in skill.Skill}
    return res
