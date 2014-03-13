#!/usr/bin/env python
# coding=utf-8

import unittest
from os.path import join
import shutil
import tempfile

from autovm.helpers import touch, Walker, CountWalkerVisitor

class Test(unittest.TestCase):
    def setUp(self):
        self.base = tempfile.mkdtemp()
        touch(join(self.base, "file1"))
        touch(join(self.base, "file2"))
        d = join(self.base, "dir1")
        touch(join(d, "file3"))
    def test_fn(self):
        
        w = Walker()
        c = CountWalkerVisitor()
        w.process(self.base, c)
        self.assertEqual(3, c.files)
        self.assertEqual(1, c.directories)
        
    def tearDown(self):
        shutil.rmtree(self.base)
        
if __name__ == "__main__":
    unittest.main()
