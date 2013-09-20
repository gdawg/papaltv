#!/usr/bin/env python
import argparse
import sys
import logging
import os

from papaltvcmd import PapalTvCmd

def greeting(host):
    welcome = 'Welcome to Papaltv,'
    print '\n'.join([
        '    _          ',
        '  _| |_    {0} ',
        ' (_   _)   {1} ',
        '   | |         ',
        '   |_|     {2} ',
        ''
        ]).format(
            welcome.rjust(max(len(welcome),len(host))),
            'you are blessed.'.rjust(max(len(welcome),len(host))),
            host.rjust(max(len(welcome),len(host)))
            )

def main():
    logging.basicConfig()

    parser = argparse.ArgumentParser()
    parser.add_argument('--host',help="apple tv hostname",default='apple-tv.local')
    parser.add_argument('--cmd',help="issue a single command then quit")
    parser.add_argument('--commands',action='store_true',help="lists information on avilable commands")
    args = parser.parse_args()

    tv = PapalTvCmd(host=args.host)

    if args.commands:
        parser.print_help()
        print 'The following commands are available as options to --cmd'
        tv.onecmd('help')
    elif args.cmd:
        tv.onecmd(args.cmd)
    else:
        tv.cmdloop(intro=greeting(args.host))

if __name__ == '__main__':
    main()