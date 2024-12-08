"""
Custom Django Command to Rewrite Links and Styles in Django Format

This command ('process_html') is specifically designed to parse the 'index.html' file generated
from the React build process and rewrite the links to CSS, JavaScript, and image assets to utilize
Django's static file handling system. It is an essential part of integrating React-built frontend
applications with Django backend applications, ensuring that assets are correctly referenced
and loaded in a Django deployment.

The command reads the specified 'index.html' file, processes it using BeautifulSoup to identify
and modify <link> and <script> tags, and rewrites these tags to conform to Django's static file syntax.
This allows the use of the Django `{% static 'path' %}` template tag system for asset links, enabling
proper asset loading in Django's development and production environments.

Requirements:
- BeautifulSoup4: Ensure that 'beautifulsoup4' is installed in your environment.

Usage:
Run this command through Django's manage.py utility with the necessary arguments.

Example:
    python manage.py process_html --f index.html --dir /path/to/build --enc utf-8

Where:
    --f: Optional. Specify the file name to be processed, defaulting to 'index.html' if not provided.
    --dir: Optional. Specify the directory of the file, defaulting to the React build directory.
    --enc: Optional. Specify the file encoding, defaulting to 'utf-8'.

The command will attempt to read the specified HTML file, process the identified links and scripts,
rewrite them in Django static format, and write the updated content back to the same file. It provides
console messages about the progress and completion of the task.

Note:
This command is particularly suited for projects that use React for frontend development and Django for
backend development, helping bridge the gap between React's static assets and Django's static management.
"""

import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


# Constants and settings
HTML_ENCODING = 'utf-8'

# Directory where build files are located. Defaults to "build" directory in BASE_DIR.
BUILD_DIR = getattr(settings, 'BUILD_DIR', settings.BASE_DIR / "build")
# The base filename for build files, defaulted to 'index.html'.
BUILD_BASE_FILENAME = getattr(settings, 'BUILD_BASE_FILENAME', 'index.html')

# Static tag to load static files in Django.
STATIC_LOAD_TAG = '{% load static %}\n'
# Dictionary mapping HTML tags to their relevant attribute for static file paths.
TAG_ATTR = getattr(settings, 'TAG_ATTR', {'link': 'href', 'script': 'src'})
# Dictionary defining the directories for different static file types.
STATIC_FILE_TYPES = getattr(settings, 'STATIC_FILE_TYPES', {'js': 'js', 'css': 'css', 'image': 'images'})


def get_static_file_dir(filename: str) -> str:
    """
    Determine and return the static file directory based on the file type.

    Args:
        - filename (str): The filename whose directory needs to be found.

    Returns:
        - str: The directory path for the static file.
    """
    if filename.endswith('.js'):
        return STATIC_FILE_TYPES.get('js') + '/' + filename
    elif filename.endswith('.css'):
        return STATIC_FILE_TYPES.get('css') + '/' + filename
    else:
        return STATIC_FILE_TYPES.get('image') + '/' + filename


def process_html_file(soup) -> None:
    """
    Process an HTML file to modify static file paths to Django template format.

    This function iterates through <link> and <script> tags in the <head> of the HTML document,
    adjusting the file paths to use Django's static file templating system.

    Args:
        - soup (BeautifulSoup): A BeautifulSoup object of the HTML file.
    """
    for head in soup.select('head > link, head > script'):
        # Get tag attribute (href or src) based on the tag type.
        attr = TAG_ATTR.get(head.name, None)
        link = head.get(attr)

        # Exclude external links (CDNs) and template static urls.
        if link.startswith('https://') or (link.startswith('{%') and link.endswith('%}')):
            continue

        # Remove the '/static/' prefix from the link.
        cleaned_link = link.replace(f'/static/', '')

        # Ensure the directory is correctly prefixed, modifying it if necessary.
        if not cleaned_link.endswith(tuple(STATIC_FILE_TYPES.keys())):
            cleaned_link = get_static_file_dir(cleaned_link)

        # Modify the link to match Django's static file syntax.
        new_attr = f"{{% static '{cleaned_link}' %}}"
        head[attr] = new_attr


