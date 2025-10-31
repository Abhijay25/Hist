#!/usr/bin/env python3
"""Setup script for Hist CLI tool."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hist-cli",
    version="0.1.0",
    author="Hist Contributors",
    description="A command line tool to fuzzy-search command history",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Hist",
    py_modules=["hist", "history_loader", "runner", "utils"],
    python_requires=">=3.7",
    install_requires=[
        "rich>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "hist=hist:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
)
