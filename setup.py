#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2017 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, 51 Franklin Street, Fifth Floor, Boston, MA 02110-1335, USA.
#
# Authors:
#     Santiago Dueñas <sduenas@bitergia.com>
#     Jesus M. Gonzalez-Barahona <jgb@gsyc.es>
#

import codecs
import os.path
import re
import sys
import unittest

from setuptools import setup, Command

here = os.path.abspath(os.path.dirname(__file__))
readme_md = os.path.join(here, 'README.md')
version_py = os.path.join(here, 'perceval', '_version.py')

# Pypi wants the description to be in reStrcuturedText, but
# we have it in Markdown. So, let's convert formats.
# Set up thinkgs so that if pypandoc is not installed, it
# just issues a warning.
try:
    import pypandoc
    long_description = pypandoc.convert(readme_md, 'rst')
except (IOError, ImportError):
    print("Warning: pypandoc module not found, or pandoc not installed. "
          "Using md instead of rst")
    with codecs.open(readme_md, encoding='utf-8') as f:
        long_description = f.read()

with codecs.open(version_py, 'r', encoding='utf-8') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)


class TestCommand(Command):

    user_options = []
    __dir__ = os.path.dirname(os.path.realpath(__file__))

    def initialize_options(self):
        os.chdir(os.path.join(self.__dir__, 'tests'))

    def finalize_options(self):
        pass

    def run(self):
        test_suite = unittest.TestLoader().discover('.', pattern='test_*.py')
        result = unittest.TextTestRunner(buffer=True).run(test_suite)
        sys.exit(not result.wasSuccessful())


cmdclass = {'test': TestCommand}

setup(name="perceval",
      description="Fetch data from software repositories",
      long_description=long_description,
      url="https://github.com/grimoirelab/perceval",
      version=version,
      author="Bitergia",
      author_email="sduenas@bitergia.com",
      license="GPLv3",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Topic :: Software Development',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Programming Language :: Python :: 3'
      ],
      keywords="development repositories analytics git github bugzilla jira jenkins",
      packages=[
          'perceval',
          'perceval.backends',
          'perceval.backends.core'
      ],
      namespaces=[
          'perceval.backends'
      ],
      install_requires=[
          'python-dateutil>=2.6.0',
          'requests>=2.7.0',
          'beautifulsoup4>=4.3.2',
          'feedparser>=5.1.3',
          'dulwich>=0.18.5',
          'urllib3>=1.22',
          'grimoirelab-toolkit>=0.1.4'
      ],
      scripts=[
          'bin/perceval'
      ],
      cmdclass=cmdclass,
      zip_safe=False)
