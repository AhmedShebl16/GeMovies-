from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class MainInfo(models.Model):
    """
    Model representing main information about the owner's company or website.
    Includes various social media links, contact email, WhatsApp number, and descriptive text.
    Also tracks creation and update timestamps.
    """
    facebook = models.URLField(verbose_name=_('Facebook Link'))
    instagram = models.URLField(verbose_name=_('Instagram Link'))
    twitter = models.URLField(verbose_name=_('Twitter Link'))
    telegram = models.URLField(verbose_name=_('Telegram Link'))
    video = models.URLField(verbose_name=_('Introduction Video'), null=True)
    email = models.EmailField(verbose_name=_('Web Email'))
    whatsapp = PhoneNumberField(null=True, blank=True, verbose_name=_("Whatsapp Number"))
    why_us = models.TextField(null=True, verbose_name=_("Why do you choose us?"))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('Website Main Info')
        verbose_name_plural = _('Website Main Info')
        ordering = ('-create_at', '-update_at')

    def __str__(self):
        """
        String representation of the MainInfo model instance.

        Returns:
        - str: The email address as a string representation of the instance.
        """
        return self.email

    def whatsapp_link(self):
        """
        Generate a clickable link for the WhatsApp number using the international format.

        Returns:
        - str: A string representing the full clickable WhatsApp link.
        """
        return f"https://wa.me/{self.whatsapp}"


class FAQs(models.Model):
    """
    Model representing a Frequently Asked Question (FAQ) entry.
    Includes the question (quote), its answer, and timestamps for creation and update.
    """
    quote = models.CharField(max_length=1000, verbose_name=_("Quote"))
    answer = models.TextField(verbose_name=_("Answer"))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('Frequently Asked Question')
        verbose_name_plural = _('Frequently Asked Questions')
        ordering = ('-create_at', '-update_at')

    def __str__(self):
        """
        String representation of the FAQ model instance.

        Returns:
        - str: The quote (question part) of the FAQ as a string representation of the instance.
        """
        return self.quote


