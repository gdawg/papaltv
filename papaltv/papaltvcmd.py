"""Commandline AppleTV control via fireCore's AirControl protocol

This if for jailbroken TV's running fireCore's protocol only. 

See their page for details:

    http://support.firecore.com/entries/21375902-3rd-Party-Control-API-AirControl-beta-


This package provides both an interactive shell and a python
library for communicating with jailbroken Apple TV's.

There's folder list options, navigation, searching, play,
pause, now playing info etc!

Login:
    awesomehost: $ papaltv
        _
      _| |_    Welcome to Papaltv,
     (_   _)      you are blessed.
       | |
       |_|          apple-tv.local    

    apple-tv.local$ ls
     Add Site
     Apple Events
     Browser
     Computers
     Flickr
     Infuse
     MLB.TV

...


Navigation:
    apple-tv.local$ cd /Settings/General

Menu Control
    apple-tv.local$ down
    apple-tv.local$ up
    apple-tv.local$ menu
    apple-tv.local$ hold_select

Shortcut comands  (up and menu shown below)
    apple-tv.local$ u    
    apple-tv.local$ m

Chained commands for quick navigation
    apple-tv.local$ mmmmrr


Quite a few commands implemented
    apple-tv.local$ help    

    ======================
    EOF   find         log        menu   playing    quit   select     stop    up
    cd    hold_menu    log_debug  ok     playpause  right  skip       text
    down  hold_select  log_warn   pause  psoup      rw     skip_back  toggle
    ff    left         ls         play   q          sel    soup       type


"""
import re
from argparse import ArgumentParser
import urllib2
import logging
from bs4 import BeautifulSoup
import cmd
from cmd import Cmd
import pdb
import time
import plistlib
import pprint
import json

from tv import AppleTV

logger = logging.getLogger(__name__)

# time to pause when we see ',' chars in command strings
_menu_wait_time = 2.5
# time in between chained presses
_quick_key_interval = 0.20
# I think 255 is generous here, be careful what you wish for! 
_max_key_quantifier = 255

