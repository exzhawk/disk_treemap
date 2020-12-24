#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess

import setuptools
from setuptools import setup


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


setup(
    name='disk_treemap',
    version='1.0.0',
    packages=['disk_treemap'],
    keyword='treemap',
    description='xsJust another disk usage analyzer with treemap GUI.',
    author='Epix Zhang',
    license='MIT',
    zip_safe=True,
    include_package_data=True,
    cmdclass={
        'build_static': BuildStatic,
    },
    install_requires=[
        'flask',
        'tqdm',
    ],
    extras_require={
        'compression': ["flask-compress"]
    },

    entry_points={
        'console_scripts': [
            'disk-treemap=disk_treemap.main:main',
        ]
    }
)
