__all__ = ('NWTMPDIR',
           'VERSION', 'get_version',
           'is_win', 'is_cygwin', 'is_darwin', 'is_linux', 
           'is_py27')

import os

from nw import nwfiles

VERSION = (0, 0, 1)

is_py27 = nwfiles.is_py27


is_win = nwfiles.is_win
is_cygwin = nwfiles.is_cygwin
is_darwin = nwfiles.is_darwin

is_linux = nwfiles.is_linux

if is_win:
  NWTMPDIR = os.environ.get('LOCALAPPDATA')
  if not NWTMPDIR:
    NWTMPDIR = os.path.expanduser('~\\Documents')
elif is_darwin:
  NWTMPDIR = os.path.expanduser('~/Library/Application Support')
else:
  NWTMPDIR = os.environ.get('XDG_DATA_HOME')
  if not NWTMPDIR:
    NWTMPDIR = os.path.expanduser('~/.config')    

if is_cygwin:
  NWTMPDIR = os.path.normcase(NWTMPDIR)
  
NWTMPDIR = os.path.join(NWTMPDIR, 'node-webkit')

def get_version():
  version = '%s.%s' % (VERSION[0], VERSION[1])
  if VERSION[2]:
      version = '%s.%s' % (version, VERSION[2])
  if len(VERSION) >= 4 and VERSION[3]:
      version = '%s%s' % (version, VERSION[3])
      # include git revision in version string
      if VERSION[3] == 'dev' and VERSION[4] > 0:
          version = '%s-%s' % (version, VERSION[4])
  return version
