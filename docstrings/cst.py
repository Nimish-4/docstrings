import libcst as cst

from typing import List, Tuple, Dict, Optional
from .docgenerator import DOCSTRING_FOR_CLASS, DOCSTRING_FOR_FUNCTION

class FunctionAndClassVisitor(cst.CSTTransformer):
    def __init__(self, file_path=None):
        self.stack: List[Tuple[str, ...]] = []
        self.indent_level = 0  # no. of whitespaces at current level
        self.file_path = file_path
        self.missing_docstrings = []

    def _build_indented_docstring(self, raw_text: str, indent_ws: str) -> str:
        lines = raw_text.strip("\n").splitlines()
        formatted_lines = ['"""' + lines[0]]
        num_whitespaces = indent_ws

        for line in lines[1:]:
            formatted_lines.append(num_whitespaces + line)
        formatted_lines.append(num_whitespaces + '"""')

        return "\n".join(formatted_lines)

    def _get_indent_level(self, node):

        if node.body.indent is not None:
            indent_ws = len(node.body.indent)

        elif node.body.body:
            first_stmt = node.body.body[0]
            indent_ws = (
                len(first_stmt.leading_lines[0].indent.value)
                if first_stmt.leading_lines and first_stmt.leading_lines[0].indent
                else 4
            )
        else:
            indent_ws = 4

        return indent_ws

    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:

        self.indent_level += self._get_indent_level(node)
        return True

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.CSTNode:

        current_indent = self._get_indent_level(original_node)
        self.indent_level -= current_indent

        return updated_node

    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
        self.indent_level += self._get_indent_level(node)

        # Do not visit functions inside functions
        return False

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.CSTNode:

        indent_ws = self.indent_level * " "
        current_indent = self._get_indent_level(original_node)
        self.indent_level -= current_indent

        if original_node.get_docstring() is not None:
            return updated_node

        # Determine indentation based on the body
        final_docstring = self._build_indented_docstring(DOCSTRING_FOR_CLASS, indent_ws)

        docstring_stmt = cst.SimpleStatementLine(
            body=[cst.Expr(value=cst.SimpleString(final_docstring))],
        )
        new_body = updated_node.body.with_changes(
            body=[docstring_stmt] + list(updated_node.body.body)
        )

        return updated_node.with_changes(body=new_body)

    def _store_missing_docstrings(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
        module = cst.parse_module(source_code)

        visitor = FunctionAndClassVisitor()
        module.visit(visitor)
        for node in visitor.stack2:
            if node.get_docstring() is None:
                self.missing_docstrings.append(node)
