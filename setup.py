from setuptools import setup, find_packages

setup(name='papaltv',
      version='0.2',
      description='Interactive shell Apple Tv controller',
      long_description=
      """Commandline AppleTV control via fireCore's AirControl protocol
      See their page for details:

        http://support.firecore.com/entries/21375902-3rd-Party-Control-API-AirControl-beta-
      """,
      author='Andrew Griffiths',
      author_email='andrew.john.griffiths@gmail.com',
      url='http://github.com/gdawg/papaltv',
      packages = ['papaltv'],
      scripts = ['bin/papaltv'],
      install_requires = ['beautifulsoup4']
 )
