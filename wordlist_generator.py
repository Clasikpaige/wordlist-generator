import os
import subprocess
import argparse
import pandas as pd
import hashlib
import binascii
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pybtc import BitcoinPrivateKey
from mnemonic import Mnemonic


def generate_wordlist(count, output_file):
    mnemonic = Mnemonic("english")
    words = mnemonic.generate(strength=128)
    df = pd.DataFrame([words], columns=['word'])
    df.to_csv(output_file, index=False)
    return words


def hash_wordlist(hash_type, wordlist_file):
    hash_command = f'john --wordlist={wordlist_file} --format={hash_type}'
    subprocess.run(hash_command, shell=True)


def generate_private_key(wordlist, target_hash):
    backend = default_backend()
    salt = os.urandom(16)
    password = None
    mnemonic = Mnemonic("english")
    if mnemonic.check(target_hash):
        password = target_hash.encode()
    else:
        return None
    if password:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=backend
        )
        seed = mnemonic.to_seed(password)
        key = kdf.derive(seed)
        private_key = binascii.hexlify(key).decode()
        return private_key
    return None


def validate_private_key(private_key, target_address):
    key = BitcoinPrivateKey(private_key)
    address = key.public_key().address()
    return address == target_address


def main():
    parser = argparse.ArgumentParser(description='Generate a wordlist and hash it with John the Ripper.')
    parser.add_argument('--count', type=int, default=1, help='the number of words to generate in the wordlist')
    parser.add_argument('--output', type=str, default='wordlist.csv', help='the name of the output file')
    parser.add_argument('--hash-type', type=str, default='md5crypt', help='the type of hash to use with John the Ripper')
    parser.add_argument('--target', type=str, default=None, help='the hostname or wallet to target')
    parser.add_argument('--target-hash', type=str, default=None, help='the hash of the target to generate the private key for')
    args = parser.parse_args()

    count = args.count
    output_file = args.output
    hash_type = args.hash_type
    target = args.target
    target_hash = args.target_hash

    if not target:
        target = input("Enter the target hostname or wallet address: ")
    if not target_hash:
        target_hash = input("Enter the target BIP39 seed phrase: ")

    wordlist_file = os.path.join('wordlist', output_file)
    wordlist = generate_wordlist(count, wordlist_file)
    hash_wordlist(hash_type, wordlist_file)

    if target and target_hash:
        print(f"Generating private key for target {target}...")
        private_key = generate_private_key(wordlist, target_hash)
        if private_key:
            print(f"Private key generated: {private_key}")
            is_valid = validate_private_key(private_key, target)
            if is_valid:
print(f"The private key is valid and matches the bitcoin address {address}")
else:
print("The private key is not valid for the given bitcoin address.")
else:
print("Unable to generate private key for target.")

if name == 'main':
main()
