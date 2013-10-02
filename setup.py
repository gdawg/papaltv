from setuptools import setup, find_packages
import subprocess

try:
      subprocess.check_call('pandoc --from=markdown README.md --to=rst --output=README.rst',shell=True)
except Exception, e:
      print '*** NOTE: this package uses pandoc to generate rst documentation '
      print 'from the original markdown and this step just failed! you need pandoc'
      print 'installed and in your path locally for this to work.'
      print ''
      print 'the error returned was',e
      print ''
      print 'continuing anyway...'


with open('README.rst') as file:
    long_description = file.read()

setup(name='papaltv',
      version='0.2.2',
      description='Interactive shell Apple Tv controller',
      long_description=long_description,
      author='Andrew Griffiths',
      author_email='andrew.john.griffiths@gmail.com',
      url='http://github.com/gdawg/papaltv',
      packages = ['papaltv'],
      scripts = ['bin/papaltv'],
      install_requires = ['beautifulsoup4']
 )
