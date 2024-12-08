from sphinx.application import Sphinx


def process_docstring(app: Sphinx, what: str, name: str, obj, options, lines) -> None:
    """
    Prepend an inheritance diagram to the docstring of classes.

    This function is designed to be connected to the 'autodoc-process-docstring' event
    in Sphinx. It automatically adds an inheritance diagram directive to the
    docstrings of classes being documented by Sphinx.

    Args:
        - app (Sphinx): The Sphinx application object.
        - what (str): The type of the object which the docstring belongs to (e.g., "class", "function").
        - name (str): The fully qualified name of the object.
        - obj: The object itself.
        - options: The options given to the directive: an object with attributes inherited_members, undoc_members,
          show_inheritance and noindex that are true if the flag option of same name was given to the auto directive.
        - lines (list of str): The lines of the docstring, which can be modified in place.
    """
    if what == "class":
        # Define the inheritance_diagram directive
        diagram_lines = [
            '.. inheritance-diagram:: ' + name,
            '   :parts: 1',
            ''
        ]
        lines[:0] = diagram_lines


def setup(app: Sphinx) -> None:
    """
    Connect the `process_docstring` function to the `autodoc-process-docstring` event in Sphinx.

    This setup function is intended to be used within a Sphinx extension. It connects
    the `process_docstring` function to the `autodoc-process-docstring` event, enabling
    automatic modification of docstrings during the documentation build process.

    Args:
        - app (Sphinx): The Sphinx application object.
    """
    # Connect the process_docstring function to the autodoc-process-docstring event
    app.connect("autodoc-process-docstring", process_docstring)
