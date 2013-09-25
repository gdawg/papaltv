import os
import re
import logging
from volume import BaseVolume

_map_root = '/Volumes/nas/Video'

logger = logging.getLogger(__name__)

class MyCustomVolumeMap(object):
    """example class which reads from a drivemap on the papaltv host and converts
       between appleTV and local paths by stripping the mount prefix.
    """
    def __init__(self, real_rootdir=_map_root):
        super(MyCustomVolumeMap, self).__init__()
        self.real_rootdir = real_rootdir
        
    def realdir(self,path):
        return os.path.join(self.real_rootdir,path)

    def isdir(self,path):
        return os.path.isdir(self.realdir(path))

    def cdcmd(self,path):
        if not path.startswith('/'):
            path = '/' + path
        # start with keystrokes to get to the root
        cmdstr = [
            '4m2,,,'
            'do,',
            '4l2,,'
            ]

        parent = _map_root
        for d in [d for d in path.split('/') if len(d.strip()) > 0]:
            if d == 'tv':
                cmdstr = cmdstr + [ 'rro9,' ]
                list_view_mode = True
            elif d == 'movies':
                cmdstr = cmdstr + [ 'o7,' ]

            else:
                # anything under tv and one more should be in list view so we go down to navigate
                searchdir = parent
                navkey = 'r' if searchdir.find('/tv/') == -1 else 'd'
                paths = self.listdir(searchdir)
                paths = [re.sub(r'^The ','',p,flags=re.IGNORECASE) for p in paths]
                indir = sorted(paths,key=str.lower)
                # print 'in list is',indir
                idx = indir.index(d)

                logger.debug('')
                for p in indir[:idx]:
                    logger.debug('skipping show {0}'.format(p))

                cmdstr = cmdstr + [str(idx) + navkey]


            parent = parent + '/' + d


        cmdstr = cmdstr + ['o']

        return ''.join(cmdstr)
        
    def listdir(self,path):
        return sorted([p for p in os.listdir(self.realdir(path)) if not p.startswith('.')],key=str.lower)


    def isfile(self,path):
        return os.path.isfile(self.realdir(path))