class AboutUs(models.Model):
    """
    Model representing an "About Us" section entry.
    Includes the title, description, and timestamps for creation and update.
    Typically used to provide visitors with information about the organization or website.
    """
    title = models.CharField(max_length=500, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('About us')
        verbose_name_plural = _('About us')
        ordering = ('-create_at', '-update_at')

    def __str__(self):
        """
       String representation of the AboutUs model instance.

       Returns:
       - str: The title of the About Us entry as a string representation of the instance.
       """
        return self.title


class TermsOfService(models.Model):
    """
    Model representing the Terms of Service for the site.
    Includes a title, descriptive text, and timestamps for creation and update.
    Typically used to outline the rules and guidelines for using the site's services.
    """
    title = models.CharField(max_length=500, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('Terms Of Service')
        verbose_name_plural = _('Terms Of Service')
        ordering = ('-create_at', '-update_at')

    def __str__(self):
        """
        String representation of the TermsOfService model instance.

        Returns:
        - str: The title of the TermsOfService entry as a string representation of the instance.
        """
        return self.title


class CookiePolicy(models.Model):
    """
    Model representing the Cookie Policy for the site.
    Includes a title, descriptive text, and timestamps for creation and update.
    Typically used to inform users about the use of cookies on the site.
    """
    title = models.CharField(max_length=500, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('Cookie Policy')
        verbose_name_plural = _('Cookie Policy')
        ordering = ('-create_at', '-update_at')

    def __str__(self):
        """
        String representation of the CookiePolicy model instance.

        Returns:
        - str: The title of the CookiePolicy entry as a string representation of the instance.
        """
        return self.title


class PrivacyPolicy(models.Model):
    """
    Model representing the Privacy Policy for the site.
    Includes a title, descriptive text, and timestamps for creation and update.
    Typically used to inform users about how their data is collected, used, and protected.
    """
    title = models.CharField(max_length=500, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('Privacy Policy')
        verbose_name_plural = _('Privacy Policy')
        ordering = ('-create_at', '-update_at')

    def __str__(self):
        """
        String representation of the PrivacyPolicy model instance.

        Returns:
        - str: The title of the PrivacyPolicy entry as a string representation of the instance.
        """
        return self.title


class ContactUs(models.Model):
    """
    Model representing a contact submission from a user.
    Includes fields for the user's name, contact information, subject, and message,
    along with timestamps for when the contact was created and last updated.
    """
    first_name = models.CharField(max_length=120, null=True, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=120, null=True, verbose_name=_("Last name"))
    email = models.EmailField(verbose_name=_("Email"))
    phone_number = PhoneNumberField(verbose_name=_("Phone Number"))
    subject = models.CharField(max_length=250, verbose_name=_("Subject"))
    message = models.TextField(verbose_name=_("Message"))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    def __str__(self):
        """
        String representation of the ContactUs model instance.

        Returns:
        - str: The combination of first & last names as a string representation of the instance.
        """
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = _('Contact Us')
        verbose_name_plural = _('Contact Us')
        ordering = ('-create_at', '-update_at')


class HeaderImageManager(models.Manager):
    """
    Custom manager for the HeaderImage model, providing additional methods to filter and manage header images,
    specifically focusing on active images.
    """

    def active(self):
        """
        Filter the queryset to include only active header images.

        Returns:
        - QuerySet: A queryset containing only header images that are marked as active.
        """
        # Filter and return only the images marked as 'is_active=True'
        return self.filter(is_active=True)


class HeaderImage(models.Model):
    """
    Represents a header image for a website's homepage.

    This model stores information about header images used on the homepage of a website, including the title,
    description, alternative text for accessibility, the image file itself, and its visibility status. Images can
    be linked to a URL, and the model tracks the creation and last update dates. The model includes a custom manager
    for additional functionalities.
    """
    title = models.CharField(max_length=250, null=True, verbose_name=_("Title"))
    description = models.TextField(null=True, verbose_name=_("Description"))
    alt = models.CharField(max_length=250, verbose_name=_("Alternative (Alt)"),
                           help_text=_("Text is meant to convey the “why” of the image as it relates to the content of "
                                       "a document or webpage"))
    image = models.ImageField(upload_to='home/header', verbose_name=_("Image"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"),
                                    help_text=_("Setting it to false, makes the image disappear from homepage"))
    url = models.URLField(null=True, blank=True, verbose_name=_('Link'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    objects = HeaderImageManager()

    def __str__(self):
        """
        String representation of the HeaderImage model instance.

        Returns:
            - str: The title of the header image.
        """
        return self.title

    class Meta:
        verbose_name = _('Home Page Image')
        verbose_name_plural = _('Home Page Images')
        ordering = ('-create_at', '-update_at')


class TeamMember(models.Model):
    """
    Model representing a member of the team or staff. Includes their name, position, a brief about section, image,
    social media links, join date, and active status, as well as timestamps for creation and update.
    """
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    position = models.CharField(max_length=100, verbose_name=_('Position'))
    about = models.TextField(blank=True, verbose_name=_('About'))
    image = models.ImageField(upload_to='members/', verbose_name=_('Image'))
    facebook = models.URLField(blank=True, null=True, verbose_name=_('Facebook Link'))
    twitter = models.URLField(blank=True, null=True, verbose_name=_('Twitter Link'))
    linkedin = models.URLField(blank=True, null=True, verbose_name=_('Linked Link'))
    github = models.URLField(blank=True, null=True, verbose_name=_('Github Link'))
    join_date = models.DateField(verbose_name=_('Join Date'))
    is_active = models.BooleanField(blank=True, null=True, default=True, verbose_name=_('Is Active'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    def __str__(self):
        """
        String representation of the TeamMember model instance.

        Returns:
        - str: The name of the team member as a string representation of the instance.
        """
        return self.name

    class Meta:
        verbose_name = _('Team Member')
        verbose_name_plural = _('Team Members')
        ordering = ('-create_at', '-update_at')


class News(models.Model):
    """
    Represents a news article in the system.

    This class is used to create and manage news articles within the application. Each news article includes a title,
    description, publication timestamp, alternative text for images, an associated image, and flags to indicate if the
    article is currently active. Articles are automatically timestamped upon creation and update.
    """

    title = models.CharField(max_length=250, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    date = models.DateField(verbose_name=_("Publication Date"))
    alt = models.CharField(max_length=250, verbose_name=_("Alternative (Alt)"),
                           help_text=_("Text is meant to convey the “why” of the image as it relates to the content of "
                                       "a document or webpage"))
    image = models.ImageField(upload_to='home/news', verbose_name=_("Image"))
    is_active = models.BooleanField(blank=True, null=True, default=True, verbose_name=_('Is Active'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ('-create_at', '-update_at')

    def __str__(self):
        """
        Returns the string representation of the News instance, which is its title.

        Returns:
            - str: The title of the news article.
        """
        return self.title


class Award(models.Model):
    """
    Represents an award in the database.

    This class defines the schema for an award entity, typically used to showcase recognitions or achievements on a
    website or application. An award has a name, awarding organization, description, date of the award, and an
    associated image. It also includes flags for activity status and tracks both creation and last update dates.
    The `Meta` subclass defines additional settings such as verbose names and default ordering for the model.
    """

    name = models.CharField(max_length=250, verbose_name=_("Award Name"))
    organization = models.CharField(max_length=250, verbose_name=_("Awarding Organization"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    date = models.DateField(verbose_name=_("Date"))
    image = models.ImageField(upload_to='home/awards', verbose_name=_("Image"))
    is_active = models.BooleanField(blank=True, null=True, default=True, verbose_name=_('Is Active'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _("Award")
        verbose_name_plural = _("Awards")
        ordering = ('-create_at', '-update_at')

    def __str__(self):
        """
        Returns the string representation of the Award instance, which is its name.

        Returns:
            - str: The name of the award.
        """
        return self.name


class Partner(models.Model):
    """
    Represents a partner entity in the database.

    This class is designed to manage information about partners, such as sponsors, collaborators, or any other
    entities that have a partnership with the organization. Each partner has a name, an optional description, an image,
    and an activity status. The model also includes automatic fields to track the creation and last update times of
    each partner record. The `Meta` subclass provides additional settings for the model, including verbose naming and
    default sorting behavior.
    """

    name = models.CharField(max_length=250, verbose_name=_("Partner Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    image = models.ImageField(upload_to='home/partners', verbose_name=_("Image"))
    is_active = models.BooleanField(blank=True, null=True, default=True, verbose_name=_('Is Active'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")
        ordering = ('-create_at', '-update_at')

    def __str__(self):
        """
        Returns the string representation of the Partner instance, which is its name.

        Returns:
            - str: The name of the partner.
        """
        return self.name