class Command(BaseCommand):
    """
    A custom Django management command to process the HTML file generated from the React building process.

    This command reads a specified HTML file, replaces specified header tags with Django template tags, and then writes
    the modified content back to the file.

    Attributes:
        - help: A brief description of the command. States 'Processes the React built HTML file to insert Django template tags'.

    Note:
    The current implementation only replaces the header tags that have link or script tag

    Returns:
        - Outputs a success message to stdout upon successful processing.
        - Outputs an error message to stdout if the specified file is not found or any error occurs during processing.
    """

    help = 'Processes the React built HTML file to insert Django template tags'

    def add_arguments(self, parser):
        """
        Adds command line arguments for this command.

        Args:
            - parser: The parser for command line arguments.

        Defines:
            --f: Optional. Specifies the file name to be processed. Defaults to BUILD_BASE_FILENAME.
            --dir: Optional. Specifies the directory of the file to be processed. Defaults to BUILD_DIR.
            --enc: Optional. Specifies the encoding to be used when reading and writing the file. Defaults to HTML_ENCODING.
        """
        parser.add_argument('--f', type=str, help='Enter the file name', default=BUILD_BASE_FILENAME)
        parser.add_argument('--dir', type=str, help='Enter the directory of the file name', default=BUILD_DIR)
        parser.add_argument('--enc', type=str, help='Encode the file', default=HTML_ENCODING)

    def handle(self, *args, **options):
        """
        The entry point for executing the command's logic.
        Orchestrates the flow: file retrieval, reading, processing, and writing back.

        Args:
            - *args: Variable length argument list.
            - **options: Arbitrary keyword arguments.
        """
        filename, filepath = self.get_file_details(options)
        soup = self.read_and_parse_html(filepath)
        self.process_and_write_back_html(soup, filepath, options)
        self.stdout.write(self.style.NOTICE('The processing is finished'))

    def get_file_details(self, options):
        """
        Retrieves the file name and constructs the file path from options.

        Args:
            - options (dict): Command options including 'f' for file name and 'dir' for directory.

        Returns:
            - tuple: A tuple containing the filename and the filepath.
        """
        filename, filedir = options.get('f'), options.get('dir')
        filepath = os.path.join(filedir, filename)
        return filename, filepath

    def read_and_parse_html(self, filepath):
        """
        Attempts to read the HTML file and parse it using BeautifulSoup.

        Args:
            - filepath (str): The complete path of the HTML file to read and parse.

        Returns:
            - BeautifulSoup: A BeautifulSoup object of the parsed HTML file.

        Raises:
            - CommandError: If the file cannot be opened, read, or parsed.
        """
        try:
            from bs4 import BeautifulSoup
            with open(filepath, 'r', encoding=HTML_ENCODING) as file:
                content = file.read()
        except ImportError:
            raise CommandError(
                "BeautifulSoup is not installed. Please install it with 'pip install beautifulsoup4' to use this "
                "command."
            )
        except FileNotFoundError:
            raise CommandError(f"The file {filepath} does not exist.")
        except Exception as e:
            raise CommandError(f"An error occurred while reading or parsing the file: {e}")
        else:
            return BeautifulSoup(content, 'html.parser')

    def process_and_write_back_html(self, soup, filepath, options):
        """
        Processes the HTML file and writes the changes back.

        Args:
            - soup (BeautifulSoup): The BeautifulSoup object of the HTML file to process.
            - filepath (str): The complete path of the HTML file to write back.
            - options (dict): Command options.

        Raises:
            - CommandError: If an error occurs during the processing of the HTML file.
        """
        try:
            process_html_file(soup)
            self.stdout.write(self.style.SUCCESS(f'Successfully parsed the HTML file'))
        except Exception as e:
            raise CommandError(f'Error occurred during processing with message: {e}')
        self.write_to_file(soup, filepath, options.get('enc'))

    def write_to_file(self, soup, filepath, encoding):
        """
        Writes the modified soup object back to the HTML file.

        Args:
            - soup (BeautifulSoup): The BeautifulSoup object of the HTML file to write back.
            - filepath (str): The complete path of the HTML file to write back.
            - encoding (str): Encoding type to use when writing the file.

        Returns:
            - None: This method writes to the file and does not return anything.
        """
        with open(filepath, "wb") as html_file_output:
            html_file_output.write(STATIC_LOAD_TAG.encode(encoding))
            html_file_output.write(soup.prettify().encode(encoding))
        self.stdout.write(self.style.SUCCESS(f'Successfully updated the file at {filepath}'))
