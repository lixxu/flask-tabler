#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from Cython.Build import cythonize
from setuptools.command.build_py import build_py as _build_py

package = "flask_tabler"


class build_py(_build_py):
    def run(self):
        self.run_command("build_ext")
        result = super().run()
        [path.unlink() for path in Path(package).glob("*.c")]
        return result

    def initialize_options(self):
        super().initialize_options()
        if self.distribution.ext_modules is None:
            self.distribution.ext_modules = []

        [path.unlink() for path in Path(package).glob("*.c")]
        files = [f"{package}/{p.name}" for p in Path(package).glob("*.py")]
        self.distribution.ext_modules = cythonize(files, language_level=3)
