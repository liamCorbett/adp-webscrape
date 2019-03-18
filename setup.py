from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='adp-webscrape',
    version='0.1.0',
    author='Liam Corbett',
    description='A tool for scraping ADP Resource and ezLaborManager.',
    long_description=long_description,
    url='https://github.com/liamCorbett/adp-webscrape',
    keywords='adp selenium scraper',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['selenium']
)