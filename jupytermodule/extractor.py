import ast
import astor


class Extractor(ast.NodeVisitor):
    def __init__(self):
        self.extracted = []

    def visit_Import(self, node):
        self.extracted.append(astor.to_source(node))

    def visit_ImportFrom(self, node):
        self.extracted.append(astor.to_source(node))

    def visit_FunctionDef(self, node):
        self.extracted.append(astor.to_source(node))

    def visit_ClassDef(self, node):
        self.extracted.append(astor.to_source(node))

    def visit_Assign(self, node):
        self.extracted.append(astor.to_source(node))

    def code(self):
        return "\n".join(self.extracted)
