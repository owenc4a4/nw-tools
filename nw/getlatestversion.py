#!/usr/bin/env python

# get the latest version of node-webkit frome s3.amazonaw.com


import re
header_match = '[\s\S]*nw-headers-v\d*.\d*.\d*.tar.gz'
win_match = '[\s\S]*node-webkit-v\d*.\d*.\d*-win-ia32.zip'
mac_match = '[\s\S]*node-webkit-v\d*.\d*.\d*-osx-ia32.zip'
linux32_match = '[\s\S]*node-webkit-v\d*.\d*.\d*-linux-ia32.tar.gz'
linux64_match = '[\s\S]*node-webkit-v\d*.\d*.\d*-linux-x64.tar.gz'

_DEFAULT_VERSION = '0.4.0'
_HEAFERS = 0
_WIN = 1
_MAC = 2
_LINUX32 = 3
_LINUX64 = 4


matchs = [
  header_match,
  win_match,
  mac_match,
  linux32_match,
  linux64_match,
]

ver_before = [
  'nw-headers-v',
  'node-webkit-v',
  'node-webkit-v',
  'node-webkit-v',
  'node-webkit-v',
  'node-webkit-v',
]

ver_end = [
  '.tar.gz',
  '-win-ia32.zip',
  '-osx-ia32.zip',
  '-linux-ia32.tar.gz',
  '-linux-x64.tar.gz',
]



def MaxVersion(ver_a, ver_b):
  max_value = ver_b
  ver_a_values = []
  ver_b_values = []

  ver_a_values.append(ver_a[:ver_a.index('.')])
  ver_a_values.append(ver_a[ver_a.index('.') + 1: ver_a.rindex('.')])
  ver_a_values.append(ver_a[ver_a.rindex('.') + 1: len(ver_a)])

  ver_b_values.append(ver_b[:ver_b.index('.')])
  ver_b_values.append(ver_b[ver_b.index('.') + 1: ver_b.rindex('.')])
  ver_b_values.append(ver_b[ver_b.rindex('.') + 1: len(ver_b)])

  for i in range(3):
    if ver_a_values[i] > ver_b_values[i]:
      max_value = ver_a
    elif ver_a_values[i] == ver_b_values[i]:
      continue
    break

  return max_value



def GetVersion(str, index):
  begin = str.index(ver_before[index])
  end = str.index(ver_end[index])
  return str[begin + len(ver_before[index]): end]


def latestVersion():
  import urllib2
  f = urllib2.urlopen('https://s3.amazonaws.com/node-webkit/')

  import xml.etree.ElementTree as ET
  tree = ET.parse(f)
  root = tree.getroot()
  max_version = _DEFAULT_VERSION
  versions = {}

  # get all versions
  for child in root:
    if child.tag.find('Contents') != -1 and child[0].text.find('-pre') == -1:

      for match in matchs:
        if re.match(match, child[0].text):
          index = matchs.index(match)
          version = GetVersion(child[0].text, index)
          if versions.has_key(version):
            versions[version] += 1
          else :
            versions[version] = 1



  for ver in versions:
    if versions[ver] == len(matchs):
      max_version = MaxVersion(ver, max_version)

  return max_version

