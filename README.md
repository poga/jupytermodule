# jupyter-module

![](https://img.shields.io/pypi/v/jupytermodule?style=flat-square)
![](https://img.shields.io/pypi/l/jupytermodule?style=flat-square)

Import jupyter notebooks as python modules.

* Only imports, top-level variables, and class/function definition will be imported.
* Jupyter magics can still be used in the notebook without affecting importing.


## Install

```
pip install jupytermodule
```

## Synopsis

```python
from jupytermodule import open

notebook_module = open("https://raw.githubusercontent.com/poga/jupytermodule/master/examples/primes.ipynb")

print(notebook_module.primes(10))
# [2,3,5,7]

# Access to top-level variables
print(notebook_module.PI)
# 3.1415
```

## License

MIT
