from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationAdmin

from .utils import get_model_fields_names, create_html_icon_link, create_image_html
from .models import (MainInfo, FAQs, AboutUs, TermsOfService, CookiePolicy, PrivacyPolicy, ContactUs, HeaderImage,
                     TeamMember, News, Award, Partner)


class MainInfoAdmin(TranslationAdmin):
    """
    Custom admin for the MainInfo model providing a specific list display, fieldsets, and read-only fields
    configuration.
    It is used for managing main site information that usually requires translation support.
    """
    list_display = (
        'email', 'facebook_html_link', 'instagram_html_link', 'twitter_html_link', 'telegram_html_link',
        'whatsapp_html_link', 'create_at', 'update_at'
    )
    fieldsets = (
        (_('Main Info'), {'fields': ('email', 'why_us')}),
        (_('Links'), {'fields': (
            ('facebook', 'facebook_html_link'),
            ('instagram', 'instagram_html_link'),
            ('twitter', 'twitter_html_link'),
            ('telegram', 'telegram_html_link'),
            ('whatsapp', 'whatsapp_html_link'),
            ('video', )
        )}),
        (_('Important Dates'), {'fields': ('create_at', 'update_at')}),
    )
    readonly_fields = (
        'facebook_html_link', 'instagram_html_link', 'twitter_html_link', 'telegram_html_link', 'whatsapp_html_link',
        'create_at', 'update_at'
    )

    def has_delete_permission(self, request, obj=None):
        """
        Determine if the delete operation is allowed for the model instances.

        Args:
            - request: HttpRequest object.
            - obj: The model instance being processed.

        Returns:
            - bool: False indicating deletion is not allowed.
        """
        return False  # deny user from deleting the instance

    def has_add_permission(self, request):
        """
        Determine if adding new model instances is allowed.

        Args:
            - request: HttpRequest object.

        Returns:
            - bool: False if a model instance already exists, otherwise defer to superclass.
        """
        if self.model.objects.count() >= 1:
            return False  # Limit main info to only one instance
        return super().has_add_permission(request)

    def facebook_html_link(self, obj=None):
        """
        Retrieve or generate the HTML link for the owner company's Facebook profile.

        This method is designed to be used within the MainInfo model's admin class, where each MainInfo instance
        represents the owner company's details. It utilizes a utility function 'create_html_icon_link' to generate an
        HTML string that represents an icon link to the company's Facebook profile. If the MainInfo instance is None or
        doesn't have a Facebook attribute, it returns an empty string.

        Args:
            - obj: The MainInfo instance (optional) for which the Facebook HTML link is being generated. This instance
              is expected to have a 'facebook' attribute storing the URL.

        Returns:
            - str: HTML string representing an icon link to the Facebook profile, or an empty string if no URL is
              provided or the instance is None.
        """
        if obj is None:
            return ''
        return create_html_icon_link(getattr(obj, 'facebook', None), 'facebook')
    facebook_html_link.short_description = _('Facebook Link')

    def instagram_html_link(self, obj=None):
        """
        Retrieve or generate the HTML link for the owner company's Instagram profile.
        This method is designed to be used within the MainInfo model's admin class, where each MainInfo instance
        represents the owner company's details. It utilizes a utility function 'create_html_icon_link' to generate an
        HTML string that represents an icon link to the company's Instagram profile. If the MainInfo instance is None
        or doesn't have an Instagram attribute, it returns an empty string.

        Args:
            - obj: The MainInfo instance (optional) for which the Instagram HTML link is being generated. This instance
              is expected to have an 'instagram' attribute storing the URL.

        Returns:
            - str: HTML string representing an icon link to the Instagram profile, or an empty string if no URL is
              provided or the instance is None.
        """
        if obj is None:
            return ''
        return create_html_icon_link(getattr(obj, 'instagram', None), 'instagram')
    instagram_html_link.short_description = _('Instagram Link')

    def twitter_html_link(self, obj=None):
        """
        Retrieve or generate the HTML link for the owner company's Twitter profile.
        This method is designed to be used within the MainInfo model's admin class, where each MainInfo instance
        represents the owner company's details. It utilizes a utility function 'create_html_icon_link' to generate an
        HTML string that represents an icon link to the company's Twitter profile. If the MainInfo instance is None or
        doesn't have a Twitter attribute, it returns an empty string.

        Args:
            - obj: The MainInfo instance (optional) for which the Twitter HTML link is being generated. This instance
              is expected to have a 'twitter' attribute storing the URL.

        Returns:
            - str: HTML string representing an icon link to the Twitter profile, or an empty string if no URL is
              provided or the instance is None.
        """
        if obj is None:
            return ''
        return create_html_icon_link(getattr(obj, 'twitter', None), 'twitter')
    twitter_html_link.short_description = _('Twitter Link')

    def telegram_html_link(self, obj=None):
        """
        Retrieve or generate the HTML link for the owner company's Telegram profile.
        This method is designed to be used within the MainInfo model's admin class, where each MainInfo instance
        represents the owner company's details. It utilizes a utility function 'create_html_icon_link' to generate an
        HTML string that represents an icon link to the company's Telegram profile. If the MainInfo instance is None or
        doesn't have a Telegram attribute, it returns an empty string.

        Args:
            - obj: The MainInfo instance (optional) for which the Telegram HTML link is being generated. This instance
              is expected to have a 'telegram' attribute storing the URL.

        Returns:
            - str: HTML string representing an icon link to the Telegram profile, or an empty string if no URL is
              provided or the instance is None.
       """
        if obj is None:
            return ''
        return create_html_icon_link(getattr(obj, 'telegram', None), 'telegram')
    telegram_html_link.short_description = _('Telegram Link')

    def whatsapp_html_link(self, obj=None):
        """
        Retrieve or generate the HTML link for the owner company's WhatsApp contact.
        This method is designed to be used within the MainInfo model's admin class, where each MainInfo instance
        represents the owner company's details. It utilizes a utility function 'create_html_icon_link' to generate an
        HTML string that represents an icon link to the company's WhatsApp contact. If the MainInfo instance is None or
        doesn't have a WhatsApp attribute, it returns an empty string.

        Args:
            - obj: The MainInfo instance (optional) for which the WhatsApp HTML link is being generated. This instance
              is expected to have a 'whatsapp' attribute storing the URL.

        Returns:
            - str: HTML string representing an icon link to the WhatsApp contact, or an empty string if no URL is
              provided or the instance is None.
        """
        if obj is None:
            return ''
        return create_html_icon_link(getattr(obj, 'whatsapp_link', None), 'whatsapp')
    whatsapp_html_link.short_description = _('Whatsapp Link')


