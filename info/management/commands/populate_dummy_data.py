"""
Custom Django Command for Automated Dummy Data Generation

This command ('populate_dummy_data') is an essential tool for developers and testers working with Django. It automates
the generation of dummy data across all models in a Django project. Leveraging Django's dynamic model retrieval and
the 'factory_boy' library, it creates realistic test data, enhancing the development and testing workflow. The command
provides flexibility in terms of model selection and the volume of data generation.

Key Features:
- Dynamic Model Processing: Iterates through all Django models or a user-specified subset.
- Integration with 'factory_boy': Utilizes model factories to generate context-appropriate dummy data for each model
  field.
- Customization Options: Offers parameters to include or exclude specific models and to control the number of instances
  generated.

Usage Guidelines:
Execute this command via Django's manage.py utility, optionally adding arguments to tailor its operation.

Examples:
    python manage.py populate_dummy_data
    python manage.py populate_dummy_data --quantity 20
    python manage.py populate_dummy_data --include app.ModelA app.ModelB
    python manage.py populate_dummy_data --exclude app.ModelX

Parameters:
    --quantity: (Optional) Sets the number of instances to create per model.
    --include:  (Optional) A list of models to specifically include in the data generation process.
    --exclude:  (Optional) A list of models to omit from the data generation process.

Operational Feedback:
As the command executes, it provides real-time feedback in the console. It reports the progress for each model,
including any errors encountered during instance creation.

Important Note:
This command is designed for use in non-production environments. It is ideal for setting up a comprehensive dataset for
testing and development purposes. Exercise caution to avoid accidental execution in production environments, as it can
lead to the creation of large volumes of test data in live databases.
"""
from django.apps import apps
from django.core.management.base import BaseCommand
from django.utils.module_loading import import_string


class Command(BaseCommand):
    """
    A management command for populating the database with dummy data for each model.
    It allows specifying the number of instances, and inclusion or exclusion of specific models.
    """
    help = 'Populates the database with dummy data for each model.'

    def add_arguments(self, parser):
        """
        Adds command-line arguments for the management command.

        Args:
            - parser: The parser for command-line arguments.
        """
        parser.add_argument('--quantity', type=int, help='Number of dummy instances to create for each model.')
        parser.add_argument('--include', nargs='+', help='List of models to include (e.g., app.ModelName).')
        parser.add_argument('--exclude', nargs='+', help='List of models to exclude (e.g., app.ModelName).')

    def handle(self, *args, **options):
        quantity = options['quantity']
        include_models = set(options['include']) if options['include'] else None
        exclude_models = set(options['exclude']) if options['exclude'] else None

        for model in apps.get_models():
            model_label = f'{model._meta.app_label}.{model._meta.model_name}'
            if include_models and model_label not in include_models:
                continue
            if exclude_models and model_label in exclude_models:
                continue

            model_identifier = f'{model._meta.app_label}.{model._meta.model_name}'
            factory_path = f'{model._meta.app_label}.factories.{model._meta.object_name}Factory'
            try:
                model_factory = import_string(factory_path)
                model_factory.create_batch(quantity)
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created {quantity} dummy data instances for {model_identifier}')
                )
            except ImportError:
                self.stdout.write(
                    self.style.ERROR(f"Failed to import {factory_path} for given model {model_identifier}")
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create dummy data for {model_identifier}: {e}'))
