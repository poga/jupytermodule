# jupyter-module

Import jupyter notebook as a python module

## Install

```
pip install jupytermodule
```

## Synopsis

```python
from jupytermodule import open

notebook_module = open("...")

print(notebook_module.primes(10))
# [2,3,5,7]
print(notebook_module.PI)
# 3.1415
```