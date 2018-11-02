from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='SystemeExpert',
    version='0.5',
    description='Systeme Expert 0+',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/theodeze/SystemeExpert',
    packages=find_packages(exclude=['docs']),
    install_requires=['pptree','pyside2'],
    include_package_data=True,
    package_data={'res/fonts': ['*.ttf'],
                'res/html' : ['*.html'],
                'res/icons' : ['*.svg']},
    entry_points={
        'console_scripts': [
            'se-cli = se:main_cli',
            'se-gui = se:main_gui',
        ],
    }
)