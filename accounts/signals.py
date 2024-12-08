from django.dispatch import Signal

#: Signal sent when a user deactivates their account. This signal can be used to perform additional actions or cleanup
#: when a user account is deactivated.
#: It should be sent with the following arguments:
#:
#: - **User**: The user instance that is deactivating their account.
#: - **Request**: The HTTP request object that initiated the account deactivation.
user_deactivated = Signal()
