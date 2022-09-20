#!/usr/bin/env python
"""client"""
import setuptools

__version__ = "0.0.1"

with open("requirements.txt", "r", encoding="utf-8") as f:
    INSTALL_REQUIRES = f.read().splitlines()


setuptools.setup(
    name="pauditor",
    version=__version__,
    description="The super duper Star Wars client thing!",
    packages=["client"],
    install_requires=INSTALL_REQUIRES,
    python_requires=">=3.10",
    entry_points={"console_scripts": ["client = client.main:main"]},
)
