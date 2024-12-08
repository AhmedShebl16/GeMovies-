from typing import Any

from django.db import models


def get_choice_label_from_value(enum: models.Choices, value: Any) -> Any:
    """
    Retrieve the label corresponding to a given choice value from an enumeration.

    This function takes an enumeration, which is expected to have a 'choices' attribute that is a list of tuples, where
    each tuple consists of two elements: the choice value and its corresponding label. It returns the label for the
    given value, or None if the value is not found in the enumeration.

    Args:
        - enum (models.Choices): The enumeration containing choice values and labels.
        - value (Any): The value for which the corresponding label is desired.

    Returns:
        - Any: The label corresponding to the provided value, or None if the value is not found.
    """
    dict_enum = dict(enum.choices)
    return dict_enum.get(value, None)
