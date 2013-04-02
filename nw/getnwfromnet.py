import os
import shutil
import urllib2
import zipfile
import tarfile

from nw import nwfiles
from nw import NWTMPDIR, is_win, is_darwin, is_linux

from nw.download import DownloadFile


def GetNwFromNet(ver, target):
  path_ = NWTMPDIR
  if not os.path.isdir(path_):
    os.mkdir(path_)
    
  nw_name_ =  nwfiles.GetNwTarName(ver, target)
  nw_tar_path_ = os.path.join(path_, nw_name_)
  nw_path_ = os.path.join(path_, 
                          'updates', 
                          nwfiles.GetNwName(ver, target))
  
  url = 'https://s3.amazonaws.com/node-webkit/v%s/%s' % (ver, nw_name_)
  
  #print 'nw:', nw_name_
  #print nw_tar_path_
  
  #check nw files
  if nwfiles.CheckNwFiles(nw_path_, target):
    return nw_path_
   
  #download      
  DownloadFile(url, nw_tar_path_)
  
  #uncompress
  if os.path.isdir(nw_path_):
    shutil.rmtree(nw_path_)
  
  target_platfrom = nwfiles.GetPlatformName(target)
  
  if target_platfrom == nwfiles.PLATFORMNAMELINUX:
    tar = tarfile.open(nw_tar_path_)
    tar.extractall(path_)
    tar.close()

  if target_platfrom == nwfiles.PLATFORMNAMEWIN:
    zip = zipfile.ZipFile(nw_tar_path_, 'r')
    zip.extractall(path_)
    zip.close()
    
  if target_platfrom == nwfiles.PLATFORMNAMEMAC:
    zip = zipfile.ZipFile(nw_tar_path_, 'r')
    zip.extractall(nw_path_)
    zip.close()
       
  #delete compress file
  os.remove(nw_tar_path_)
  
  return nw_path_