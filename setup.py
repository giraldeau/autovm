#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages


setup(name='autovm',
      version='0.0.1',
      author='Francis Giraldeau',
      author_email='francis.giraldeau@mail.com',
      url='http://github.com',
      download_url='http://github.com/',
      description='Automate KVM virtual machine setup',
      long_description='Automate KVM virtual machine setup',

      packages = find_packages(),
      include_package_data = True,
      package_data = {
        '': ['*.txt', '*.rst'],
      },
      exclude_package_data = { '': ['README.txt'] },
      
      scripts = ['bin/autovm'],
      
      keywords='python tools utils internet www',
      license='GPL',
      classifiers=['Development Status :: 1 - Planning',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Topic :: System :: Clustering',
                  ],
                  
      #setup_requires = ['python-stdeb', 'fakeroot', 'python-all'],
      install_requires = ['setuptools'],
     )
