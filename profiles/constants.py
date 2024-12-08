"""
This module defines a set of constants used for error messaging throughout the application,
particularly in the context of profile model validation and constraints.

These constants are utilized in various parts of the application such as models and forms to maintain consistency in
error messaging and to facilitate easier updates to error messages if required.
"""


#: An int used to declare the minimum user's age
MIN_AGE = 16
#: A string used to indicate an error when the user's age is determined to be under 16 years.
INVALID_BIRTHDATE_ERROR = f'Age must be at least {MIN_AGE} years'
