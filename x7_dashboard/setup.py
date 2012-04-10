#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4

#    Vms Manage
#    Copyright (C) GridDynamics X7 Core Team, GridDynamics
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import gettext
import glob
import os
import subprocess
import sys

from setuptools import setup, find_packages, findall


setup(name='x7dashboard',
      version='0.0.1',
      license='GNU GPL v3',
      description='Django based interface for vms-manage',
      author='x7fan.king ( X7 Core Team, (c) vonbros.com)',
      author_email='vcfan.king@gmail.com',
      url='http://www.x7cloud.org',
      packages=find_packages(exclude=['bin', 'smoketests', 'tests']),
      package_data = {'x7tools':
                        [s[len('x7tools/'):] for s in
                         findall('x7tools/templates') \
                         + findall('x7tools/static') ]},
      py_modules=[],
      test_suite='tests'
)

