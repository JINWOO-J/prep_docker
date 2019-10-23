#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import binascii
import hashlib
from asn1crypto import keys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from secp256k1 import PrivateKey
import sys, json
from iconsdk.wallet.wallet import KeyWallet


def is_json(jsonfile):
    try:
        json_object = json.loads(jsonfile)
    except ValueError as e:
        return False
    return True


def from_prikey_file(prikey_file: str, password):
    if isinstance(password, str):
        password = password.encode()

    if prikey_file.endswith('.der') or prikey_file.endswith('.pem'):
        with open(prikey_file, "rb") as file:
            private_bytes = file.read()
        try:
            if prikey_file.endswith('.der'):
                temp_private = serialization \
                    .load_der_private_key(private_bytes,
                                          password,
                                          default_backend())
            if prikey_file.endswith('.pem'):
                temp_private = serialization \
                    .load_pem_private_key(private_bytes,
                                          password,
                                          default_backend())
        except Exception as e:
            raise ValueError("Invalid Password or Certificate load Failure)")

        no_pass_private = temp_private.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        key_info = keys.PrivateKeyInfo.load(no_pass_private)

        val = key_info['private_key'].native['private_key']
        width = val.bit_length()
        width += 8 - ((width % 8) or 8)
        fmt = '%%0%dx' % (width // 4)
        prikey = binascii.unhexlify(fmt % val)

    pubkey = PrivateKey(prikey).pubkey.serialize(compressed=False)
    hash_pub = hashlib.sha3_256(pubkey[1:]).hexdigest()
    return f"hx{hash_pub[-40:]}"


priv_key = sys.argv[1:][0]
password = sys.argv[1:][1]

if priv_key.endswith('.der') or priv_key.endswith('.pem'):
    print(from_prikey_file(priv_key, password))
else:
    wallet = KeyWallet.load(priv_key, password)
    print(wallet.get_address())
