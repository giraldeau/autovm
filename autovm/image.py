'''
Created on Mar 27, 2014

@author: francis
'''

from fcache import HTTPFileProvider, FileCache
from os.path import expanduser
from helpers import default_arch, default_dist, null_progress

class UbuntuImageCache(object):
    '''
    Ubuntu VM image
    '''
    default_domain = 'cloud-images.ubuntu.com'
    path = '%(dist)s/current/%(dist)s-server-cloudimg-%(arch)s-disk1.img'
    cache_dir = '~/.cache/autovm'
    def __init__(self, domain=default_domain):
        provider = HTTPFileProvider(domain)
        self.file_cache = FileCache(expanduser(UbuntuImageCache.cache_dir), provider)
    def get_default_image(self):
        return self.get_image(default_dist(), default_arch())
    def _image_name(self, dist, arch):
        return UbuntuImageCache.path % {'dist': dist, 'arch': arch}
    def get_image(self, dist, arch, force=False, progress=null_progress):
        return self.file_cache.get_file(self._image_name(dist, arch), force, progress)
    def has_image(self, dist, arch):
        return self.file_cache.has_file(self._image_name(dist, arch))