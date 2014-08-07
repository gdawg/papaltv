from setuptools import setup, find_packages
import subprocess

with open('README.md') as file:
    long_description = file.read()

setup(name='papaltv',
      version='0.2.3',
      description='Interactive shell Apple Tv controller',
      long_description=long_description,
      author='Andrew Griffiths',
      author_email='andrew.john.griffiths@gmail.com',
      url='http://github.com/gdawg/papaltv',
      packages = ['papaltv'],
      scripts = ['bin/papaltv'],
      install_requires = ['beautifulsoup4']
 )
