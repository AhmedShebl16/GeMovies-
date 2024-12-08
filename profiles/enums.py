from django.db import models
from django.utils.translation import gettext_lazy as _


class GenderChoices(models.IntegerChoices):
    """
    Enumeration for gender choices.
    """
    MALE = 1, _("Male")
    FEMALE = 2, _("Female")
    OTHER = 3, _("Other")


class InterestChoices(models.IntegerChoices):
    """
    Enumeration for various interests or focus areas individuals might identify with, particularly in the context of
    environmental or ocean-related activism.
    """
    OCEAN_LOVER = 1, _('Ocean Lover')
    ENVIRONMENT_ACTIVIST = 2, _('Environmental Activist')
    CONSERVATIONIST = 3, _('Conservationist')
    EDUCATOR = 4, _('Educator')
    RESEARCHER = 5, _('Researcher')
    COMMUNITY_ENGAGER = 6, _('Community Engager')
    ADVENTURER = 7, _('Adventurer')
    SOCIAL_RESPONSIBILITY = 8, _('Social Responsibility')
    CLEAN_FUTURE = 9, _('Clean Future Advocate')
    OTHER = 10, _('Other')


class ReasonChoices(models.IntegerChoices):
    """
    Enumeration for various reasons or motivations people might have for participating in activities, particularly
    those related to environmental efforts or initiatives.
    """
    PLASTIC_CLEANUP = 1, _('Plastic Cleanup Efforts')
    KNOWLEDGE_GAIN = 2, _('Gain Knowledge about Plastic Pollution')
    SPREAD_AWARENESS = 3, _('Spread Awareness about Ocean Plastic')
    CONTRIBUTE_SOLUTION = 4, _('Contribute to a Solution')
    SUPPORT_INITIATIVE = 5, _('Support Environmental Initiatives')
    PERSONAL_GROWTH = 6, _('Personal Growth and Learning')
    COMMUNITY_INVOLVEMENT = 7, _('Community Involvement')
    PROFESSIONAL_NETWORKING = 8, _('Professional Networking')
    INSPIRE_OTHERS = 9, _('Inspire Others to Take Action')
    OTHER = 10, _('Other')
