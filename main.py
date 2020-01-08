# import importer
from importer import nbimport

url = "http://localhost:8000/Untitled.ipynb"

m = nbimport(url)

print(m.primes(100))