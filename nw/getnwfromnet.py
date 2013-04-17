import os
import shutil
import urllib2
import zipfile
import tarfile

from nw import nwfiles
from nw import NWTMPDIR, is_win, is_darwin, is_linux, s3_node_webkit_url

from nw.download import DownloadFile


def GetPermission(zip, dst):
  # build the destination pathname, replacing
  # forward slashes to platform specific separators.
  # Strip trailing path separator, unless it represents the root.
  if (dst[-1:] in (os.path.sep, os.path.altsep)
      and len(os.path.splitdrive(dst)[1]) > 1):
    dst = dst[:-1]

  members = zip.infolist()
  for member in members:
    targetpath = dst
    # don't include leading "/" from file name if present
    if member.filename[0] == '/':
      targetpath = os.path.join(targetpath, member.filename[1:])
    else:
      targetpath = os.path.join(targetpath, member.filename)

    targetpath = os.path.normpath(targetpath)
    if os.path.isfile(targetpath):
      mode = member.external_attr >> 16 & 0x1FF
      os.chmod(targetpath, mode)

def GetUrl(nw_name):
  base_url = s3_node_webkit_url
  f = urllib2.urlopen(base_url)
  import xml.etree.ElementTree as ET
  tree = ET.parse(f)
  root = tree.getroot()

  for child in root:
    if child.tag.find('Contents') != -1 and child[0].text.find(nw_name) != -1:
      return base_url + child[0].text

def GetNwFromNet(ver, target, keep=False):
  path_ = NWTMPDIR
  if not os.path.isdir(path_):
    os.mkdir(path_)

  nw_name_ = nwfiles.GetNwTarName(ver, target)
  update_path_ = os.path.join(path_, 'updates')
  nw_tar_path_ = os.path.join(update_path_, nw_name_)
  nw_path_ = os.path.join(update_path_, nwfiles.GetNwName(ver, target))

  #print 'nw:', nw_name_
  #print nw_tar_path_

  # check nw files
  if nwfiles.CheckNwFiles(nw_path_, target):
    return nw_path_

  # download
  url = GetUrl(nwfiles.GetNwName(ver, target))
  if not DownloadFile(url, nw_tar_path_):
    return None

  # uncompress
  target_platfrom = nwfiles.GetPlatformName(target)
  if target_platfrom == nwfiles.PLATFORMNAMELINUX:
    tar = tarfile.open(nw_tar_path_)
    nw_path_ = os.path.join(update_path_, tar.getnames()[0])
    if os.path.isdir(nw_path_):
      shutil.rmtree(nw_path_)
    tar.extractall(update_path_)
    tar.close()

  if target_platfrom == nwfiles.PLATFORMNAMEWIN:
    zip = zipfile.ZipFile(nw_tar_path_, 'r')
    file_name = os.path.dirname(zip.namelist()[0])
    nw_path_ = os.path.join(update_path_, file_name)
    if os.path.isdir(nw_path_):
      shutil.rmtree(nw_path_)
    zip.extractall(update_path_)
    GetPermission(zip, update_path_)
    zip.close()

  if target_platfrom == nwfiles.PLATFORMNAMEMAC:
    zip = zipfile.ZipFile(nw_tar_path_, 'r')
    if os.path.isdir(nw_path_):
      shutil.rmtree(nw_path_)
    zip.extractall(nw_path_)
    GetPermission(zip, nw_path_)
    zip.close()

  if not keep:
    # delete compress file
    os.remove(nw_tar_path_)

  return nw_path_
