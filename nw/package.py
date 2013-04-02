#!/usr/bin/env python
import os
import subprocess
import shutil
import re

from nw import nwfiles
from nw import getnwfromnet
from nw import getlatestversion
from nw import is_win, is_darwin, is_linux, is_cygwin


_DIR_FOR_APP = 'nw-packaged-app'
_DIR_FOR_EXEC = 'exec-app'

ignore_dirs = [
  _DIR_FOR_APP,
]

def CheckVer(ver):
  match = '\d*.\d*.\d*'
  if re.match(match, ver):
    return True
  
  else:
    print 'The format of version %s is not corrent.' % (ver)
    return False  


def MakeZip():
  """ compress the source code """
  
  tmp_cwd = os.getcwd()
  os.chdir(options['path_to_app_src'])
  
  app_name = options['app_name']
  top = '.'
  tmp_app_path = os.path.join(options['path_for_package'], app_name)
  
  print 'Begin to compress app.'
  """ copy files """
  if os.path.isdir(tmp_app_path):
    shutil.rmtree(tmp_app_path)
    
  os.mkdir(tmp_app_path)  
  for name in os.listdir(top):
    if not name in ignore_dirs:
      if os.path.isfile(name):
        shutil.copy(name, os.path.join(tmp_app_path, name))
      else:
        shutil.copytree(name, os.path.join(tmp_app_path, name))
  """"""
  
  app_zip_path = os.path.join(options['path_for_package'], app_name)
  if os.path.isfile(app_zip_path + '.nw'):
    os.remove(app_zip_path + '.nw')
  

  shutil.make_archive(app_zip_path, 'zip', tmp_app_path) 
       
  print 'Compressing app ends.'

  shutil.rmtree(tmp_app_path)
  shutil.move(app_zip_path + '.zip', app_zip_path + '.nw')
  os.chdir(tmp_cwd)
  

def GenerateExecutableApp(nw_path, target):
  exec_app_path = options['path_for_exec_app'] + nwfiles.GetPlatformArch(target)
  package_path = options['path_for_package']
  app_tar_name = options['app_name'] + '.nw'
  #make directory
  if os.path.isdir(exec_app_path):
    shutil.rmtree(exec_app_path)
  os.mkdir(exec_app_path)

    
  print "package app with node-webkit"
  
  """ copy nw binaries files """
  for file in nwfiles.REQUIRE_FILES_FOR_APP[target]:
    src = os.path.join(nw_path, file)
    dst = os.path.join(exec_app_path, file)
    if os.path.isfile(src):
        shutil.copy(src, dst)
    else:
        shutil.copytree(src, dst)
  
  
  if nwfiles.GetPlatformName(target) == nwfiles.PLATFORMNAMEMAC:
    shutil.copy(os.path.join(package_path, app_tar_name),
                os.path.join(exec_app_path, 
                             'node-webkit.app',
                             'Contents',
                             'Resources',
                             app_tar_name))
  else:
    shutil.copy(os.path.join(package_path, app_tar_name),
                os.path.join(exec_app_path, app_tar_name))
  
  
  tmp_cwd = os.getcwd()
  os.chdir(exec_app_path)
  if is_cygwin or is_linux or is_darwin:
    if nwfiles.GetPlatformName(target) == nwfiles.PLATFORMNAMELINUX:
      subprocess.call('cat nw %s > app && chmod +x app' % (app_tar_name),
                      shell=True)
    if nwfiles.GetPlatformName(target) == nwfiles.PLATFORMNAMEWIN:
      subprocess.call('cat nw.exe %s > app.exe && chmod +x app.exe' % (app_tar_name)
                      , shell=True)
  elif is_win:
    if nwfiles.GetPlatformName(target) == nwfiles.PLATFORMNAMELINUX:
      subprocess.call('copy /b nw+%s app' % (app_tar_name), shell=True)
    if nwfiles.GetPlatformName(target) == nwfiles.PLATFORMNAMEWIN:
      subprocess.call('copy /b nw.exe+%s app.exe' % (app_tar_name), shell=True)
  
  
  if nwfiles.GetPlatformName(target) == nwfiles.PLATFORMNAMELINUX:
    os.remove('nw')
  if nwfiles.GetPlatformName(target) == nwfiles.PLATFORMNAMEWIN:
    os.remove('nw.exe')
    
  if os.path.isfile(app_tar_name):
    os.remove(app_tar_name)
  
  os.chdir(tmp_cwd)  
  

def CheckNwFiles(target):
  """
    --nw-path and --nw-ver, most one can be set.
    if --nw-path is set, use this nw'binrary and don't download from web.
    if --nw-ver, download this version's node-webkit.
    if both not, download the latest node-webkit.
  """
  _is_download_ = False 
  if not options.has_key('path_to_nw'):
    _is_download_ = True
  else:
    nw_path = options['path_to_nw']
  
  nw_ver = ''
  if options.has_key('nw_version'): 
    nw_ver = options['nw_version']
  elif _is_download_:
    nw_ver = options['latest_version']
  
  #download file
  if nw_ver != '':
    nw_path = getnwfromnet.GetNwFromNet(nw_ver, target)  
  
  #print options['path_to_nw']
  if not nwfiles.CheckNwFiles(nw_path, target):
    print 'files are not completed.'
    return None
  
  return nw_path


def PackageApp(targets):
  #make directory
  if not os.path.isdir(options['path_for_package']):
    os.mkdir(options['path_for_package'])    
  MakeZip()
  
  """ get node-webkit version """
  options['latest_version'] = getlatestversion.latestVersion()
  
  for t in targets:
    nw_path = CheckNwFiles(t)
    if not nw_path:
      continue  
    GenerateExecutableApp(nw_path, t)
  

def __add_argument(parser):
  parser.add_argument("app_path",
                      help="app path") 
  
  group = parser.add_mutually_exclusive_group()
  group.add_argument("--nw-path",
                      help="path to nw files")
  group.add_argument("--nw-ver",
                      help="the download version of node-webkit")


  
def main(app_path, nw_path, nw_ver, **kw):  
 
  targets = set()
  
  """ generate target list """
  nwfiles.GetTargetList(targets, kw)

  global options
  options = {
    'path_to_app_src': '',
    'path_for_package': "",
    'path_for_exec_app': '',
    'app_name': '',    
  }
  options['path_to_app_src'] = os.path.abspath(app_path)
  options['path_for_package'] = os.path.join(options['path_to_app_src'], _DIR_FOR_APP)
  options['path_for_exec_app'] = os.path.join(options['path_for_package'], _DIR_FOR_EXEC)
  options['app_name'] = os.path.basename(options['path_to_app_src'])
  
  path_to_app = options['path_to_app_src']
  
  if not os.path.isdir(path_to_app):
    print 'no such directory: %s' % (path_to_app)
    return
  
  if nw_path:
    options['path_to_nw'] = nw_path
  if nw_ver:
    options['nw_version'] = nw_ver
    if not CheckVer(nw_ver):
      return  
        
  PackageApp(targets)
