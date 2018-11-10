from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='sysexpert',
    version='0.2',
    description='Systeme Expert 0+',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='LICENSE.txt',
    author='Théo Dézé, Charles Mallet',
    author_email='theo.deze@etud.univ-angers.fr, charles.mallet@etud.univ-angers.fr',
    url='https://github.com/theodeze/SystemeExpert',
    python_requires='>=3',
    packages=find_packages(
        exclude=['docs']),
    install_requires=[
        'pptree>=2.0',
        'pyside2>=5.9.0'],
    include_package_data=True,
    package_data={
        'res/fonts': ['*.ttf'],
        'res/html': ['*.html'],
        'res/icons': ['*.svg']},
    entry_points={
        'console_scripts': [
            'se-cli = sysexpert:main_cli',
            'se-gui = sysexpert:main_gui',
        ],
    })
