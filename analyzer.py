import ast
import astor
from pprint import pprint


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {"import": [], "from": [], "defs": []}

    def visit_Import(self, node):
        for alias in node.names:
            self.stats["import"].append(astor.to_source(node))
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.stats["from"].append(astor.to_source(node))
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.stats["defs"].append(astor.to_source(node))
        # print(node.name, astor.to_source(node))
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.stats["defs"].append(astor.to_source(node))
        # print(node.name, astor.to_source(node))
        self.generic_visit(node)

    def report(self):
        pprint(self.stats)

    def code(self):
        code = ""

        for f in self.stats["from"]:
            code += f
            code += "\n"
        code += "\n"

        for i in self.stats["import"]:
            code += i
            code += "\n"
        code += "\n"

        for d in self.stats["defs"]:
            code += d
            code += "\n"
        code += "\n"

        return code
