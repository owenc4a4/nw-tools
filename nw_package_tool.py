#!/usr/bin/env python

import os
import argparse

import nw.package
import nw.nwfiles

from nw import is_py27

def __add_argument(parser):
  return


def main():

  parser = argparse.ArgumentParser(
      prog='nw_package_tool',
      usage='%(prog)s [options] app_path',
      )
  nw.package.__add_argument(parser)
  nw.nwfiles.__add_argument(parser)
  parser.add_argument_group()

  args = parser.parse_args()

  # print **args.__dict__
  if not is_py27:
    print 'Required python version is 2.7.3', 'Pelease update your python.'
    return

  nw.package.main(**args.__dict__)

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    raise SystemExit("Aborted by user request.")
