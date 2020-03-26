# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('LICENSE', "r") as f:
    license = f.read()

setuptools.setup(
    name="polygons-ilyaabramovich",
    version="0.0.1",
    author="Ilya Abramovich",
    author_email="ilyaabramovich1998@gmail.com",
    description="Package for polygon splitting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=license,
    url="https://github.com/ilyaabramovich/polygons",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
