'''
Created on Mar 28, 2014

@author: francis
'''
import unittest
from autovm.vm import QemuKvm


class Test(unittest.TestCase):

    def testOpen(self):
        vmm = QemuKvm()
        vmm.open()
        self.assertTrue(vmm.connected()) 

    def testAddNetwork(self):
        vmm = QemuKvm()
        vmm.open()
        vmm.add_subnet("192.168.42.0")
        self.assertTrue(vmm.has_subnet("192.168.42.0"))

if __name__ == "__main__":
    unittest.main()