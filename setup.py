from distutils.core import setup

import os
import glob

pyfiles = glob.glob(os.path.join('*', '*.py'))
pyfiles = [pyfile[:-3] for pyfile in pyfiles]

setup (
  name             = 'fnal-snow-python',
  version          = '1',
  description      = 'SNOW JSON API access',
  maintainer       = 'Tim Skirvin',
  maintainer_email = 'tskirvin@fnal.gov',
  package_dir      = { 'pyfnalsnow': 'pyfnalsnow' },
  py_modules       = pyfiles,
)
