#!/usr/bin/env python

import argparse
import sys
import os.path
import json
from openvpn_status import parse_status
import time

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')


def create_cli():
    parser = argparse.ArgumentParser(description='Openvpn client zabbix exporter')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l', '--lld', action='store_true',
                        help='export information for Zabbix LLD')
    group.add_argument('-m', '--metric', action='store_true',
                        help='export metric information by openvpn user id')
    parser.add_argument('-i', '--id', type=str, required=('--metric' in sys.argv or '-m' in sys.argv),
                        help='openvpn user id')
    parser.add_argument('-f', '--file', required=True,
                        help="input file with openvpn status", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    return parser


def main():
    parser = create_cli()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    try:
        status = parse_status(args.file.read())
    except:
        print('Error parsing openvpn status file')
        sys.exit()

    if args.lld:
        lld = {'data': []}
        for key, value in status.client_list.items():
            lld['data'].append({'{#CLIENT_ID}': value.common_name})
        print(json.dumps(lld))

    elif args.metric:
        for key, value in status.client_list.items():
            if value.common_name == args.id:
                args.id = key
        if args.id in status.client_list:
            peer_bytes_received = status.client_list[args.id].bytes_received
            peer_bytes_sent = status.client_list[args.id].bytes_sent
            peer_connected_since = status.client_list[args.id].connected_since
            metric = {'bytes_received': peer_bytes_received,
                      'bytes_sent': peer_bytes_sent,
                      'connected_since': int(time.mktime(peer_connected_since.timetuple()))
                      }
            print(json.dumps(metric))
        else:
            print('Peer with ID {} not found'.format(args.id))
            sys.exit()


if __name__ == '__main__':
    main()
