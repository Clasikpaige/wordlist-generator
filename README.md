# Wordlist_Generator
![alt text](https://www.dropbox.com/s/2jgjgzzl4b7m4gg/Photo%2014-05-2023%2C%2012%2001%2056%20PM.jpg?raw=1)

*This script generates a wordlist and hashes it using John the Ripper.
It can be used for security testing and password cracking.
Additionally, it can generate private keys for a specified target hash.*
*This functionality is useful for generating private keys for cryptocurrency wallets or other applications that use hashed values for authentication or verification.*

 The program uses a number of technologies to accomplish this. It relies on the John the Ripper tool for hashing the wordlist, and uses the cryptography library to generate private keys from the hashed values. It also uses the `pybtc` library for generating Bitcoin private keys, and the `mnemonic` library for generating BIP39 seed phrases.

Overall, the `wordlist_generator` program is a powerful tool that can help you with a variety of security testing and password cracking tasks, as well as generating private keys for cryptocurrency wallets and other The program takes several command-line arguments:
--count: the number of words to generate in the wordlist (default is 1)
--output: the name of the output file (default is "wordlist.csv")
--hash-type: the type of hash to use with John the Ripper (default is "md5crypt")
--target: the hostname or wallet to target (optional)
--target-hash: the hash of the target to generate the private key for (optional)

If the `target` and `target-hash` arguments are not specified, the user will be prompted to enter them. The program generates a wordlist, hashes it using the specified hash type, and then checks each word in the list to see if it generates a private key that matches the target address or wallet. If a matching private key is found, the program will indicate that the private key is valid. Otherwise, it will indicate that no matching password was found for the target hash.





![alt text](https://www.dropbox.com/s/1x2avy6hc9qsned/Photo%2014-05-2023%2C%2011%2045%2049%20AM.jpg?raw=1)



The program uses a number of technologies to accomplish this. It relies on the `John the Ripper` tool for hashing the wordlist, and uses the `cryptography` library to generate private keys from the hashed values. It also uses the `pybtc` library for generating Bitcoin private keys, and the `mnemonic` library for generating BIP39 seed phrases.

Overall, the `wordlist_generator` program is a powerful tool that can help you with a variety of security testing and password cracking tasks, as well as generating private keys for cryptocurrency wallets and other applications.

Installation

![alt text](https://www.dropbox.com/s/8t4cem1pmf3vmow/Photo%2014-05-2023%2C%2011%2048%2052%20AM.jpg?raw=1)

To install and utilize the wordlist_generator program, you must have Python 3 and John the Ripper installed on your system.
```
git clone https://github.com/clasikpaige/wordlist_generator.git
```
After cloning the repository, navigate to the wordlist_generator directory and install the required packages:
bash
```
cd wordlist_generator
pip install -r requirements.txt
```
Usage

To use the wordlist_generator tool, simply run the wordlist_generator.py script from the command line:

```
 python wordlist_generator.py
```
1. Generate a list of 20,000 random words and hash them using the MD5-Crypt algorithm. 
    - The generated wordlist will be saved to the `wordlist/wordlist.txt` file. 
    - The hashes will be saved to the `wordlist/wordlist.txt.hash` file.

2. Customize the length of the words, the number of words generated, and the hash algorithm used by modifying the variables at the top of the `wordlist_generator.py` file.

3. Specify a target hostname or wallet address by using the `--target` flag.

```
 python wordlist_generator.py --target example.com
```
This will generate a wordlist and hash it, using the MD5-Crypt algorithm, with the goal of cracking a password associated with the target hostname example.com. If you want to crack a password associated with a specific wallet address, you can use the --wallet flag:

```
 python wordlist_generator.py --wallet 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2
```
This will generate a wordlist and hash it, using the MD5-Crypt algorithm, with the goal of cracking a password associated with the wallet address 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2.

Note that the wordlist_generator tool should only be used for ethical purposes, such as security testing and password recovery. Do not use this tool to engage in illegal activities or to harm others.