class ContactUsAdmin(admin.ModelAdmin):
    """
    Custom admin for the ContactUs model, allowing management of user inquiries or contact submissions.
    It provides a specific list display and search fields configuration to easily navigate through contacts.
    """
    list_display = ('email', 'phone_number', 'subject', 'create_at', 'update_at')
    search_fields = ('email', 'subject', 'first_name', 'last_name', 'message')

    def has_delete_permission(self, request, obj=None):
        """
        Determine if the delete operation is allowed for the model instances.

        Args:
            - request: HttpRequest object.
            - obj: The model instance being processed.

        Returns:
            - bool: False indicating deletion is not allowed.
        """
        return False  # deny user from deleting the instance

    def has_add_permission(self, request):
        """
        Determine if adding new model instances is allowed.

        Args:
            - request: HttpRequest object.

        Returns:
            - bool: False indicating adding is not allowed.
        """
        return False  # deny user from adding new instance

    def get_readonly_fields(self, request, obj=None):
        """
        Retrieve a list of fields that will be displayed as read-only in the admin.
        If a ContactUs object is being viewed (i.e., obj is not None), all of its fields
        should be read-only to prevent modifications after submission.

        Args:
            - request: The HttpRequest object.
            - obj: The ContactUs instance that is being processed (if any).

        Returns:
            - Iterable(str): A list or tuple of field names that will be read-only.
        """
        # If an object exists, return all fields as read-only except 'id'
        if obj:
            return get_model_fields_names(obj, exclude=['id'])
        # Otherwise, defer to the default method to get read-only fields
        return super().get_readonly_fields(request, obj)


