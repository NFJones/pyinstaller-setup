import sys
import os
import inspect
import re
from setuptools import setup as setuptools_setup

ENTRY_POINT_TEMPLATE = """
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import re
import sys

from {} import {}

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit({}())
"""


class setup(object):
    """
    This is intended to run pyinstaller in order to make executables out of
    all of the scripts and console script entry points listed in setuptools.setup

    Usage:
        ```
        python ./setup.py build
        python ./setup.py install
        python ./setup.py pyinstaller [-- pyinstaller-opts ...]
        ```
    """

    def __init__(self, scripts=None, entry_points=None, **kwargs):
        self.scripts = scripts
        self.entry_points = entry_points

        if "pyinstaller" in sys.argv:
            if "--" in sys.argv and sys.argv.index("--") < len(sys.argv) - 1:
                self.flags = " ".join(sys.argv[sys.argv.index("--") + 1 :])
            else:
                self.flags = ""

            if not os.path.exists("./dist"):
                os.mkdir("dist")

            if self.scripts:
                self.install_scripts()
            if self.entry_points:
                self.install_entry_points()
        else:
            setuptools_setup(scripts=scripts, entry_points=entry_points, **kwargs)

    def pyinstaller(self, name, target):
        if os.system("pyinstaller --name {} {} {}".format(name, self.flags, target)):
            raise Exception("PyInstaller failed!")

    def install_scripts(self):
        for script in self.scripts:
            self.pyinstaller(os.path.basename(script).replace(".py", ""), script)

    def install_entry_points(self):
        if "console_scripts" in self.entry_points.keys():
            for entry_point in self.entry_points["console_scripts"]:
                name, entry = [part.strip() for part in entry_point.split("=")]
                module, func = [part.strip() for part in entry.split(":")]

                script = inspect.cleandoc(
                    ENTRY_POINT_TEMPLATE.format(module, func, func)
                )

                input_file = "dist/{}_entry.py".format(name)
                with open(input_file, "w") as outfile:
                    outfile.write(script)

                self.pyinstaller(name, input_file)
