import sys
import types
import os.path
from os.path import join
import re
from urllib.request import urlopen
import nbformat
from nbconvert import PythonExporter
import ast

from jupytermodule.extractor import Extractor


class JupyterFinder(object):
    def try_url(self, url_without_extension):
        url = url_without_extension

        if not (url.startswith("http") or url.startswith("file")):
            return None

        try:
            resp = urlopen(url)

            if resp:
                return url

        except Exception as e:
            # try again with .ipynb extension
            url += '.ipynb'
            try:
                resp = urlopen(url)

                if resp:
                    return url
            except Exception as e:
                return None

    def find_module(self, fullname, path=None):
        if self.try_url(fullname):
            return self

    def load_module(self, fullname):
        url = self.try_url(fullname)

        if fullname in sys.modules:
            return

        try:
            # The importer protocol requires the loader create a new module
            # object, set certain attributes on it, then add it to
            # `sys.modules` before executing the code inside the module (which
            # is when the "module" actually gets code inside it)
            m = types.ModuleType(fullname,
                                 'remote notebook: {}'.format(fullname))
            m.__file__ = '<notebook {}>'.format(fullname)
            m.__name__ = url
            m.__loader__ = self
            sys.modules[url] = m

            # Try to load notebook
            resp = urlopen(url)

            body = resp.read().decode()
            notebook = nbformat.reads(body, as_version=4)
            exporter = PythonExporter()
            (code, resources) = exporter.from_notebook_node(notebook)
            code = re.sub(r'%.+', "", code)

            tree = ast.parse(code)
            extractor = Extractor()
            extractor.visit(tree)

            exec(extractor.code(), sys.modules[url].__dict__)
            sys.modules[fullname] = sys.modules[url]

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


def open(url):
    return import_module(url)


sys.meta_path.append(JupyterFinder())

import unittest


class JupyterFinderTest(unittest.TestCase):
    def test_local_file(self):
        url = "file:///Users/poga/projects/jupyter-module/examples/primes.ipynb"

        m = open(url)

        self.assertEqual(m.primes(10), [2, 3, 5, 7])
        self.assertEqual(m.PI, 3.1415)


if __name__ == '__main__':
    unittest.main()