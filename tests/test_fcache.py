'''
Created on Mar 13, 2014

@author: francis
'''
import unittest
from os.path import join, exists, isfile
from os import makedirs
import tempfile
import shutil
import time
from autovm.helpers import touch
from autovm.fcache import LocalFileProvider, FileCache 

F1 = "file1"
MSG = "testing"

class TestFileProvider(LocalFileProvider):
    def __init__(self, path):
        super(TestFileProvider, self).__init__(path)
        self.fetch_count = 0
    def fetch(self, name):
        self.fetch_count += 1
        return super(TestFileProvider, self).fetch(name)

def _w(path, data):
    f = open(path, "w")
    f.write(data)
    f.close()

class TestBase(unittest.TestCase):
    
    def setUp(self):
        self.base = "source"
        makedirs(self.base)
        self.cache = tempfile.mkdtemp()
        self.file1 = join(self.base, F1)
        _w(self.file1, MSG)
        self.provider = TestFileProvider(self.base)
        self.fc = FileCache(self.cache, self.provider)
        
    def test_get(self):
        # The file is not in the cache
        self.assertFalse(self.fc.has_file(F1))
        
        # Add the file to the cache
        path = self.fc.get_file(F1)
        
        # The file is in the cache
        self.assertTrue(self.fc.has_file(F1))
        self.assertTrue(exists(path))
        self.assertTrue(isfile(path))
        self.assertEqual(join(self.cache, F1), path)
        
        # Check that content matches
        with open(path, 'r') as f:
            m = f.read()
        self.assertEqual(MSG, m)

    def test_fetch_once(self):
        # check the file is not fetch again
        self.assertEqual(self.provider.fetch_count, 0)
        self.fc.get_file(F1)
        self.assertEqual(self.provider.fetch_count, 1)
        self.fc.get_file(F1)
        self.assertEqual(self.provider.fetch_count, 1)
        self.assertEqual(self.fc.count(), 1)
        
    def test_clear(self):
        # clear the cache, should re-fetch
        self.fc.get_file(F1)
        self.assertEqual(self.provider.fetch_count, 1)
        self.assertTrue(self.fc.has_file(F1))
        self.fc.clear()
        self.assertFalse(self.fc.has_file(F1))
        self.fc.get_file(F1)
        self.assertEqual(self.provider.fetch_count, 2)
        self.assertEqual(self.fc.count(), 1)
        
    def tearDown(self):
        shutil.rmtree(self.base)
        shutil.rmtree(self.cache)

def _ifile(i):
    return "file%d" % i

class TestLRU(unittest.TestCase):
    
    def setUp(self):
        self.base = "source"
        makedirs(self.base)
        for i in range(100):
            touch(join(self.base, _ifile(i)))
        self.cache = tempfile.mkdtemp()
        self.fc = FileCache(self.cache, LocalFileProvider(self.base), max_size=5)

    def test_max_item(self):
        for i in range(10):
            self.fc.get_file(_ifile(i))
            time.sleep(0.01) # make timestamps drift
        entries = self.fc._lru_entries(5)
        print
        for e in entries:
            print e
        self.assertEqual(self.fc.count(), 10)
        self.fc.cleanup()
        self.assertEqual(self.fc.count(), 5)
        
    def tearDown(self):
        shutil.rmtree(self.base)
        shutil.rmtree(self.cache)
    
if __name__ == "__main__":
    unittest.main()