'''
Created on Mar 28, 2014

@author: francis
'''
import unittest
from autovm.vm import QemuKvm


class Test(unittest.TestCase):

    def testName(self):
        vmm = QemuKvm()
        vmm.open()
        self.assertTrue(vmm.connected()) 


if __name__ == "__main__":
    unittest.main()