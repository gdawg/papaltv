"""Commandline AppleTV control via fireCore's AirControl protocol

This class is an extension of the regular PapalTvCmd object included 
to demonstrate how you might go about implementing mapping between
your media collection and navigation. 

You'd pretty much have to be insane to do this...  but of course I did
mine and I figured it'd be rude not to at least include it as an example.


"""
from papaltv.papaltvcmd import PapalTvCmd
from volume import BaseVolume
from geezvolumes import MyCustomVolumeMap
import logging
import argparse
import pdb

class PopeVille(PapalTvCmd):
    def __init__(self,*args,**kwargs):
        PapalTvCmd.__init__(self,*args,**kwargs)
        self.volume_map = MyCustomVolumeMap()
        self.valid_prefix = ['mnt','Volumes','media']

    def is_volume_map_path(self,opts):
        try:
            components = [p for p in opts.strip().split('/') if len(p) > 0]
            return components[0] in self.valid_prefix
        except Exception, e:
            pass
        return False

    def remotepath(self,opts):
        components = [p for p in opts.strip().split('/') if len(p) > 0]
        return '/'.join(components[1:])

    def do_ls(self,opts):
        try:
            if self.is_volume_map_path(opts):
                remote_path = self.remotepath(opts)
                if self.volume_map.isdir(remote_path):
                    self.print_list(self.volume_map.listdir(remote_path))
                    return
        except Exception, e:
            pass
        
        return PapalTvCmd.do_ls(self,opts)

    def do_find(self,opts):
        print ''
        self.print_list(self.volume_map.listdir(''))
        PapalTvCmd.do_find(self,opts)

    def do_cd(self,opts):
        try:
            if self.is_volume_map_path(opts):
                remote_path = self.remotepath(opts)
                if self.volume_map.isdir(remote_path) or self.volume_map.isfile(remote_path):
                    cdcmd = self.volume_map.cdcmd(remote_path)
                    print "I'ma try some magic now... hold on:",cdcmd
                    self.onecmd(cdcmd)
                    return
        except Exception, e:
            logging.exception(e)
            pass

        return PapalTvCmd.do_cd(self,opts)

        
    def print_list(self,li):
        for i in li:
            print ' {0}'.format(i)
 



def greeting(host):
    welcome = 'Welcome to PopeVille,'
    print '\n'.join([
        '    / \        ',    
        '   |   |       ',     
        '   |___|   {0} ',     
        '           {1} ',    
        '   \/ \/       ',     
        '   O   O   {2} ',     
        '    ---        ',    
        ''
        ]).format(
            welcome.rjust(max(len(welcome),len(host))),
            'I am the blessed.'.rjust(max(len(welcome),len(host))),
            host.rjust(max(len(welcome),len(host)))
            )

def main():
    logging.basicConfig()

    parser = argparse.ArgumentParser()
    parser.add_argument('--host',help="apple tv hostname",default='apple-tv.local')
    parser.add_argument('--cmd',help="issue a single command then quit")
    parser.add_argument('--commands',action='store_true',help="lists information on avilable commands")
    args = parser.parse_args()

    tv = PopeVille(host=args.host)

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