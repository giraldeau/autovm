import argparse
import sys

from image import UbuntuImageCache
from helpers import default_arch, default_dist
from autovm.helpers import CmdProgressMonitor, NullProgressMonitor
from os.path import basename

dists = ['precise',
         'quantal',
         'raring',
         'saucy',
         'trusty',
         'vagrant']

arches = ['i386', 'amd64', 'armhf']

def cmd_fetch_image(args):
    cache = UbuntuImageCache()
    name = basename(cache._image_name(args.dist, args.arch))
    if not cache.has_image(args.dist, args.arch):
        progress = CmdProgressMonitor(name)
        cache.get_image(args.dist, args.arch, args.force, progress)
    print "%s ready" % (name)
    
def cmd_list_images(args):
    cache = UbuntuImageCache()
    entries = cache.file_cache.entries()
    if len(entries) == 0:
        print "no entry"
    else:
        print "entries (%d):" % (len(entries))
        for entry in entries:
            print "%s" % (repr(entry))

def cmd_template(args):
    d = {"tag": args.tag, "dist": args.dist, "arch": args.arch}
    prefix = "%(tag)s-%(dist)s-%(arch)s" % d
    name = "%(prefix)s-%(name)s" % {"prefix": prefix, "name": "template"}
    print "configure template %s" % (name)
    cache = UbuntuImageCache()
    if not cache.has_image(args.dist, args.arch):
        cmd_fetch_image(args.dist, args.arch)
    path = cache.get_image(args.dist, args.arch)
    
    
def main():
    cmds = {
        'get-image': cmd_fetch_image,
        'list-images': cmd_list_images,
        'make-template': cmd_template,
    }
    parser = argparse.ArgumentParser(description='Manage Ubuntu VMs')
    parser.add_argument('command', choices=cmds.keys(),
                        help='command to execute')
    parser.add_argument('--dist', choices=dists, default=default_dist(), help='distribution version')
    parser.add_argument('--arch', choices=arches, default=default_arch(), help='architecture')
    parser.add_argument('--tag', default="autovm", help='name')
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