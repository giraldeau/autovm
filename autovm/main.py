import argparse
import sys

from image import UbuntuImageCache
from helpers import default_arch, default_dist
from autovm.helpers import CmdProgressMonitor

dists = ['precise',
         'quantal',
         'raring',
         'saucy',
         'trusty',
         'vagrant']

arches = ['i386', 'amd64', 'armhf']

def cmd_download(args):
    #img = UbuntuImageCache.get_image()
    cache = UbuntuImageCache()
    progress = CmdProgressMonitor()
    print cache.get_image(args.dist, args.arch, args.force, progress)

def cmd_list_images(args):
    cache = UbuntuImageCache()
    entries = cache.file_cache.entries()
    if len(entries) == 0:
        print "no entry"
    else:
        print "entries (%d):" % (len(entries))
        for entry in entries:
            print "%s" % (repr(entry))

def main():
    cmds = {
        'download': cmd_download,
        'list-images': cmd_list_images,
    }
    parser = argparse.ArgumentParser(description='Manage Ubuntu VMs')
    parser.add_argument('command', choices=cmds.keys(),
                        help='command to execute')
    parser.add_argument('--dist', choices=dists, default=default_dist(), help='distribution version')
    parser.add_argument('--arch', choices=arches, default=default_arch(), help='architecture')
    parser.add_argument('--force', action='store_true', default=False, help='force')
    
    args = parser.parse_args()
    cmd = cmds.get(args.command, None)
    if cmd is None:
        args.print_usage()
        sys.exit(1)
    
    try:
        cmd(args)
    except KeyboardInterrupt:
        print " interrupted"