"""
This module defines a set of constants used for error messaging throughout the application,
particularly in the context of user model validation and constraints.

These constants are utilized in various parts of the application such as models and forms to maintain consistency in
error messaging and to facilitate easier updates to error messages if required.
"""


#: A string used to indicate an error when a user does not accept the terms and conditions.
INVALID_TERMS_ERROR = 'Our terms and condition must be accepted.'
#: A string used to convey an error when a superuser is assigned a role other than 'Admin'.
INVALID_ROLE_ERROR = 'Superusers must have the \'Admin\' role.'