class TitledDescriptiveTranslationAdmin(TranslationAdmin):
    """
    Custom admin for models with title and description fields that need translation.
    It provides a list display, search functionality, and pagination for models with common fields like title,
    description, and creation/update timestamps.
    Inherits from TranslationAdmin to facilitate internationalization support for these fields.
    """
    list_display = ('title', 'description', 'create_at', 'update_at')
    search_fields = ('title', 'description')
    list_per_page = 20
    date_hierarchy = 'create_at'


class FAQsAdmin(TranslationAdmin):
    """
    Custom admin for the FAQs model, allowing management of Frequently Asked Questions.
    Inherits from TranslationAdmin to facilitate internationalization of FAQ entries.
    """
    list_display = ('quote', 'answer', 'create_at', 'update_at')
    search_fields = ('quote', 'answer')


class TeamMemberAdmin(admin.ModelAdmin):
    """
    Custom admin for the TeamMember model, allowing management of team member profiles.
    This includes personal details, roles, and other relevant information. It utilizes
    TranslationAdmin to support internationalization of text fields.
    """
    list_display = ('name', 'position', 'is_active', 'create_at', 'update_at')
    readonly_fields = ('create_at', 'update_at', 'show_image')
    list_filter = ('is_active', )
    search_fields = ('position', 'about')
    fieldsets = (
        (_('Main Info'), {'fields': ('name', 'position', 'about', 'join_date', 'is_active')}),
        (_('Image'), {'fields': ('image', 'show_image')}),
        (_('Social Links'), {'fields': ('facebook', 'twitter', 'linkedin', 'github')}),
        (_('Dates'), {'fields': ('create_at', 'update_at')}),
    )

    def show_image(self, obj):
        """
        Generate an HTML snippet to display a thumbnail of the image directly in the admin.

        This method is particularly useful for providing a quick visual reference for
        administrators managing header images.

        Args:
            - obj: The TeamMember instance being processed.

        Returns:
            - str: HTML string representing a thumbnail of the image, or an empty string if no image is associated.
        """
        if obj.image:
            return create_image_html(obj.image)
        return ''

    show_image.short_description = ''


class HeaderImageAdmin(TranslationAdmin):
    """
    Custom admin for the HeaderImage model, providing specific configurations for
    managing header images across the site, including image upload and selection.
    """
    list_display = ('title',  'is_active', 'create_at', 'update_at')
    list_filter = ('is_active', )
    readonly_fields = ('create_at', 'update_at', 'show_image')
    fieldsets = (
        ('Text', {'fields': ('title', 'description', 'alt')}),
        ('Image', {'fields': ('url', ('image', 'show_image'), 'create_at', 'update_at')}),
    )

    def show_image(self, obj):
        """
        Generate an HTML snippet to display a thumbnail of the image directly in the admin.

        This method is particularly useful for providing a quick visual reference for
        administrators managing header images.

        Args:
            - obj: The HeaderImage instance being processed.

        Returns:
            - str: HTML string representing a thumbnail of the image, or an empty string if no image is associated.
        """
        if obj.image:
            return create_image_html(obj.image)
        return ''

    show_image.short_description = ''


