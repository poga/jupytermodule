# jupyter-module

Import jupyter notebooks as python modules

## Install

```
pip install jupytermodule
```

## Synopsis

```python
from jupytermodule import open

notebook_module = open("https://raw.githubusercontent.com/poga/jupyter-module/master/examples/primes.ipynb")

print(notebook_module.primes(10))
# [2,3,5,7]
print(notebook_module.PI)
# 3.1415
```