from django.forms.models import model_to_dict

from templated_mail.mail import BaseEmailMessage
from djoser.email import (ActivationEmail, ConfirmationEmail, PasswordResetEmail, PasswordChangedConfirmationEmail,
                          UsernameChangedConfirmationEmail, UsernameResetEmail)

from info.models import MainInfo


class AttachMainInfoEmailMixin:
    """
    Mixin to attach main information to the context of an email template.
    It is designed to be used with classes that generate emails and need to include a "main info" in their context.
    """
    # Class variable that holds the context name for main information
    main_info_context_name = 'main_info'

    def get_main_info_data(self):
        """
        Fetches the main information from the MainInfo model.

        Returns:
            - dict: A dictionary of the main info if it exists, otherwise an empty dictionary.
        """
        # Attempt to fetch the first instance of the MainInfo object
        main_info = MainInfo.objects.first()
        # Convert the main_info object to a dictionary if it exists, else return empty dict
        return model_to_dict(main_info) if main_info else {}

    def get_context_data(self):
        """
        Extends the base context data with the main information.

        Returns:
            - dict: The updated context dictionary with main info included.
        """
        # Call the superclass's get_context_data to get the initial context
        context = super().get_context_data()
        # Add the main_info data to the context under the specified context name
        context[self.main_info_context_name] = self.get_main_info_data()
        return context


class DeleteEmail(AttachMainInfoEmailMixin, BaseEmailMessage):
    """
    A class representing an email sent when an account is deleted.
    This class is meant to customize the deletion email process by including main information from the application
    context and utilizing the base functionalities of BaseEmailMessage.
    """
    # Class variable that holds the path to the template for the delete email
    template_name = "email/delete.html"


class CustomActivationEmail(AttachMainInfoEmailMixin, ActivationEmail):
    """
    A class representing an email sent when an account needs to be activated.
    This class is meant to customize the activation email process by including main information from the application
    context and utilizing the base functionalities of ActivationEmail.
    """


class CustomConfirmationEmail(AttachMainInfoEmailMixin, ConfirmationEmail):
    """
    A class representing an email sent when an account is successfully activated.
    This class is meant to customize the activation email process by including main information from the application
    context and utilizing the base functionalities of ConfirmationEmail.
    """


class CustomPasswordResetEmail(AttachMainInfoEmailMixin, PasswordResetEmail):
    """
    A class representing an email sent when a password needs to change.
    This class is meant to customize the activation email process by including main information from the application
    context and utilizing the base functionalities of PasswordResetEmail.
    """


class CustomPasswordChangedConfirmationEmail(AttachMainInfoEmailMixin, PasswordChangedConfirmationEmail):
    """
    A class representing an email sent when a password is successfully changed.
    This class is meant to customize the activation email process by including main information from the application
    context and utilizing the base functionalities of PasswordChangedConfirmationEmail.
    """


class CustomUsernameResetEmail(AttachMainInfoEmailMixin, UsernameResetEmail):
    """
    A class representing an email sent when an username needs to be changed.
    This class is meant to customize the activation email process by including main information from the application
    context and utilizing the base functionalities of CustomUsernameResetEmail.
    """


class CustomUsernameChangedConfirmationEmail(AttachMainInfoEmailMixin, UsernameChangedConfirmationEmail):
    """
    A class representing an email sent when an username is successfully changed.
    This class is meant to customize the activation email process by including main information from the application
    context and utilizing the base functionalities of CustomPasswordChangedConfirmationEmail.
    """
