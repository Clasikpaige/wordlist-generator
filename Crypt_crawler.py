import os
import subprocess
import argparse
import pandas as pd
from pywallet import wallet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from mnemonic import Mnemonic
from bitcoinlib.keys import BitcoinPrivateKey
import multiprocessing

def generate_wordlist(count, output_file):
    mnemonic = Mnemonic("english")
    words = mnemonic.generate(strength=128)
    df = pd.DataFrame(words.split(), columns=['word'])  # Fixed column syntax
    df.to_csv(output_file, index=False)
    return words

def hash_wordlist(hash_type, wordlist_file):
    hash_command = f'john --wordlist={wordlist_file} --format={hash_type}'
    subprocess.run(hash_command, shell=True)

def generate_private_key(mnemonic, target_hash):
    backend = default_backend()
    salt = os.urandom(16)
    password = None
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
        private_key = key.hex()
        return private_key
    return None

def validate_private_key(private_key, target_address):
    key = BitcoinPrivateKey(private_key)
    address = key.public_key().address()
    return address == target_address

def recover_recovery_phrase(wordlist, target_address):
    for word in wordlist:
        seed = wallet.mnemonic_to_seed(word)
        recovered_wallet = wallet.create_wallet(network="BTC", seed=seed, children=1)
        recovered_address = recovered_wallet['address']
        
        if target_address == recovered_address:
            return word
    
    return None

def process_wordlist_chunk(chunk, target_address):
    mnemonic = Mnemonic("english")
    for word in chunk:
        seed = wallet.mnemonic_to_seed(word)
        recovered_wallet = wallet.create_wallet(network="BTC", seed=seed, children=1)
        recovered_address = recovered_wallet['address']
        
        if target_address == recovered_address:
            return word
    
    return None

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

    if not target:
        target = input("Enter the target hostname or wallet address: ")

    target_hash = args.target_hash

    if not target_hash:
        target_hash = input("Enter the target BIP39 seed phrase: ")

    wordlist_file = os.path.join('wordlist', output_file)
    wordlist = generate_wordlist(count, wordlist_file)
    hash_wordlist(hash_type, wordlist_file)

    if target_hash:
        mnemonic = Mnemonic("english")
        private_key = generate_private_key(mnemonic, target_hash)
        if private_key:
            print(f"Private key generated: {private_key}")
            is_valid = validate_private_key(private_key, target)
            if is_valid:
                print("Private key is valid!")
            else:
                print("Generated private key is invalid.")
        else:
            print(f"No matching password found for target hash {target_hash}.")

    recovery_word = None
    if wordlist:
        pool = multiprocessing.Pool()  # Create a multiprocessing pool
        num_processes = multiprocessing.cpu_count()  # Number of available CPU cores
        chunk_size = len(wordlist) // num_processes
        wordlist_chunks = [wordlist[i:i + chunk_size] for i in range(0, len(wordlist), chunk_size)]

        # Run the wordlist chunks in parallel
        results = [pool.apply_async(process_wordlist_chunk, args=(chunk, target)) for chunk in wordlist_chunks]

        # Get the results from the multiprocessing pool
        for result in results:
            recovery_word = result.get()
            if recovery_word:
                break

        pool.close()
        pool.join()

    if recovery_word:
        print(f"Recovered recovery phrase: {recovery_word}")
    else:
        print("Recovery phrase not found.")

if __name__ == '__main__':
    main()

