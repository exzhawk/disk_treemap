# disk_treemap

Just another disk usage analyzer with treemap GUI.

## Pros

* Written in Python. Easy to run, modify and extend. Cross platform support. (Tested on Linux, Windows, and Android with
  Termux.)
* B/S structure. You can run the scanner on a remote machine, and view treemap via a browser on a local machine
* Support save/load a treemap. You can run the scanner on a machine, then copy result to another one and view it.

## Cons

* The web base frontend may suffering performance issue if the treemap is too large.
* Scan speed is not ideal, especially on Windows.

# Installation

## Install via pip package installer

```shell
pip install disk_treemap
```

## Build and install from source

TODO finish build steps
```shell
# clone the repository
git clone 
git submodules update --recursively
# build static
python3 setup.py build_static

#build wheel
python3 setup.py bdist_wheel
#install built wheel 
pip install dist/disk_treemap-1.0.0-py3-none-any.whl # change the filename
```

# Usage

```
usage: disk-treemap [-h] [--size_tree_path SIZE_TREE_PATH] [--overwrite]
               [--scan_only] [--host HOST] [--port PORT] [--compression]
               [--static_path STATIC_PATH]
               paths [paths ...]

positional arguments:
  paths                 path(s) to scan. if multiple paths is provided, they
                        will be show in root side by side

optional arguments:
  -h, --help            show this help message and exit
  --size_tree_path SIZE_TREE_PATH
                        path to save scan result as a JSON file
  --overwrite           overwrite existed JSON file. default to False
  --scan_only           scan and save JSON file but do not start web server.
                        default to False
  --host HOST           listening host of the web server
  --port PORT           listening port of the web server. default to 8000
  --compression         enable compression of web server. require
                        flask_compress to operate. default to False
```

A `size_tree.json` will be generated in the current directory. It contains file tree and file size information. Keep it
safe!

# Typical Usage

**Analyze an ordinary computer**

1. Run `disk-treemap <Paths to analyze>`
1. After `listening 127.0.0.1:8000` appearing, open browser and navigate to http://127.0.0.1:8000 .

**Analyze a remote Linux server, view on the local machine**

1. Run `disk-treemap <Paths to analyze> --host 0.0.0.0`.

   If bandwidth between the server and the local machine is limited, try to install `
1. After `listening 0.0.0.0:8000` appearing, open browser on the local machine and navigate to http:
   //<IP address of the server>:8000 .

**Analyze a remote Linux server without external accessible IP, view on the local machine**

1. Run `disk-treemap <Paths to analyze> --scan_only`
1. After process exit without error. There should be a file named `size_tree.json` in the current directory. Copy the
   file to local machine using `rsync` or other tools.
1. Run `disk-treemap` in the directory where the copied file located.
1. After `listening 127.0.0.1:8000` appearing, open browser and navigate to http://127.0.0.1:8000 .

**Install and analyze an Android phone with Termux**

1. Install Termux https://termux.com/
1. Install Python and pip in Termux https://wiki.termux.com/wiki/Python
1. Install disk_treemap via pip: `pip install termux`

# TODO

* Provide more visualization. Icicle/flame, sunburst maybe.
* Use NTFS USN Journal to speed up scanning on Windows.