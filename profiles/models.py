from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils.timezone import localdate
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from accounts.enums import UserRoleChoices
from accounts.models import CustomUserManager
from .constants import MIN_AGE, INVALID_BIRTHDATE_ERROR
from .enums import GenderChoices, InterestChoices, ReasonChoices


User = get_user_model()


class CustomerUserManager(CustomUserManager):
    """
    User manager for Customer users, extending the CustomUserManager. This manager filters the user queryset to return
    only users with the role of Customer.
    """

    def get_queryset(self, *args, **kwargs):
        """
        Retrieve the queryset of users, filtering it to include only customers.

        Args:
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

        Returns:
            - QuerySet: A queryset filtered to only include users with a customer role.
        """
        # Get the initial queryset from CustomUserManager
        results = super().get_queryset(*args, **kwargs)
        # Filter the queryset to only include users with the role of Customer
        return results.filter(role=UserRoleChoices.CUSTOMER)


class CustomerUser(User):
    """
    Proxy model for User that specifically represents a Customer user. It uses the base User model but defaults to the
    Customer role and applies a custom manager to filter querysets to only include Customer users.
    """
    # Default role for this proxy model is set to Customer
    base_role = UserRoleChoices.CUSTOMER

    # Set the custom manager for CustomerUser
    objects = CustomerUserManager()

    class Meta:
        # Indicate that this is a proxy model
        proxy = True


class ProfilerQuerySet(models.QuerySet):
    """
    A custom queryset for a profile model that provides additional methods to annotate profiles with age and filter
    profiles based on age range.
    """

    def with_age(self):
        """
        Annotate the queryset with an 'age' field calculated from the date_of_birth field.

        Returns:
            - QuerySet: The annotated queryset with an additional 'age' field.
        """
        # Calculate the current date
        current_date = localdate()
        # Exclude profiles where date of birth is not specified
        return self.exclude(date_of_birth__isnull=True).annotate(
            # Annotate each profile with the calculated age
            age=models.ExpressionWrapper(
                # Calculate age as the difference in years minus 1 if birthday hasn't occurred yet this year
                current_date.year - models.F('date_of_birth__year') -
                models.Case(
                    # Check if the birthday hasn't occurred yet this year
                    models.When(
                        models.Q(date_of_birth__month__gt=current_date.month) |
                        models.Q(date_of_birth__month=current_date.month, date_of_birth__day__gt=current_date.day),
                        then=models.Value(1)
                    ),
                    default=models.Value(0),
                    output_field=models.IntegerField()
                ),
                output_field=models.IntegerField()
            )
        )

    def age_range(self, start: int, end: int):
        """
        Filter the queryset to only include profiles within a specific age range.

        Args:
            - start (int): The start of the age range.
            - end (int): The end of the age range.

        Returns:
           - QuerySet: The filtered queryset including only profiles within the specified age range.
        """
        # Filter the profiles to those within the specified age range
        return self.with_age().filter(age__gte=start, age__lte=end)


class ProfileManager(models.Manager):
    """
    Custom manager for Profile models that utilizes the ProfilerQuerySet to provide additional methods for filtering
    and retrieving profiles.
    """

    def get_queryset(self):
        """
        Override the default get_queryset to return instances of ProfilerQuerySet.

        Returns:
            - ProfilerQuerySet: The custom queryset with additional profiling methods.
        """
        # Return an instance of ProfilerQuerySet for this manager
        return ProfilerQuerySet(self.model, using=self._db)

    def active(self):
        """
        Filter the queryset to only include profiles linked to active users.

        Returns:
            - QuerySet: A queryset filtered to only include profiles of active users.
        """
        # Filter the queryset for profiles with active user accounts
        return self.get_queryset().filter(user__is_active=True)

    def age_range(self, start: int, end: int):
        """
        Filter the queryset to include only profiles within a specific age range
        using the age_range method from ProfilerQuerySet.

        Args:
            - start (int): The start of the age range.
            - end (int): The end of the age range.

        Returns:
            - QuerySet: The filtered queryset including only profiles within the specified age range.
        """
        # Filter the profiles to those within the specified age range using ProfilerQuerySet
        return self.get_queryset().age_range(start, end)


class Profile(models.Model):
    """
    Profile model to store additional information for a user. Each user has one unique profile.
    """
    user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE, related_name='profile', verbose_name=_('User'))

    # Personal Details
    gender = models.PositiveSmallIntegerField(choices=GenderChoices.choices, default=GenderChoices.MALE, null=True,
                                              blank=True, verbose_name=_('Gender'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('Date of Birth'))

    # Contact Information
    phone_number_1 = PhoneNumberField(null=True, blank=True, verbose_name=_('Phone Number 1'))
    phone_number_2 = PhoneNumberField(null=True, blank=True, verbose_name=_('Phone Number 2'))

    # Current Location
    city = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('City'))
    country = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Country'))
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Address'))

    # Interest Details
    interest = models.PositiveSmallIntegerField(choices=InterestChoices.choices, default=InterestChoices.OTHER,
                                                null=True,
                                                blank=True, verbose_name=_('Interest'))
    reason = models.PositiveSmallIntegerField(choices=ReasonChoices.choices, default=ReasonChoices.OTHER, null=True,
                                              blank=True, verbose_name=_('Reason'))

    # Manipulation Attributes
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    objects = ProfileManager()

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        ordering = ('-create_at', '-update_at')
        constraints = [
            # A CheckConstraint is defined here to enforce a minimum age requirement for the user.
            models.CheckConstraint(
                # The constraint's name dynamically includes the minimum age requirement, making it clear what this
                # constraint is enforcing.
                name=f'age_must_be_gte_{MIN_AGE}',
                # The 'check' condition uses a Q object to ensure the 'date_of_birth_year' field value is logically
                # consistent with being at least MIN_AGE years old.
                # It compares the year part of the 'date_of_birth' field to the current year minus MIN_AGE, allowing
                # users who are MIN_AGE or older.
                # The use of `localdate().year - MIN_AGE` calculates the latest possible birth year for meeting the
                # age requirement.
                # An additional condition allows for the 'date_of_birth' field to be null, providing flexibility in
                # data requirements.
                check=models.Q(date_of_birth__year__lte=localdate().year-MIN_AGE) | models.Q(date_of_birth__isnull=True),
                # The 'violation_error_message' is intended to provide a custom error message if the constraint is
                # violated.
                # This feature suggests a project-specific extension or customization, as Django's CheckConstraint
                # doesn't support it natively.
                violation_error_message=_(INVALID_BIRTHDATE_ERROR)
            )
        ]


@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, *args, **kwargs):
    """
    Signal receiver that creates a Profile for a new User instance.

    This function is triggered by Django's post_save signal each time a User instance is saved.
    It specifically checks if the User instance is newly created, matches the role of 'CUSTOMER'.
    If these conditions are met, a new Profile is created and linked to the User instance.

    Args:
        - sender (Model): The model class that sent the signal. In this case, it's the User model.
        - instance (User): The instance of the User model that was saved.
        - created (bool): A boolean flag that is True if a new record was created.
        - *args: Variable length argument list.
        - **kwargs: Arbitrary keyword arguments.
    """
    if created and instance and instance.role == UserRoleChoices.CUSTOMER:
        Profile.objects.get_or_create(user=instance)
