#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import sys
from iconsdk.wallet.wallet import KeyWallet


def main():
    global args, fastpeer_domains
    parser = argparse.ArgumentParser(prog='icon_wallet')
    parser.add_argument('command', nargs='?', help='cat, tail', default="keystore")
    parser.add_argument('-p', '--password', type=str, help=f'keystore password', default=None)
    parser.add_argument('-f', '--filename', type=str, help=f'keystore filename', default="keystore.json")
    args = parser.parse_args()
    wallet = KeyWallet.create()
    if args.password is None:
        print("[ERROR] need a password")
        sys.exit(127)
    wallet.store(args.filename, args.password)
    print(f"store file={args.filename} / password={args.password}")


if __name__ == '__main__':
    main()
