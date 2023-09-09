from setuptools import setup
from setuptools import find_packages

VERSION = "0.0.1"
DESCRIPTION = "Simple SVG graphing package"
LONG_DESCRIPTION = "Graphing package that generates base64-encoded SVG graphs"

setup(
    name="svgsimplegraph",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Garrett M. Petersen",
    author_email="garrett.m.petersen@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=["matplotlib", "numpy"],
    keywords=["graph", "svg", "base64", "svg simple graph"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