class NewsAdmin(TranslationAdmin):
    """
    Customizes the admin interface for the News model.

    This class configures how the News model is presented in the Django admin interface, including which fields are
    displayed in the list view, which fields are read-only, and how to filter the list of news articles. It also
    includes a custom method to display a thumbnail of the news image directly in the admin interface.
    """

    list_display = ('title',  'is_active', 'date', 'create_at', 'update_at')
    list_filter = ('is_active', )
    readonly_fields = ('create_at', 'update_at', 'show_image')
    fieldsets = (
        ('General', {'fields': ('title', 'description', 'date', 'is_active')}),
        ('Other', {'fields': ('alt', ('image', 'show_image'), 'create_at', 'update_at')}),
    )

    def show_image(self, obj):
        """
        Generate an HTML snippet to display a thumbnail of the image directly in the admin.

        This method is particularly useful for providing a quick visual reference for
        administrators managing news images.

        Args:
            - obj: The News instance being processed.

        Returns:
            - str: HTML string representing a thumbnail of the image, or an empty string if no image is associated.
        """
        if obj.image:
            return create_image_html(obj.image)
        return ''

    show_image.short_description = ''


class AwardAdmin(TranslationAdmin):
    """
    Customizes the admin interface for the Award model.

    This class is designed to enhance the administration of the Award model in Django's admin interface. It specifies
    which fields are displayed in the list view, sets filters for easier navigation, marks certain fields as read-only
    to prevent modification, and organizes fields into logical sections within the form view. Additionally, it includes
    a method to display a thumbnail of the award's image directly in the admin interface for a quick visual reference.
    """

    list_display = ('name',  'organization', 'is_active', 'create_at', 'update_at')
    list_filter = ('is_active', )
    readonly_fields = ('create_at', 'update_at', 'show_image')
    fieldsets = (
        ('General', {'fields': ('name', 'organization', 'description', 'date', 'is_active')}),
        ('Other', {'fields': (('image', 'show_image'), 'create_at', 'update_at')}),
    )

    def show_image(self, obj):
        """
        Generate an HTML snippet to display a thumbnail of the image directly in the admin.

        This method is particularly useful for providing a quick visual reference for
        administrators managing Award images.

        Args:
            - obj: The Award instance being processed.

        Returns:
            - str: HTML string representing a thumbnail of the image, or an empty string if no image is associated.
        """
        if obj.image:
            return create_image_html(obj.image)
        return ''

    show_image.short_description = ''


class PartnerAdmin(TranslationAdmin):
    """
    Customizes the admin interface for the Partner model.

    This configuration class enhances the Partner model management within the Django admin interface. It specifies
    the fields to be displayed in the list view, sets up filters to streamline the navigation of partner records,
    and identifies certain fields as read-only to preserve the integrity of the data, particularly the creation and
    update timestamps. Furthermore, the class organizes form fields into coherent sections and includes a method to
    display a thumbnail of the partner's image, offering a quick visual reference for administrators.
    """

    list_display = ('name', 'is_active', 'create_at', 'update_at')
    list_filter = ('is_active', )
    readonly_fields = ('create_at', 'update_at', 'show_image')
    fieldsets = (
        ('General', {'fields': ('name', 'description', 'is_active')}),
        ('Other', {'fields': (('image', 'show_image'), 'create_at', 'update_at')}),
    )

    def show_image(self, obj):
        """
        Generate an HTML snippet to display a thumbnail of the image directly in the admin.

        This method is particularly useful for providing a quick visual reference for
        administrators managing partner images.

        Args:
            - obj: The Partner instance being processed.

        Returns:
            - str: HTML string representing a thumbnail of the image, or an empty string if no image is associated.
        """
        if obj.image:
            return create_image_html(obj.image)
        return ''

    show_image.short_description = ''


admin.site.register(News, NewsAdmin)
admin.site.register(FAQs, FAQsAdmin)
admin.site.register(Award, AwardAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(MainInfo, MainInfoAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(HeaderImage, HeaderImageAdmin)
admin.site.register(AboutUs, TitledDescriptiveTranslationAdmin)
admin.site.register(CookiePolicy, TitledDescriptiveTranslationAdmin)
admin.site.register(PrivacyPolicy, TitledDescriptiveTranslationAdmin)
admin.site.register(TermsOfService, TitledDescriptiveTranslationAdmin)
