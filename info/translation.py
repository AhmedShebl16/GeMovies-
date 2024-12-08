from modeltranslation.translator import translator, TranslationOptions

from .models import (MainInfo, FAQs, AboutUs, TermsOfService, CookiePolicy, PrivacyPolicy, HeaderImage, News, Award,
                     Partner)


class MainInfoTranslationOptions(TranslationOptions):
    """
    Specifies fields of the MainInfo model to be translated.
    """
    fields = ('why_us', )


class FAQsTranslationOptions(TranslationOptions):
    """
    Specifies fields of the FAQs model to be translated.
    """
    fields = ('quote', 'answer')


class TitledDescriptiveTranslationOptions(TranslationOptions):
    """
    Specifies fields common to models with title and description to be translated.
    This includes AboutUs, CookiePolicy, PrivacyPolicy, TermsOfService.
    """
    fields = ('title', 'description')


class HeaderImageTranslationOptions(TranslationOptions):
    """
    Specifies fields of the HeaderImage model to be translated.
    """
    fields = ('title', 'description', 'alt')


class NewsTranslationOptions(TranslationOptions):
    """
    Specifies fields of the News model to be translated.
    """
    fields = ('title', 'description', 'alt')


class AwardTranslationOptions(TranslationOptions):
    """
    Specifies fields of the Award model to be translated.
    """
    fields = ('name', 'organization', 'description')


class PartnerTranslationOptions(TranslationOptions):
    """
    Specifies fields of the Partner model to be translated.
    """
    fields = ('name', 'description')


translator.register(FAQs, FAQsTranslationOptions)
translator.register(News, NewsTranslationOptions)
translator.register(Award, AwardTranslationOptions)
translator.register(Partner, PartnerTranslationOptions)
translator.register(MainInfo, MainInfoTranslationOptions)
translator.register(HeaderImage, HeaderImageTranslationOptions)
translator.register(AboutUs, TitledDescriptiveTranslationOptions)
translator.register(CookiePolicy, TitledDescriptiveTranslationOptions)
translator.register(PrivacyPolicy, TitledDescriptiveTranslationOptions)
translator.register(TermsOfService, TitledDescriptiveTranslationOptions)
