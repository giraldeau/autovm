#!/usr/bin/env python
# coding=utf-8

from os.path import join, dirname, exists
from os import makedirs, utime, unlink, walk

# http://stackoverflow.com/questions/12654772/create-empty-file-using-python
def touch(path):
    d = dirname(path)
    if not exists(d):
        makedirs(d)
    with open(path, 'a'):
        utime(path, None)

class AbstractWalkerVisitor(object):
    def visit_file(self, root, name):
        print "f %s" % repr(join(root, name))
    def visit_dir(self, root, name):
        print "d %s" % repr(join(root, name))

class PrintWalkerVisitor(AbstractWalkerVisitor):
    def visit_file(self, root, name):
        print "f %s" % repr(join(root, name))
    def visit_dir(self, root, name):
        print "d %s" % repr(join(root, name))

class CountWalkerVisitor(AbstractWalkerVisitor):
    def __init__(self):
        self.files = 0
        self.directories = 0
    def visit_file(self, root, name):
        self.files += 1
    def visit_dir(self, root, name):
        self.directories += 1

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