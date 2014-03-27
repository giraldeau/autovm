#!/usr/bin/env python
# coding=utf-8

import os
from os.path import join, dirname, exists
from os import makedirs, utime, unlink, walk
from heapq import heappush, heappop, heappushpop
import platform
import sys

def terminal_size():
    import fcntl, termios, struct
    h, w, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return w, h

def default_dist():
    (a, b, c) = platform.dist()
    return c

def default_arch():
    mapping = { 'x86_64': 'amd64', 'i386': 'i386' }
    arch = platform.machine()
    return mapping.get(arch, 'amd64')

class NullProgressMonitor(object):
    def __init__(self, msg="progress"):
        pass
    def update(self, percent):
        pass

class CmdProgressMonitor(object):
    def __init__(self, msg="progress"):
        self.msg = msg
    def update(self, percent):
        (w, h) = terminal_size()
        bar = w - len(self.msg) - 10
        rep = int((bar * percent) + 1)
        blank = bar - rep
        sys.stdout.write("%s %s%s %.1f%%\r" % (self.msg, ' ' * blank,  '#' * rep, percent * 100.0))

null_progress = NullProgressMonitor()

def copyfileobj_progress(fsrc, fdst, size, length=16*1024, progress=null_progress):
    """copy data from file-like object fsrc to file-like object fdst"""
    total = 0.0
    if size == 0:
        return
    while 1:
        progress.update(total / size)
        buf = fsrc.read(length)
        total += len(buf)
        if not buf:
            break
        fdst.write(buf)
    progress.update(1.0)

# http://stackoverflow.com/questions/12654772/create-empty-file-using-python
def touch(path):
    d = dirname(path)
    if not exists(d):
        makedirs(d)
    with open(path, 'a'):
        utime(path, None)

class AbstractWalkerVisitor(object):
    def visit_file(self, root, name):
        pass
    def visit_dir(self, root, name):
        pass

class PrintWalkerVisitor(AbstractWalkerVisitor):
    def visit_file(self, root, name):
        print "f %s" % repr(join(root, name))
    def visit_dir(self, root, name):
        print "d %s" % repr(join(root, name))

class EntriesWalkerVisitor(AbstractWalkerVisitor):
    def __init__(self):
        self.entries = []
    def visit_file(self, root, name):
        self.entries.append(join(root, name))

class CountWalkerVisitor(AbstractWalkerVisitor):
    def __init__(self):
        self.files = 0
        self.directories = 0
    def visit_file(self, root, name):
        self.files += 1
    def visit_dir(self, root, name):
        self.directories += 1

class FileEntry(object):
    def __init__(self, path):
        self.path = path
        self.st = os.stat(path)
    def __cmp__(self, other):
        if (self.st.st_mtime < other.st.st_mtime):
            return 1
        elif (self.st.st_mtime == other.st.st_mtime):
            return 0
        return -1
    def __repr__(self):
        return "%s %s" % (str(self.st.st_mtime), self.path)

class LRUWalkerVisitor(AbstractWalkerVisitor):
    'make the list of least used files'
    def __init__(self, max_item=100):
        self.heap = []
        self.max_item = max_item
    def visit_file(self, root, name):
        item = FileEntry(join(root, name))
        if len(self.heap) < self.max_item:
            heappush(self.heap, item)
        else:
            heappushpop(self.heap, item)
    def get_entries(self):
        return [heappop(self.heap) for i in range(len(self.heap))]
        
class DeleteWalkerVisitor(AbstractWalkerVisitor):
    def visit_file(self, root, name):
        unlink(join(root, name))
    def visit_dir(self, root, name):
        unlink(join(root, name))
            
class Walker(object):
    'Scan directory and feed visitor'
    def process(self, path, *visitor):
        for root, dirs, files in walk(path, topdown=False):
            for name in files:
                for v in visitor:
                    v.visit_file(root, name)
            for name in dirs:
                for v in visitor:
                    v.visit_dir(root, name)