#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess

import setuptools
from setuptools import setup
from disk_treemap import __version__


class BuildStatic(setuptools.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        cwd = 'disk_treemap/static'
        subprocess.call(['npm', 'install'], cwd=cwd)
        subprocess.call(['npm', 'run', 'build', '--', '--prod'], cwd=cwd)


with open('README.md', 'r', encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='disk_treemap',
    version=__version__,
    author='Epix Zhang',
    packages=['disk_treemap'],
    description='Just another disk usage analyzer with treemap GUI.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/exzhawk/disk_treemap',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "Programming Language :: JavaScript",
        "Topic :: Desktop Environment :: File Managers",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: System :: Filesystems",
        "Topic :: Utilities",
    ],
    python_requires='>=3.6',
    license='MIT',
    zip_safe=True,
    include_package_data=True,
    cmdclass={
        'build_static': BuildStatic,
    },
    install_requires=[
        'flask>=2.0',
        'tqdm',
        'flask-compress',
        'boto3',
    ],
    entry_points={
        'console_scripts': [
            'disk-treemap=disk_treemap.main:main',
        ]
    }
)
