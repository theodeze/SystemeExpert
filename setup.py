from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='SystemeExpert',
    version='0.1',
    description='Systeme Expert 0+',
    url='https://github.com/theodeze/SystemeExpert',
    packages=find_packages(exclude=['docs']),
    install_requires=['pptree'],
    entry_points={
        'console_scripts': [
            'systemeexpert = src.main:main',
        ],
    }
)