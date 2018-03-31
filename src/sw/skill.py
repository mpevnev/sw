"""
Skills module.

Provides HasSkills class for things that have skills.
"""


class HasSkills():
    """ A thing that can have skills. """

    def __init__(self):
        self.base_skills = empty_skill_dict()
        self.total_skills = empty_skill_dict()

    def update_skill_totals(self):
        """ Update total skills. """
        # TODO: cross-training
        self.total_skills = self.base_skills.copy()
