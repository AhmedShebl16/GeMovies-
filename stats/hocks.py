from rest_framework.request import Request


def postprocessing_exclude_stats_path(result: dict, generator, request: Request, public: bool) -> dict:
    """
    Modifies the API documentation to exclude certain paths and schemas for non-staff users.

    This function checks if the user making the request is a staff member. If not, it filters out
    API paths that start with '/api/stats/' and schema definitions that end with 'Stats' from the
    API documentation.

    Args:
        - result (dict): The original API documentation data.
        - generator: The generator used to create the API documentation. The type is not specified,
          as it depends on the implementation of the API documentation generator.
        - request (Request): The request object. The type is not specified, as it depends on the framework
          handling the request (e.g., Django, Flask).
        - public (bool): Indicates whether the documentation is being accessed in a public or
          private context. Not used in the current implementation.

    Returns:
        - dict: The modified API documentation data, with certain paths and schemas excluded for non-staff users.

    Note:
        This function assumes the presence of 'paths' and 'components.schemas' keys in the 'result' dictionary, and
        that the request object has a 'user' attribute with 'is_superuser' and 'is_staff' properties.
    """
    # It fixes the issues when using the command line
    if request is None:
        return result

    is_staff_user = lambda user: user.is_superuser or user.is_staff
    if not is_staff_user(request.user):
        # Exclude paths starting with /api/stats/ for non-staff users
        result['paths'] = {path: value for path, value in result['paths'].items() if not path.startswith('/api/stats/')}
        # Exclude schema definitions ending with 'Stats' for non-staff users
        result['components']['schemas'] = {schema: value for schema, value in result['components']['schemas'].items()
                                           if not schema.endswith('Stats')}
    return result
