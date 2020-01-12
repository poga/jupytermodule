import ast
import astor
from pprint import pprint


class Extractor(ast.NodeVisitor):
    def __init__(self):
        self.extracted = []

    def visit_Import(self, node):
        self.extracted.append(astor.to_source(node))
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.extracted.append(astor.to_source(node))
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.extracted.append(astor.to_source(node))
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.extracted.append(astor.to_source(node))
        self.generic_visit(node)

    def code(self):
        code = ""

        for c in self.extracted:
            code += c
            code += "\n"

        return code
