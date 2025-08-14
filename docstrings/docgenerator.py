from docstrings.cst import FunctionAndClassVisitor

import libcst as cst
from pathlib import Path

DOCSTRING_FOR_FUNCTION = """
This is an example of a module level function.

Function parameters should be documented in the ``Parameters`` section.
The name of each parameter is required. The type and description of each
parameter is optional, but should be included if not obvious.

If \*args or \*\*kwargs are accepted,
they should be listed as ``*args`` and ``**kwargs``.

The format for a parameter is:

    name : type
        description

        The description may span multiple lines. Following lines
        should be indented to match the first line of the description.
        The ": type" is optional.

        Multiple paragraphs are supported in parameter
        descriptions.

Parameters
----------
param1 : int
    The first parameter.
param2 : :obj:`str`, optional
    The second parameter.
*args
    Variable length argument list.
**kwargs
    Arbitrary keyword arguments.

Returns
-------
bool
    True if successful, False otherwise.

    The return type is not optional. The ``Returns`` section may span
    multiple lines and paragraphs. Following lines should be indented to
    match the first line of the description.

    The ``Returns`` section supports any reStructuredText formatting,
    including literal blocks::

        {
            'param1': param1,
            'param2': param2
        }

Raises
------
AttributeError
    The ``Raises`` section is a list of all exceptions
    that are relevant to the interface.
ValueError
    If `param2` is equal to `param1`.
"""

DOCSTRING_FOR_CLASS = """One line summary for the class and its purpose.

The __init__ method can be documented either here, or have its separate 
docstring in the method itself. Stick with one of the two choices.
This paragraph (and others that may follow) are for explaining the 
class in more detail.

Note
----
Do not include the `self` parameter in the ``Parameters`` section.

Parameters
----------
num : float
    The number to be used for operations.
msg : str, optional
    Message to be displayed.

Attributes
----------
x : int
    Description of attribute `x`

Examples
--------
Import an example class

>>> from foo import bar
>>> y = bar(3.14)

References
----------
[1] ManeBo
"""


def process_module(file_path: str) -> bool:
    try:
        path = Path(file_path)
        source_code = path.read_text(encoding="utf-8")

        try:
            module = cst.parse_module(source_code)
        except Exception as parse_err:
            print(f"Skipping {file_path} (parse error): {parse_err}")
            return False

        visitor = FunctionAndClassVisitor(file_path=file_path)
        modified_module = module.visit(visitor)

        # Write back ONLY if changed
        if modified_module.code != source_code:
            path.write_text(modified_module.code, encoding="utf-8")
            print(f"Updated {file_path}")
        else:
            print(f"No changes in {file_path}")

        return True

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False
