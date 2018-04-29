"""
Skills module.

Provides HasSkills class for things that have skills.
"""


from sw.misc import empty_skill_dict


class HasSkills():
    """ A thing that can have skills. """

    def __init__(self):
        self.base_skills = empty_skill_dict()
        self.total_skills = empty_skill_dict()

    def upgrade_skill(self, which):
        """
        Increase a skill's level by one.

        :param which: which skill to improve.
        :type which: sw.const.skill.Skill
        """
        self.base_skills[which] += 1
