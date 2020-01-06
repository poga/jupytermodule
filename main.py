from urllib.request import urlopen
import ast
from pprint import pprint
import re
import astor

url = 'http://jakevdp.github.com/downloads/notebooks/XKCD_plots.ipynb'
response = urlopen(url).read().decode()
# print(response)

import nbformat
jake_notebook = nbformat.reads(response, as_version=4)
# print(jake_notebook.cells[9].source)
# print(jake_notebook.cells[12])

# 1. Import the exporter
from nbconvert import PythonExporter

# 2. Instantiate the exporter. We use the `basic` template for now; we'll get into more details
# later about how to customize the exporter further.
export = PythonExporter()

# 3. Process the notebook we loaded earlier
(body, resources) = export.from_notebook_node(jake_notebook)
# print(body)


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {"import": [], "from": []}

    def visit_Import(self, node):
        for alias in node.names:
            self.stats["import"].append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.stats["from"].append(alias.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        print(node.name, astor.to_source(node))

    def visit_ClassDef(self, node):
        print(node.name, astor.to_source(node))

    def report(self):
        pprint(self.stats)


py = re.sub(r'%.+', "", body)
# print(py)
tree = ast.parse(py)
analyzer = Analyzer()
analyzer.visit(tree)
analyzer.report()

# import importer
# import spam
# spam.foo()