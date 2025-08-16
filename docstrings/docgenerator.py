from pathlib import Path

import libcst as cst

from docstrings.cst import FunctionAndClassVisitor

DOCSTRING_FOR_FUNCTION = """Summarize the function in one line.

Several sentences providing an extended description. Refer to
variables using back-ticks, e.g. `var`. For functions (also method and module),
there should be no blank lines after closing the docstring.

Parameters
----------
var1 : array_like
    Array_like means all those objects -- lists, nested lists, etc. --
    that can be converted to an array.  We can also refer to
    variables like `var1`.

var2 : int
    The type above can either refer to an actual Python type
    (e.g. ``int``), or describe the type of the variable in more
    detail, e.g. ``(N,) ndarray`` or ``array_like``.

*args : iterable
    Other arguments.

long_var_name : {'hi', 'ho'}, optional
    Choices in brackets, default first when optional.

Returns
-------
type
    Explanation of anonymous return value of type ``type``.

describe : type
    Explanation of return value named `describe`.

out : type
    Explanation of `out`.

type_without_description

Other Parameters
----------------
only_seldom_used_keyword : int, optional
    Infrequently used parameters can be described under this optional
    section to prevent cluttering the Parameters section.
**kwargs : dict
    Other infrequently used keyword arguments. Note that all keyword
    arguments appearing after the first parameter specified under the
    Other Parameters section, should also be described under this
    section.

Raises
------
BadException
    Because you shouldn't have done that.

See Also
--------
numpy.array : Relationship (optional).
numpy.ndarray : Relationship (optional), which could be fairly long, in
                which case the line wraps here.
numpy.dot, numpy.linalg.norm, numpy.eye

Notes
-----
Notes about the implementation algorithm (if needed).

This can have multiple paragraphs.

You may include some math:

.. math:: X(e^{j\omega } ) = x(n)e^{ - j\omega n}

And even use a Greek symbol like :math:`\omega` inline.

References
----------
Cite the relevant literature, e.g. [1]_.  You may also cite these
references in the notes section above.

.. [1] O. McNoleg, "The integration of GIS, remote sensing,
   expert systems and adaptive co-kriging for environmental habitat
   modelling of the Highland Haggis using object-oriented, fuzzy-logic
   and neural-network techniques," Computers & Geosciences, vol. 22,
   pp. 585-588, 1996.

Examples
--------
These are written in doctest format, and should illustrate how to
use the function.

>>> a = [1, 2, 3]
>>> print([x + 3 for x in a])
[4, 5, 6]
>>> print("a\nb")
a
b
"""

DOCSTRING_FOR_CLASS = """One line summary for the class and its purpose.

The __init__ method can be documented either here, or have its separate 
docstring in the method itself. Stick with one of the two choices.
This paragraph (and others that may follow) are for explaining the 
class in more detail.

After closing the class docstring, there should be one blank line to
separate following codes (PEP257).

Note
----
The `self` parameter is not listed as the first parameter of methods.

Parameters
----------
num : float
    The number to be used for operations.

msg : str (default: "")
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
[1] https://numpydoc.readthedocs.io/en/latest/
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

        # check if the code has been modified
        if modified_module.code != source_code:
            path.write_text(modified_module.code, encoding="utf-8")
            print(f"Updated {file_path}")
        else:
            print(f"No changes in {file_path}")

        return True

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False
