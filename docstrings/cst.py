import libcst as cst
import os

from typing import List, Tuple, Dict, Optional
from docgenerator import DOCSTRING_FOR_CLASS
"""
print(type(original_node.body.children))
        print(type(original_node.body.children[0]))
        #t = cst.SimpleString(value=DOCSTRING_FOR_CLASS)
        if original_node.get_docstring() is None:
            cst.Expr(value=cst.SimpleString(value=DOCSTRING_FOR_CLASS), semicolon=cst.MaybeSentinel.DEFAULT )
            #print('yes')
            line_ = cst.IndentedBlock(body=[cst.SimpleStatementLine(
                body=[
                    cst.Expr(
                        value=cst.SimpleString(
                            value=DOCSTRING_FOR_CLASS,
                            lpar=[],
                            rpar=[],
                        ),
                        semicolon=cst.MaybeSentinel.DEFAULT,
                    ),
                ],
                leading_lines=[],
                trailing_whitespace=cst.TrailingWhitespace(
                    whitespace=cst.SimpleWhitespace(
                        value='',
                    ),
                    comment=None,
                    newline=cst.Newline(
                        value=None,
                    ),
                ),
            )],
            header=cst.TrailingWhitespace(
            whitespace=cst.SimpleWhitespace(
                value='',
            ),
            comment=None,
            newline=cst.Newline(
                value=None,
                ),
            ),
            indent=None,
            footer=[],
            )

            y = updated_node.deep_replace(updated_node.body, line_)
            print(type(updated_node.body))
            #z = cst.FunctionDef(body=cst.FlattenSentinel([]))
            #y = updated_node.deep_replace(updated_node.body.children, cst.FlattenSentinel([line_, original_node.body.children]))
            print(y.body)
            
            return  cst.FlattenSentinel([y, original_node.body]) #, *x, updated_node.body])


"""
class FunctionAndClassVisitor(cst.CSTTransformer):
    def __init__(self, file_path=None):
        # stack for storing the canonical name of the current function
        self.stack: List[Tuple[str, ...]] = []
        self.indent_level = ""
        self.file_path = file_path
        self.missing_docstrings = []

    def _create_docstring_stmt(self, doc_text: str, indent_ws: str) -> cst.SimpleStatementLine:
    
        return cst.SimpleStatementLine(
            body=[cst.Expr(value=cst.SimpleString(doc_text))],
            leading_lines=[cst.EmptyLine(indent=cst.SimpleWhitespace(indent_ws))],
        )
    
    def _build_indented_docstring(self, raw_text: str, indent_ws: str) -> str:
        lines = raw_text.strip("\n").splitlines()
        formatted_lines = ['"""' + lines[0]] 

        for line in lines[1:]:
            formatted_lines.append(indent_ws + line)

        formatted_lines.append(indent_ws + '"""')  # closing quotes

        return "\n".join(formatted_lines)

    def _get_indent_level(self, node):
        #print(node)
        #print(node.body)
        if node.body.body:
            first_stmt = node.body.body[0]
            indent_ws = (
                first_stmt.leading_lines[0].indent.value
                if first_stmt.leading_lines and first_stmt.leading_lines[0].indent
                else " " * 4
            )
        else:
            indent_ws = " " * 4
        
        return indent_ws
    
    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        self.stack.append(node.name.value)
        self.indent_level += self._get_indent_level(node)

        print("visit_class", node.name.value, len(self.indent_level))
        return True

    def leave_ClassDef( self, original_node: cst.ClassDef, updated_node: cst.ClassDef) -> cst.CSTNode:
        # self.stack.pop()
        #self.stack.pop()
        current_indent = self._get_indent_level(original_node)
        self.indent_level = (len(self.indent_level) - len(current_indent)) * " "
        print("leave_class", original_node.name.value, len(self.indent_level))
        return updated_node

    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
        self.stack.append(node.name.value)
        self.indent_level += self._get_indent_level(node)
        print("visit_func", node.name.value, len(self.indent_level))
        return (
            False
        )  # not visiting functions inside functions

    def leave_FunctionDef( self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.CSTNode:

        indent_ws = len(self.indent_level)*" "    #self._get_indent_level(original_node)
        current_indent = self._get_indent_level(original_node)
        self.indent_level = (len(self.indent_level) - len(current_indent)) * " "
        print("leave_func", original_node.name.value, len(self.indent_level))

        if original_node.get_docstring() is not None:
            return updated_node
        # Determine indentation based on the body

        #print(len(indent_ws), indent_ws)
        final_docstring = self._build_indented_docstring(DOCSTRING_FOR_CLASS, indent_ws)

        docstring_stmt = cst.SimpleStatementLine(
            body=[cst.Expr(value=cst.SimpleString(final_docstring))],
            leading_lines=[cst.EmptyLine(indent=cst.SimpleWhitespace("    " + indent_ws))],
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
        


def convert_cst(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
    module = cst.parse_module(source_code)

    visitor = FunctionAndClassVisitor()
    modified_code = module.visit(visitor)
    print(modified_code.code)


convert_cst(r"C:\Users\Nimish Purohit\docstrings\dummy.py")
