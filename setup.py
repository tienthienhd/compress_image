from __future__ import print_function

import distutils.spawn
import os
import re
import shlex
import subprocess
import sys

from setuptools import find_packages
from setuptools import setup


def get_version():
    filename = "compress_image/__init__.py"
    with open(filename) as f:
        match = re.search(
            r"""^__version__ = ['"]([^'"]*)['"]""", f.read(), re.M
        )
    if not match:
        raise RuntimeError("{} doesn't contain __version__".format(filename))
    version = match.groups()[0]
    return version


def get_install_requires():
    PY3 = sys.version_info[0] == 3
    PY2 = sys.version_info[0] == 2
    assert PY3 or PY2

    install_requires = [
        "Pillow"
    ]

    return install_requires


def get_long_description():
    with open("README.md") as f:
        long_description = f.read()


def main():
    version = get_version()

    if sys.argv[1] == "release":
        if not distutils.spawn.find_executable("twine"):
            print(
                "Please install twine:\n\n\tpip install twine\n",
                file=sys.stderr,
            )
            sys.exit(1)

        commands = [
            "git tag v{:s}".format(version),
            "git push origin master --tag",
            "python setup.py sdist",
            "twine upload dist/compress_image-{:s}.tar.gz".format(version),
        ]
        for cmd in commands:
            subprocess.check_call(shlex.split(cmd))
        sys.exit(0)

    setup(
        name="compress_image",
        version=version,
        packages=find_packages(exclude=["github2pypi"]),
        description="Compress Image Utils",
        long_description=get_long_description(),
        long_description_content_type="text/markdown",
        author="Thien NT",
        author_email="tienthienhd@gmail.com",
        url="https://github.com/tienthienhd/compress_image",
        install_requires=get_install_requires(),
        license="LICENSE",
        keywords="Image Utils, Image Compress",
        classifiers=[
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7"
        ],
        package_data={"compress_image": []},
        entry_points={
            "console_scripts": [
                "compress_image=compress_image.main:main"
            ],
        }
    )


if __name__ == "__main__":
    main()