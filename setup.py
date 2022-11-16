#!/usr/bin/env python3
# -*- coding=utf-8 -*-

"""
flask-tabler
--------------

flask-tabler is a collection of Jinja macros for tabler and Flask.
"""
from pathlib import Path

from setuptools import setup

version = ""
work_dir = Path(__file__).resolve().parent
for line in (work_dir / "flask_tabler/__init__.py").read_text().splitlines():
    if line.startswith("__version__ = "):
        version = line.split("=")[-1].strip().replace("'", "")
        break

setup(
    name="flask-tabler",
    version=version.replace('"', ""),
    url="https://github.com/lixxu/flask-tabler",
    license="BSD-3-Clause",
    author="Lix Xu",
    author_email="xuzenglin@gmail.com",
    description="a collection of Jinja macros for tabler and Flask",
    long_description=__doc__,
    long_description_content_type="text/markdown",
    packages=["flask_tabler"],
    zip_safe=False,
    platforms="any",
    include_package_data=True,
    install_requires=["flask", "wtforms"],
    keywords="flask extension development",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Flask",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
