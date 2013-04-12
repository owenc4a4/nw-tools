## Introduction

A tool for packaging apps based on node-webkit.

Prerequisites:
* [Python][windows-python] ([`v2.7.3`][windows-python-v2.7.3], `v3.x.x` is not supported)

### Features

* Detect and download newest binaries.
* Automatically make packages for all platforms.

## How to Use

To package app with the newest node-webkit binary.

```` bash
$ python nw_package_tool path-to-app
````

Also package app for all platform.

```` bash
$ python nw_package_tool --all path-to-app
````

Now you have your packages! The packages end up in `nw-packaged-app`. At this point you can run your app!

## Command line options

```` bash
$ python nw_package_tool --help
  usage: nw_package_tool [options] app_path

  positional arguments:
    app_path           path to the application that been packaged

  optional arguments:
    -h, --help         show this help message and exit

  exclusive options:
    As for following options, at most one can be set

    --nw-path NW_PATH  path to nw binary files that to be packaged with
    --nw-ver NW_VER    the stable version of node-webkit to be download

  target platform:
    target platform to be packaged

    --all              all platform
    --WIN
    --MAC
    --LINUX32
    --LINUX64

````

[windows-python]: http://www.python.org/getit/windows
[windows-python-v2.7.3]: http://www.python.org/download/releases/2.7.3#download
