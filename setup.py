import os

from setuptools import find_packages, setup

import re

VERSIONFILE = "src/euring/_version.py"
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"

try:
    __version__ = re.search(VSRE, open(VERSIONFILE, "rt").read(), re.M).group(1)
except:  # noqa
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(
    name="euring",
    zip_safe=False,  # eggs are the devil.
    version=__version__,
    description="EURING toolkit for Python",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.rst")).read(),
    author="Dylan Verheul",
    author_email="dylan@zostera.nl",
    url="https://github.com/dyve/euring/",
    packages=find_packages("src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
    ],
    python_requires=">=3.4",
    install_requires=["Click", "requests", "beautifulsoup4"],
    entry_points="""
            [console_scripts]
            euring=euring.cli:euring_cli
        """,
)
