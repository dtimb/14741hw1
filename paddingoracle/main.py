#!/usr/bin/env python3

# imports from pkcs7.py
import json
import sys
import time
import random
from Crypto.Cipher import AES

# imports 
from pwn import *
from Crypto.Util.strxor import *

context.log_level = "critical" # hides non-critical pwntools errors i.e. JSON errors in this case (meant for clean terminal)

# interact w/ socket
"""
context.proxy = (socks.SOCKS5, 'localhost', 8123) # SOCKS proxy
host = '192.168.2.99' # Remote machine name
port = 64822 # Remote port
conn = remote(host, port)
content = conn.recv(1024)


print(content)
conn.interactive()

conn.close()
"""

# interact w/ local script
conn = process(["python3", "paddingoracle/pkcs7.py"])
#content = conn.recv(1024)
#print(content)

conn.recvline()
conn.recvuntil(b"Here is a sample cookie: ")

ciphertext = conn.recvline().decode().strip()

conn.close() # close after initial connection (re-opened in loop below)

IV = b"This is an IV456" # initialization vector

blocks_list = [ciphertext[i:i+32] for i in range(0, len(ciphertext), 32)] # create a list of all the blocks based on the received ciphertext

# print out blocks for debugging
def enumerate_blocks(b):
    print(f"# of blocks: {len(b)}")

    for i, b in enumerate(b):
        print(f"Block {i}: {b}")


for j in range(len(blocks_list)-1, 0, -1):
    target_block = bytearray.fromhex(blocks_list[j])
    block = bytearray.fromhex(blocks_list[j-1])

    modified_block = bytearray(16) # create empty byte array for use in byte loop
    plaintext = bytearray(16) # create list intended for storage of plaintext
    temparray = bytearray(16)

    for b in range(15,-1,-1):
        padding = 16 - b

        for c in range(15, b, -1):
            block_clone[c] = temparray[c] ^ padding

        for i in range(256):
            conn = process(["python3", "paddingoracle/pkcs7.py"]) # re-opens process every time iterated

            block_clone = block[:] # create a copy of original block [c-1]
            block_clone[b] = i # changes (last) byte of block
            guess = bytes(block_clone) + bytes(target_block) # concatenate block w/ guessed byte & target block that is being solved for
        
            conn.sendline(binascii.hexlify(guess)) # sends guess to server after converting to hex
            response = conn.clean().decode().strip() # captures server response to meet conditional that either ends loop or continue

            if "invalid padding" in response: 
                conn.close() # close connection to prevent too many processes / connections being open at once before re-opening as loop continues
                continue
            
            conn.close() # close connection

            temparray[b] = i ^ padding
            modified_block[b] = (i ^ padding) ^ (block[b]) # creates the correct modified block to be used in plaintext (ex. ""...\x01")
            plaintext[b] = i ^ block[b]
            print(modified_block)
            break


