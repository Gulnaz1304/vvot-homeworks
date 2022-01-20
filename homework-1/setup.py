from setuptools import setup, find_packages
from os.path import join, dirname

import src


setup(
    name='cloudphoto',
    version=1.0,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
        entry_points= {
            'console_scripts':
            ['cloudphoto = src.main:main']
        }
)