'''
Created on Mar 13, 2014

@author: francis
'''

from os.path import join, isdir, exists
from os import makedirs
from shutil import copyfile, rmtree
from autovm.helpers import Walker, DeleteWalkerVisitor, CountWalkerVisitor

class AbstractFileProvider(object):
    def fetch(self, name):
        'returns the path to the requested file'
        pass
    def done(self, name):
        'called after the file is added to the cache'
        pass

class LocalFileProvider(AbstractFileProvider):
    def __init__(self, path):
        self.path = path
    def fetch(self, name):
        'returns the local path of the requested file'
        return join(self.path, name)

class HTTPFileProvider(AbstractFileProvider):
    def __init__(self, domain, basic_auth_username=None,
                 basic_auth_password=None):
        self.domain = domain
        self.basic_auth_username = basic_auth_username
        self.basic_auth_password = basic_auth_password
    def fetch(self, name):
        pass

class FileCache(object):
    '''
    Maintain LRU file cache
    
    User of this class only needs to request files,
    they are added to the cache if not available, 
    or returned immediately if existing
    
    Works on the file system level, allowing to maintain big files
    '''

    def __init__(self, cache, provider=None):
        # make sure the provider is set
        self.provider = provider
        if not self.provider:
            self.provider = AbstractFileProvider()
        self.cache = cache
        
        if exists(self.cache):
            if not isdir(self.cache):
                raise IOError("Cache directory is not a directory")
        else:
            makedirs(self.cache)
    
    def get_file(self, name):
        'get the required file'
        target = join(self.cache, name)
        if exists(target):
            return target
        source = self.provider.fetch(name)
        copyfile(source, target)
        self.provider.done(name)
        return target
    
    def has_file(self, name):
        'check if file exists in the cache'
        return exists(join(self.cache, name))
    
    def clear(self):
        'remove all cache entries'
        # don't use shutils.rmtree() here, we want to keep the top-level directory
        w = Walker()
        w.process(self.cache, DeleteWalkerVisitor())
    
    def count(self):
        'returns current number of files in the cache'
        w = Walker()
        c = CountWalkerVisitor()
        w.process(self.cache, c)
        return c.files
    
    def entries(self):
        'return all entries of the cache'
        pass
    
    def _lru_count(self):
        'perform LRU cleanup based on count'
        pass
    
    def _lru_size(self):
        'perform LRU cleanup based on size'
        pass