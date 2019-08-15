from setuptools import setup
import glob, re, os

## get documentation from README.md
with open("README.md", "r") as fh:
    long_description = fh.read()

## get version from spec file
with open('fnal-snow-python.spec', 'r') as fh:
    for line in fh:
        m = re.search("^Version:\s+(.*)\s*$", line)
        if m:
            version=m.group(1)
            break

## get list of files to install
pyfiles = glob.glob(os.path.join('*', '*.py'))
pyfiles = [pyfile[:-3] for pyfile in pyfiles]

scripts = glob.glob(os.path.join('usr/sbin/*'))
man     = glob.glob(os.path.join('man/man1/*'))

setup (
  author_email = 'tskirvin@fnal.gov',
  author = 'Tim Skirvin',
  data_files = [ ( 'share/man/man1', man ) ],
  description = 'SNOW JSON API access',
  license = 'Perl Artistic',
  install_requires = ['pysnow>=0.7.4', 'PyYAML>=3.11'],
  keywords = ['snow', 'service-now'],
  long_description_content_type = 'text/markdown',
  long_description = long_description,
  maintainer_email = 'tskirvin@fnal.gov',
  maintainer = 'Tim Skirvin',
  name = 'pyfnalsnow',
  package_dir = { 'pyfnalsnow': 'pyfnalsnow' },
  py_modules = pyfiles,
  scripts = scripts,
  url = 'https://github.com/tskirvin/pyfnalsnow.git',
  version = version
)
