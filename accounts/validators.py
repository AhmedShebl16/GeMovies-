from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .constants import INVALID_TERMS_ERROR


def validate_boolean_true(value: bool) -> None:
    """
    Validate whether the provided value is strictly True.

    Args:
        - value (bool): The boolean value to be validated.

    Raises:
        - ValidationError: If the value is not strictly True.

    This function is typically used to ensure that a user has accepted terms and conditions
    (or similar agreements) by checking a checkbox in a form.
    """

    # Check if the value is not strictly True
    if value is not True:
        # If the value is not True, raise a ValidationError
        raise ValidationError(
            message=_(INVALID_TERMS_ERROR),
            code='not_true'
        )
