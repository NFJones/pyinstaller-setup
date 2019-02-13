# PyInstaller Setup

Use pyinstaller with setuptools!

## setup.py

```python
from pyinstaller_setuptools import setup

setup(
    ...
    scripts=['path/to/a/script.py'],
    entry_points={
        'console_scripts': ['entry=module.func']
    },
    ...
)
```

## Usage

```
> python ./setup.py build
> python ./setup.py install
> python ./setup.py pyinstaller [-- <pyinstaller-flags>]
```
