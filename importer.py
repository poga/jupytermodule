import sys
import types
import os.path
from os.path import join
import re
# from pprint import pprint
from urllib.request import urlopen
import nbformat
from nbconvert import PythonExporter
import ast

from extractor import Extractor


class NbFinder(object):
    def try_url(self, url_without_extension):
        url = url_without_extension
        # print(url)
        try:
            resp = urlopen(url)

            if resp.getcode() == 200:
                return url
        except Exception as e:
            # try again with .ipynb extension
            url += '.ipynb'
            # print(url)
            try:
                resp = urlopen(url)

                if resp.getcode() == 200:
                    return url
            except Exception as e:
                return None

    def find_module(self, fullname, path=None):
        if self.try_url(fullname):
            return self

    def load_module(self, fullname):
        url = self.try_url(fullname)
        # print("loading", url)
        # If the module already exists in `sys.modules` we *must* use that
        # module, it's a mandatory part of the importer protcol
        if fullname in sys.modules:
            # Do nothing, just return None. This likely breaks the idempotency
            # of import statements, but again, in the interest of being brief,
            # we skip this part.
            return

        try:
            m = types.ModuleType(fullname,
                                 'remote notebook: {}'.format(fullname))
            m.__file__ = '<notebook {}>'.format(fullname)
            m.__name__ = url
            m.__loader__ = self
            sys.modules[url] = m

            # The importer protocol requires the loader create a new module
            # object, set certain attributes on it, then add it to
            # `sys.modules` before executing the code inside the module (which
            # is when the "module" actually gets code inside it)
            resp = urlopen(url)

            body = resp.read().decode()
            notebook = nbformat.reads(body, as_version=4)
            exporter = PythonExporter()
            (code, resources) = exporter.from_notebook_node(notebook)
            code = re.sub(r'%.+', "", code)

            tree = ast.parse(code)
            extractor = Extractor()
            extractor.visit(tree)
            # print(analyzer.code())

            # Attempt to open the file, and exec the code therein within the
            # newly created module's namespace
            # with open(location, 'r') as f:
            # print("execing", analyzer.code(), url)
            exec(extractor.code(), sys.modules[url].__dict__)
            sys.modules[fullname] = sys.modules[url]

            # Return our newly create module
            return m

        except Exception as e:
            # If it fails, we need to reset sys.modules to it's old state. This
            # is good practice in general, but also a mandatory part of the
            # spec, likely to keep the import statement idempotent and free of
            # side-effects across imports.

            # Delete the entry we might've created; use LBYL to avoid nested
            # exception handling
            if sys.modules.get(url):
                del sys.modules[url]
            raise e

            if sys.modules.get(fullname):
                del sys.modules[fullname]
            raise e


from importlib import import_module


def nbimport(url):
    return import_module(url)


sys.meta_path.append(NbFinder())
