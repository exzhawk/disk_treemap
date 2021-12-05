# -*- coding: utf-8 -*-
# Author: Epix
from functools import lru_cache

import boto3
from tqdm import tqdm


@lru_cache(maxsize=1)
def get_s3_client2(endpoint_url):
    return boto3.client('s3', endpoint_url=endpoint_url)


def walk_with_size(s3_url, endpoint_url):
    s3_url = s3_url + '/'
    bucket, prefix = s3_url[5:].split('/', 1)
    s3_client = get_s3_client2(endpoint_url)
    paginator = s3_client.get_paginator('list_objects_v2')
    response_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix)
    for response in response_iterator:
        yield [(f['Key'], f['Size']) for f in response.get('Contents', ())]


def scan(top_path, endpoint_url):
    for files in walk_with_size(top_path, endpoint_url):
        for filename, size in files:
            yield filename, size


def scan_size_tree(root_path, endpoint_url):
    object_prefix_same = set()
    size_tree = dict()
    for path, size in tqdm(scan(root_path, endpoint_url), desc=root_path):
        *directories, filename = path.lstrip('/').split('/')
        directories.insert(0, root_path)
        current_size_tree = size_tree
        skip_flag = False
        for index, directory in enumerate(directories):
            if isinstance(current_size_tree, int):
                same_path = '/'.join(directories[:index])
                if same_path not in object_prefix_same:
                    object_prefix_same.add(same_path)
                    tqdm.write('s3 path: {} is both object and prefix'.format(same_path))
                skip_flag = True
                break
            if directory not in current_size_tree:
                current_size_tree[directory] = dict()
            current_size_tree = current_size_tree[directory]
        if skip_flag:
            continue
        if isinstance(current_size_tree, int):
            same_path = '/'.join(directories)
            if same_path not in object_prefix_same:
                object_prefix_same.add(same_path)
                tqdm.write('s3 path: {} is both object and prefix'.format(same_path))
            continue
        current_size_tree[filename] = size
    return size_tree
