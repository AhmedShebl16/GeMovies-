from typing import List
from django.utils.safestring import mark_safe


def get_model_fields_names(instance, exclude: List[str] = None) -> List[str]:
    """
    Retrieves the field names of a given Django model instance, optionally excluding specified fields.
    This function is useful when you need a list of field names dynamically, such as when generating a list of fields
    for display in the Django admin or for other introspection purposes.

    Args:
    - instance: The model instance from which to retrieve field names.
    - exclude (List[str]): A list of field names to exclude from the returned list. Defaults to an empty list.

    Returns:
    - List[str]: A list of field names from the instance, minus any specified in 'exclude'.
    """
    # If no fields are specified for exclusion, initialize an empty list
    if exclude is None:
        exclude = []

    # Retrieve all field names from the instance's metadata and filter out any specified in 'exclude'
    return list(filter(
        lambda field_name: field_name not in exclude,  # Exclude specified field names
        map(lambda field: field.name, instance._meta.get_fields())  # Map each field object to its name
    ))


def create_html_icon_link(link: str, icon: str) -> str:
    """
    Generates an HTML string for a clickable icon link.
    This function creates an HTML anchor tag with a font-awesome icon. It's useful for generating icon links
    dynamically in Django templates or admin customization.

    Args:
    - link (str): The URL that the icon link points to.
    - icon (str): The font-awesome class suffix for the desired icon (e.g., 'facebook' for 'fab fa-facebook').

    Returns:
    - str: A safe HTML string representing an anchor tag with the specified icon.
    """
    # Generate and return safe HTML string for the icon link
    return mark_safe(f"""<a href="{link}" title="{icon} link"><i class="fab fa-{icon}"></i></a>""")


def create_image_html(image):
    """
    Generates an HTML string for displaying an image with specific styling.
    This function creates an HTML string that represents an image wrapped in an anchor tag, usually for displaying in
    Django admin or templates. It includes inline styling for size and appearance.

    Args:
    - image: The image object typically from an ImageField or similar in a Django model.

    Returns:
    - str: A safe HTML string representing an anchor tag wrapping an image tag with the specified source.
    """
    return mark_safe(
        f"""<a href='{image.url}'><img src="{image.url}" style="height:400px; width: 400px; border-radius: 50%; border: 
        6px solid gray;"></a>"""
    )
