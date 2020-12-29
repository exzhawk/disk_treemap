# -*- encoding: utf-8 -*-
# Author: Epix
import os

from tqdm import tqdm


def scan(top_path):
    prefix_len = len(top_path.rstrip(os.sep)) + 1
    if os.name == 'nt':
        if ':' in top_path:
            prefix_len -= 1  # backslash after drive letter and colon is missing under windows

    for root, dirs, filenames in os.walk(top_path):
        try:
            for filename in filenames:
                file_path = os.path.join(root, filename)
                yield file_path[prefix_len:], os.path.getsize(file_path)
        except (FileNotFoundError, PermissionError, OSError):
            pass


def scan_size_tree(root_path):
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
