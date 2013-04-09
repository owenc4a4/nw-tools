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

You can also get help by running:

```` bash
$ python nw_package_tool -h
````

[windows-python]: http://www.python.org/getit/windows
[windows-python-v2.7.3]: http://www.python.org/download/releases/2.7.3#download