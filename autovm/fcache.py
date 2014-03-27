'''
Created on Mar 13, 2014

@author: francis
'''

from os.path import join, isdir, exists, dirname
from os import makedirs, unlink, stat
from autovm.helpers import Walker, DeleteWalkerVisitor, CountWalkerVisitor, EntriesWalkerVisitor
from autovm.helpers import LRUWalkerVisitor, touch
from autovm.helpers import null_progress, copyfileobj_progress
from threading import Lock
import urllib2
import base64

class AbstractFileProvider(object):
    def fetch(self, name):
        'returns the path to the requested file'
        pass
    def get_path(self, name):
        pass

class LocalFileProvider(AbstractFileProvider):
    def __init__(self, path):
        self.path = path
    def fetch(self, name):
        'returns the local path of the requested file'
        p = join(self.path, name)
        f = open(p, "rb")
        s = stat(p).st_size
        return (f, s)
    def get_path(self, name):
        return name

class HTTPFileProvider(AbstractFileProvider):
    def __init__(self, domain, basic_auth_username=None,
                 basic_auth_password=None):
        self.domain = domain
        self.username = basic_auth_username
        self.password = basic_auth_password
    def fetch(self, name):
        url = "http://%s/%s" % (self.domain, name)
        req = urllib2.Request(url, None)
        
        if self.username is not None and self.password is not None:
            base64string = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
            authheader =  "Basic %s" % base64string
            req.add_header("Authorization", authheader)
        r = urllib2.urlopen(req)
        size = int(r.info()['Content-Length'])
        return (r, size)
    def get_path(self, name):
        return "%s/%s" % (self.domain, name)
        
class FileCache(object):
    '''
    Maintain LRU file cache
    
    User of this class only needs to request files,
    they are added to the cache if not available, 
    or returned immediately if existing
    
    Works on the file system level, allowing to maintain big files
    '''
    lock = Lock()
       
    def __init__(self, cache, provider=None, max_size=100):
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
        
        self.max_size = max_size
        self.hit = self.miss = 0
    
    def get_file(self, name, force=False, progress=null_progress):
        with FileCache.lock:
            'get the required file'
            path = self.provider.get_path(name)
            target = join(self.cache, path)
            if exists(target) and not force:
                touch(target)
                self.hit += 1
                return target
            self.miss += 1
            (src, size) = self.provider.fetch(name)
            if not exists(dirname(target)):
                makedirs(dirname(target))
            try:
                with open(target, "wb") as dst:
                    copyfileobj_progress(src, dst, size, progress=progress)
            except KeyboardInterrupt:
                src.close()
                unlink(target)
                raise
            src.close()
            return target
    
    def has_file(self, name):
        'check if file exists in the cache'
        with FileCache.lock:
            path = self.provider.get_path(name)
            return exists(join(self.cache, path))
    
    def entries(self):
        'list entries in the cache, returns a list of paths'
        with FileCache.lock:
            w = Walker()
            e = EntriesWalkerVisitor()
            w.process(self.cache, e)
            return e.entries
            
    def clear(self):
        'remove all cache entries'
        # don't use shutils.rmtree() here, we want to keep the top-level directory
        with FileCache.lock:
            w = Walker()
            w.process(self.cache, DeleteWalkerVisitor())
    
    def count(self):
        'returns current number of files in the cache'
        with FileCache.lock:
            w = Walker()
            c = CountWalkerVisitor()
            w.process(self.cache, c)
            return c.files
    
    def cleanup(self):
        with FileCache.lock:
            entries = self._lru_entries(self.max_size)
            for e in entries:
                unlink(e.path)
    
    def _lru_entries(self, max_entries):
        'perform LRU based on modification time'
        w = Walker()
        lru = LRUWalkerVisitor(max_entries)
        w.process(self.cache, lru)
        return lru.get_entries()