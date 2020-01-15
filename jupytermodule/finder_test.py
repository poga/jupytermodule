from os.path import join
from jupytermodule import open

import unittest

import pathlib


class JupyterFinderTest(unittest.TestCase):
    def test_local_file(self):
        url = join(pathlib.Path().absolute(), "examples/primes.ipynb")

        m = open("file://" + url)

        self.assertEqual(m.primes(10), [2, 3, 5, 7])
        self.assertEqual(m.PI, 3.1415)

    def test_remote_file(self):
        url = "https://raw.githubusercontent.com/poga/jupytermodule/master/examples/primes.ipynb"

        m = open(url)

        self.assertEqual(m.primes(10), [2, 3, 5, 7])
        self.assertEqual(m.PI, 3.1415)


if __name__ == '__main__':
    unittest.main()
