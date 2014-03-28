'''
Created on Mar 28, 2014

@author: francis
'''

import libvirt

class QemuKvm(object):
    '''
    Qemu/KVM wrapper
    '''
    def __init__(self, user=None, host=None):
        self.user = user
        self.host = host
        self.conn = None
    def connect_string(self):
        if (self.user and self.host):
            return "qemu+ssh://%s@%s/system" % (self.user, self.host)
        else:
            return "qemu:///system"
    def connected(self):
        return self.conn is not None
    def open(self):
        url = self.connect_string()
        self.conn = libvirt.open(url)
        if (not self.conn):
            raise RuntimeError("connect to %s failed" % url)
        