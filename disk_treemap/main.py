# -*- encoding: utf-8 -*-
# Author: Epix
import argparse
import json
import os
import sys
from pathlib import Path

from flask import Flask, send_file, jsonify

from .scan_fs import scan_size_tree
from .scan_s3 import scan_size_tree_s3


def start_server(size_tree_file_path, host, port, compression):
    app = Flask(__name__)
    base_dir = Path(__file__).absolute().parent / 'static' / 'dist' / 'webapp'
    app.root_path = str(base_dir)
    if compression:
        from flask_compress import Compress
        Compress(app)

    @app.route('/')
    def index():
        return send_file('index.html')

    @app.route('/<path:path>')
    def static_files(path):
        return send_file(path)

    @app.route('/size_tree.json')
    def size_tree():
        return send_file(size_tree_file_path, cache_timeout=-1)

    @app.route('/info')
    def get_info():
        info = {
            'sep': os.path.sep
        }
        return jsonify(info)

    print('listening {}:{}'.format(host, port))
    app.run(host, port)


def scan_paths(root_paths, size_tree_file_path, args):
    all_size_tree = {}
    for root_path in root_paths:
        if root_path.startswith('s3://'):
            if root_path.endswith('/'):
                root_path = root_path[:-1]
            size_tree = scan_size_tree_s3(root_path, args.endpoint_url)
        else:
            root_path = str(Path(root_path))
            size_tree = scan_size_tree(root_path)
        all_size_tree.update(size_tree)
    with open(size_tree_file_path, 'w') as f:
        json.dump(all_size_tree, f)
    print('scanning complete.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('paths', nargs='*',
                        help='path(s) to scan. '
                             'If multiple paths is provided, they will be show in root side by side.'
                             'S3 or compatible object storage service is supported by using a "s3://" prefixed URI')
    parser.add_argument('--size-tree-path', '--size_tree_path', '-f', default='size_tree.json',
                        help='path to save scan result as a JSON file')
    parser.add_argument('--overwrite', '-o', action='store_true',
                        help='overwrite existed JSON file. default to False')
    parser.add_argument('--scan-only', '--scan_only', '-s', action='store_true',
                        help='scan and save JSON file but do not start web server. default to False')
    parser.add_argument('--host', '-H', default='127.0.0.1',
                        help='listening host of the web server')
    parser.add_argument('--port', '-p', default=8000, type=int,
                        help='listening port of the web server. default to 8000')
    parser.add_argument('--compression', '-c', action='store_true',
                        help='enable compression of web server. require flask_compress to operate. default to False')
    parser.add_argument('--endpoint-url', help='custom endpoint url, only affects S3')
    parser.add_argument('--follow-links', '--follow_links', action='store_true',
                        help='follow symlinks')
    parser.add_argument('--follow-mounts', '--follow_mounts', action='store_true',
                        help='follow mounts')
    args = parser.parse_args()
    root_paths = args.paths
    size_tree_file_path = os.path.abspath(args.size_tree_path)
    if os.path.exists(size_tree_file_path):
        if args.overwrite:
            scan_paths(root_paths, size_tree_file_path, args)
        else:
            print('{} exists. Skip scanning process.'.format(args.size_tree_path))
    else:
        if len(root_paths) == 0:
            print('nothing to scan and nothing to show. exiting.')
            return -1
        else:
            scan_paths(root_paths, size_tree_file_path, args)

    if not args.scan_only:
        start_server(size_tree_file_path=size_tree_file_path, host=args.host, port=args.port,
                     compression=args.compression)
    return 0


if __name__ == '__main__':
    sys.exit(main())
