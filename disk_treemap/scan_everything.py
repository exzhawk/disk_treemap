# -*- encoding: utf-8 -*-
# Author: Epix
import ctypes
import os
from pathlib import Path, PureWindowsPath

from tqdm import tqdm

# copied from https://www.voidtools.com/support/everything/sdk/python/

# defines
EVERYTHING_REQUEST_FILE_NAME = 0x00000001
EVERYTHING_REQUEST_PATH = 0x00000002
EVERYTHING_REQUEST_SIZE = 0x00000010
EVERYTHING_REQUEST_ATTRIBUTES = 0x00000100

# dll imports
try:
    everything_dll = ctypes.WinDLL(str(Path(__file__).parent.resolve() / "Everything64.dll"))
except:
    raise RuntimeError('Load DLL failed. Only Windows x64 is supported')
everything_dll.Everything_GetResultSize.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_ulonglong)]
everything_dll.Everything_GetResultFileNameW.argtypes = [ctypes.c_int]
everything_dll.Everything_GetResultFileNameW.restype = ctypes.c_wchar_p


def scan(top_path):
    prefix_len = len(top_path.rstrip(os.sep)) + 1
    if os.name == 'nt':
        if ':' in top_path:
            prefix_len -= 1  # backslash after drive letter and colon is missing under windows

    # setup search
    everything_dll.Everything_SetSearchW(f'"{top_path}"')
    everything_dll.Everything_SetRequestFlags(
        EVERYTHING_REQUEST_FILE_NAME | EVERYTHING_REQUEST_PATH | EVERYTHING_REQUEST_SIZE)

    # execute the query
    everything_dll.Everything_QueryW(1)

    # get the number of results
    num_results = everything_dll.Everything_GetNumResults()

    # create buffers
    filename = ctypes.create_unicode_buffer(260)
    file_size = ctypes.c_ulonglong(1)

    directory_size = 2 ** 64 - 1

    # show results
    for i in range(num_results):
        everything_dll.Everything_GetResultFullPathNameW(i, filename, 260)
        everything_dll.Everything_GetResultSize(i, file_size)
        if file_size.value == directory_size: # no way to judge if it's a directory
            continue
        yield ctypes.wstring_at(filename)[prefix_len:], file_size.value


def scan_size_tree(root_path):
    root_path = str(PureWindowsPath(Path(root_path).absolute()))
    size_tree = dict()
    for path, size in tqdm(scan(root_path), desc=root_path):
        *directories, filename = path.lstrip(os.sep).split(os.sep)
        directories.insert(0, root_path)
        current_size_tree = size_tree
        for directory in directories:
            if directory not in current_size_tree:
                current_size_tree[directory] = dict()
            current_size_tree = current_size_tree[directory]
        current_size_tree[filename] = size
    return size_tree
