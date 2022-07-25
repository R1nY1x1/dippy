from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dippy",
    packages=find_packages(),

    version="0.1",

    license="MIT",

    install_requires=['numpy'],

    author="RinYixi",
    author_email="hayashi0241@gmail.com",

    url="",

    description="Digital Image Processing in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="dippy Dippy",

    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
)
