'''
Created on Mar 28, 2014

@author: francis
'''

import libvirt

"""
dist
arch
tag
num
subnet
size
user
host
"""
class VirtEnv(object):
    def __init__(self, vmm, **kwargs):
        self.vmm = vmm
        self.params = kwargs
    def setup(self):
        pass
    def start(self):
        pass
    def stop(self):
        pass
    def destroy(self):
        pass
        
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
    def add_subnet(self, subnet):
        for item in dir(self.conn):
            print item 
        networks = self.conn.listAllNetworks()
        for net in networks:
            print dir(net)
            print net.UUID()
            print net.UUIDString()
            print net.name()
        
    def has_subnet(self, subnet):
        pass
    def del_subnet(self, subnet):
        pass
    def delete(self):
        pass
    def start(self):
        pass
    def shutdown(self):
        pass
    def install(self):
        pass