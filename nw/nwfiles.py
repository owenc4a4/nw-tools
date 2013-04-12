import sys
import os

is_py27 = sys.version_info >= (2, 7)

is_win = sys.platform.startswith('win')
is_cygwin = sys.platform == 'cygwin'
is_darwin = sys.platform == 'darwin'  # Mac OS X

is_win = is_win or is_cygwin
# Unix platforms
is_linux = sys.platform.startswith('linux')

PLATFORMNAMEWIN = 'win'
PLATFORMNAMEMAC = 'osx'
PLATFORMNAMELINUX = 'linux'

# get platform information
if is_linux:
  platform_name = 'linux'

if is_cygwin or is_win:
  platform_name = 'win'

if is_darwin:
  platform_name = 'osx'


""" target option index  """
_TARGET_SELF = 0
_TARGET_WIN = 1
_TARGET_MAC = 2
_TARGET_LINUX32 = 3
_TARGET_LINUX64 = 4

_TARGET_OPTION = {
  _TARGET_WIN : 'WIN',
  _TARGET_MAC: 'MAC',
  _TARGET_LINUX32: 'LINUX32',
  _TARGET_LINUX64: 'LINUX64',
}

""" platform name list by target  """
_PLATFORM_NAME = {
  _TARGET_SELF: '',
  _TARGET_WIN: 'win',
  _TARGET_MAC: 'osx',
  _TARGET_LINUX32: 'linux',
  _TARGET_LINUX64: 'linux',
}
_PLATFORM_NAME[_TARGET_SELF] = platform_name

""" tar name list by target  """
_TARNAME_END = {
  _TARGET_SELF: '',
  _TARGET_WIN: '-win-ia32.zip',
  _TARGET_MAC: '-osx-ia32.zip',
  _TARGET_LINUX32: '-linux-ia32.tar.gz',
  _TARGET_LINUX64: '-linux-x64.tar.gz',
}

def _GetSelfTarName():
  import platform
  bits = platform.architecture()[0]
  if bits == '64bit':
    arch = 'x64'
  else:
    arch = 'ia32'

  if is_win or is_darwin:
    arch = 'ia32'

  binary_name = '-' + platform_name + '-' + arch
  binary_tar = binary_name + '.tar.gz'

  # use zip in mac and windows
  if is_win or is_darwin:
    binary_tar = binary_name + '.zip'
  return binary_tar

_TARNAME_END[_TARGET_SELF] = _GetSelfTarName()

""" require files by target """

# linux
required_file_linux = (
  'nw',
  'nw.pak',
  'libffmpegsumo.so',
)
required_dev_file_linux = (
  'nwsnapshot',
)

# win
required_file_win = (
  'ffmpegsumo.dll',
  'icudt.dll',
  'libEGL.dll',
  'libGLESv2.dll',
  'nw.exe',
  'nw.pak',
)
required_dev_file_win = (
  'nwsnapshot.exe',
)

# mac
required_file_mac = (
  'node-webkit.app',
)
required_dev_file_mac = (
 'nwsnapshot',
)

if is_linux:
  required_file_for_app = required_file_linux
  required_file = required_file_linux + required_dev_file_linux

if is_win:
  required_file_for_app = required_file_win
  required_file = required_file_win + required_dev_file_win

if is_darwin:
  required_file_for_app = required_file_mac
  required_file = required_file_mac + required_dev_file_mac

REQUIRE_FILES = {
  _TARGET_SELF: required_file,
  _TARGET_WIN: required_file_win + required_dev_file_win,
  _TARGET_LINUX32: required_file_linux + required_dev_file_linux,
  _TARGET_LINUX64: required_file_linux + required_dev_file_linux,
  _TARGET_MAC: required_file_mac + required_dev_file_mac,
}

REQUIRE_FILES_FOR_APP = {
  _TARGET_SELF: required_file_for_app,
  _TARGET_WIN: required_file_win,
  _TARGET_LINUX32: required_file_linux,
  _TARGET_LINUX64: required_file_linux,
  _TARGET_MAC: required_file_mac,
}


def GetPlatformName(target=_TARGET_SELF):
  return _PLATFORM_NAME[target]

def GetNwTarName(ver, target=_TARGET_SELF):
  tarname = 'node-webkit-v' + ver
  binary_tar = tarname + _TARNAME_END[target]
  return binary_tar

def GetNwName(ver, target=_TARGET_SELF):
  tarend = _TARNAME_END[target]
  tarname = 'node-webkit-v' + ver + tarend[:tarend.find('.')]
  return tarname

def GetPlatformArch(target=_TARGET_SELF):
  tarend = _TARNAME_END[target]
  return tarend[:tarend.find('.')]

def CheckNwFiles(path, target=_TARGET_SELF):
  """
     check whether the path have all files.
  """
  if not os.path.isdir(path):
    return False

  file_list = os.listdir(path)
  for file in REQUIRE_FILES_FOR_APP[target]:
    if not file in file_list:
      return False

  return True

def GetTargetList(targets, kw):
  has_one = False
  if kw['all']:
    for target in _TARGET_OPTION:
      targets.add(target)
    has_one = True
  for target in _TARGET_OPTION:
    if kw[_TARGET_OPTION[target]]:
      targets.add(target)
      has_one = True

  if not has_one:
    targets.add(_TARGET_SELF)

def __add_argument(parser):
  g = parser.add_argument_group('target platform', 'target platform to be packaged')
  g.add_argument("--all",
                 help='all platform',
                 action='store_true')

  for target in _TARGET_OPTION:
    g.add_argument("--%s" % (_TARGET_OPTION[target]),
                   action='store_const',
                   const=target)
