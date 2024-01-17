from setuptools import setup, find_packages

# Read in the README.md for the long description on PyPI
with open("README.md", "r") as f:
    long_description = f.read()

VERSION = "0.0.4"
DESCRIPTION = "Simple SVG graphing package"

setup(
    name="svgsimplegraph",
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
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
    project_urls={
        "Source Code": "https://github.com/GarrettPetersen/svgsimplegraph",
    },
)