class PapalTvCmd(cmd.Cmd):
    def __init__(self,host='apple-tv.local'):
        Cmd.__init__(self)
        self.tv = AppleTV()
        self.host = host
        self.shutdown = False
        self.prompt = host + '$ '

        self.quick_keys = {
            'm': self.do_menu,
            'hm': self.do_hold_menu,
            'u': self.do_up,
            'd': self.do_down,
            'o': self.do_ok,
            'ok': self.do_ok,
            'l': self.do_left,
            'r': self.do_right,
            'pp': self.do_playpause,
            'pa': self.do_pause,
            'pl': self.do_play,
            '>': self.do_play,
            'st': self.do_stop,
            '.': self.do_stop,
            'f': self.do_ff,
            'ff': self.do_ff,
            '*>': self.do_ff,
            'rw': self.do_rw,
            '<*': self.do_rw,
            'sk': self.do_skip,
            '#>': self.do_skip,
            'sb': self.do_skip_back,
            '<#': self.do_skip_back,
            'hs': self.do_hold_select,
            ',' : self._wait
        }
        keys = [self.escape_key(k) for k in self.quick_keys.keys()]
        keys = [r'\d*' + k for k in keys]
        quick_regex ='({0})'.format('|'.join(keys))
        self.re_keys = re.compile(r'{0}'.format(quick_regex))
        logger.debug('connecting to {0}'.format(host))


    # ===== apple tv or general logic / utils
    def escape_key(self,r):
        r = r.replace('.','\\.')
        r = r.replace('*','\\*')
        return r
    def encode(self,val):
        return unicode(val).encode('ascii','ignore')

    # ===== commands
    def do_ls(self,opts):
        minusl = True if opts.lower().find('-l') != -1 else False
        path = re.sub('-l','',opts).strip()
        try:
            self.print_dict(
                self.tv.ls(path),ommit_values=(not minusl))

        except KeyError, e:
            print '{0} not found'.format(e)

    def do_find(self,opts):
        for p in self.tv.find():
            print '',p

    def do_cd(self,opts):
        try:
            self.tv.load(opts.strip())
        except KeyError, e:
            print "{0} not found (don't forget to use absolute paths)".format(e)

    def print_dict(self,data,ommit_values=False):
        for key in sorted(data.keys()):
            if ommit_values:
                print ' {0}'.format(self.encode(key))
            else:
                print ' {0}: {1}'.format(self.encode(key),self.encode(data[key]))

    def do_playing(self,opts):
        show_all = True if opts.lower().find('all=true') != -1 else False

        try:
            data = self.tv.now_playing()
            if data:
                print 'Now Playing:'
                if show_all:
                    self.print_dict(data)
                else:
                    for k in [k for k in ['artistName','seasonName','trackNumber','title','mediaDescription'] if k in data.keys()]:
                        print ' {0}'.format(self.encode(data[k]))
            else:
                print 'No media currently playing.'
        except Exception, e:
            logger.error('{0}'.format(e))

    # straight through
    def do_menu(self,opts): 
        self.tv.menu() 
    def do_hold_menu(self,opts): 
        self.tv.hold_menu() 
    def do_up(self,opts): 
        self.tv.up() 
    def do_down(self,opts): 
        self.tv.down() 
    def do_select(self,opts): 
        self.tv.select() 
    def do_left(self,opts): 
        self.tv.left() 
    def do_right(self,opts): 
        self.tv.right() 
    def do_toggle(self,opts): 
        self.tv.toggle() 
    def do_playpause(self,opts): 
        self.tv.playpause() 
    def do_pause(self,opts): 
        self.tv.pause() 
    def do_play(self,opts): 
        self.tv.play() 
    def do_stop(self,opts): 
        self.tv.stop() 
    def do_ff(self,opts): 
        self.tv.ff() 
    def do_rw(self,opts): 
        self.tv.rw() 
    def do_skip(self,opts): 
        self.tv.skip() 
    def do_skip_back(self,opts): 
        self.tv.skip_back() 
    def do_hold_select(self,opts): 
        self.tv.hold_select() 

    # with arguments or aliases
    def do_np(self,opts):
        self.do_playing(opts)
    def do_text(self,args):
        self.tv.type(args.strip())
    def do_type(self,args):
        self.do_text(args)
    def do_ok(self,opts): 
        self.do_select(opts)
    def do_sel(self,opts): 
        self.do_select(opts)

    def help_np(self):
        print 'shows now playing info.'
        print '    the optional argument all=True will list extended info'

    # ===== magic parse logic to send multi
    # ===== command strings
    def default(self,line):
        keys = self.re_keys.findall(line.strip())
        if ''.join(keys) == line.strip():
            for key in keys:
                parts = re.split(r'(\D+)',key)
                count = int(parts[0]) if len(parts[0]) > 0 else 1
                key = parts[1]
                for x in xrange(0,min(count,_max_key_quantifier)):
                    self.quick_keys[key]('')
                    time.sleep(_quick_key_interval)
        else:
            Cmd.default(self,line)

    # opts ignored but accepted for consistency with other commands
    def _wait(self,opts=None):
        time.sleep(_menu_wait_time)


    # ===== developer commands
    def do_soup(self,opts):
        soup = self.soupify(opts.strip().split(' ')[0])
        print soup.prettify()
    def do_psoup(self,opts):
        soup = self.soupify(opts.strip().split(' ')[0])
        data = plistlib.readPlistFromString(str(soup))
        pprint.pprint(data,indent=2)

    def do_log(self,opts):
        level = opts.strip().lower()

        if level == 'debug':
            logger.setLevel(logging.DEBUG)
        if level == 'warning':
            logger.setLevel(logging.WARNING)
        if level == 'info':
            logger.setLevel(logging.INFO)
        if level == 'error':
            logger.setLevel(logging.ERROR)
    
    def do_log_debug(self,opts):
        self.do_log('debug')
    def do_log_warn(self,opts):
        self.do_log('warning')

    # ===== generic commands
    def do_quit(self,opts):
        self.shutdown = True
        print 'quiting...'
    def do_q(self,opts):
        self.do_quit(opts)
    def do_EOF(self,opts):
        self.do_quit(opts)

    def postcmd(self,stop,line):
        return self.shutdown
