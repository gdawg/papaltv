"""AppleTV control via fireCore's AirControl protocol

This if for jailbroken TV's running fireCore's protocol only. 

See their page for details:

    http://support.firecore.com/entries/21375902-3rd-Party-Control-API-AirControl-beta-

This file contains library components used to talk to the tv.

You may also be looking for the command line controller, see
papaltvvmd.py instead of this file.
"""
import logging
import plistlib
import urllib2
from xml.parsers.expat import ExpatError 

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class AppleTV(object):
    def __init__(self,host='apple-tv.local'):
        object.__init__(self)
        self.host = host

    # ===== commands
    def ls(self,path=''):
        return self._get_entries(path)

    def find(self):
        return self._find()

    def load(self,path):
        tvpath = self._tvpath(path)
        self._soupify('plugin={0}'.format(tvpath))

    def now_playing(self):
        soup = self._soupify('np')
        try:
            return plistlib.readPlistFromString(str(soup))
        except ExpatError:
            return None

    def type(self,args):
        txt = args.strip()
        soup = self._soupify('enterText={0}'.format(txt))

    def menu(self): 
        self._soupify('remoteAction=1')
    def hold_menu(self): 
        self._soupify('remoteAction=2')
    def up(self): 
        self._soupify('remoteAction=3')
    def down(self): 
        self._soupify('remoteAction=4')
    def select(self): 
        self._soupify('remoteAction=5')
    def left(self): 
        self._soupify('remoteAction=6')
    def right(self): 
        self._soupify('remoteAction=7')
    def toggle(self): 
        self._soupify('remoteAction=10')
    def playpause(self): 
        self._soupify('remoteAction=10')
    def pause(self): 
        self._soupify('remoteAction=15')
    def play(self): 
        self._soupify('remoteAction=16')
    def stop(self): 
        self._soupify('remoteAction=17')
    def ff(self): 
        self._soupify('remoteAction=18')
    def rw(self): 
        self._soupify('remoteAction=19')
    def skip(self): 
        self._soupify('remoteAction=20')
    def skip_back(self): 
        self._soupify('remoteAction=21')
    def hold_select(self): 
        self._soupify('remoteAction=22')


    # ===== internals
    def _soupify(self,path):
        try:
            url = 'http://{0}/{1}'.format(self.host,path)
            logger.debug('fetching ' + url)
            f = urllib2.urlopen(url)
            return BeautifulSoup(f.read())
        except urllib2.URLError, e:
            logger.error(' failed to contact appletv ({0})'.format(e))
            return BeautifulSoup('<html><body>error {0}</body></html>'.format(e))


    def _tvpath(self,path):
        realparts = []

        for p in [p for p in path.split('/') if p != '']:
            entries = {}
            if len(realparts) == 0:
                soup = self._soupify('apl')
                for x in soup.find_all('appliance'):
                    entries[x['name']]=x['identifier']
            else:
                soup = self._soupify('appcat={0}'.format('/'.join(realparts)))
                for x in soup.find_all('category'):
                    entries[x['name']]=x['identifier']

            realparts.append(entries[p])

        return '/'.join(realparts)

    def _get_entries(self,path):
        entries = {}
        if path == '' or path == '/':
            soup = self._soupify('apl')
            for x in soup.find_all('appliance'):
                entries[x['name']]=x['identifier']
        else:
            soup = self._soupify('appcat={0}'.format(self._tvpath(path)))
            for x in soup.find_all('category'):
                entries[x['name']]=x['identifier']

        return entries

    def _find(self,root=''):
        paths = []
        for p in ['{0}/{1}'.format(root,p) for p in self._get_entries(root)]:
            paths.append(p)
            subpaths = self._find(p)
            paths = paths + subpaths
        return paths

