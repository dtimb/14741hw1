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

context.proxy = (socks.SOCKS5, 'localhost', 8123) # SOCKS proxy
host = '192.168.2.99' # Remote machine name
port = 64822 # Remote port
conn = remote(host, port)
#content = conn.recv(1024)
#print(content)
#conn.interactive()



# interact w/ local script
#conn = process(["python3", "paddingoracle/pkcs7.py"])
#content = conn.recv(1024)
#print(content)

conn.recvline()
conn.recvuntil(b"Here is a sample cookie: ")

ciphertext = conn.recvline().decode().strip()

conn.close() # close after initial connection (re-opened in loop below)

IV = b"This is an IV456" # initialization vector
blocks_list = [ciphertext[i:i+32] for i in range(0, len(ciphertext), 32)] # create a list of all the blocks based on the received ciphertext


new_plaintext = b'\x00'*16



decrypted_blocks = [
    bytearray(b'\xb2\xda\rx^!\x06[\xa1$9\x1d\xc8\x01\xd0L'),
    bytearray(b'\x96\x86t\xbc\x7fa\xfcT\r\xe83}S\xbd\xdc3'),
    bytearray(b'\xa6\xcb\x14\xcf\xe2\xc8\x01\x11^U\xd4!\x9bC\x9a\xbe'),
    bytearray(b'\r\xfa\x98Yk\x14L*b\x02\xbb\x96\xd7 ZC'),
    bytearray(b'\xab\x8cN\x17H\xcbNI?\x9e\x1a8\x17\xa9\xb4z')
]

cipher_blocks_hex = [
    bytearray(b'5468697320697320616e204956343536'),
    bytearray(b'f4b294c82ae4cbc5bdc592a4b76186e6'),
    bytearray(b'1070cf8d6befe2385b94bee95618fa39'),
    bytearray(b'd0057150fa6acd09fa6b6cc2f78ab32e'),
    bytearray(b'5fd7ad4103f868a594ebf75bb1b3e4bd'),
    bytearray(b'b7fcb024c28a4cb087cfedc467ebdc66')
] 


print(decrypted_blocks ^ cipher_blocks_hex)

# print out blocks for debugging
def enumerate_blocks(b):
    print(f"# of blocks: {len(b)}")

    for i, b in enumerate(b):
        print(f"Block {i}: {b}")




print("Start: ", time.time())
for j in range(len(blocks_list)-1, 0, -1):
    target_block = bytearray.fromhex(blocks_list[j])
    block = bytearray.fromhex(blocks_list[j-1])

    modified_block = bytearray(16) # create empty byte array for use in byte loop
    plaintext = bytearray(16) # create list intended for storage of plaintext
    intermediate = bytearray(16)

    for b in range(15,-1,-1):

        padding = 16 - b
        
        # iterates through every possible byte until correct padding is found
        for i in range(256):
            conn = process(["python3", "paddingoracle/pkcs7.py"]) # re-opens process every time iterated
            block_clone = block[:] # create a copy of original block [c-1]
            
            for k in range(15, b, -1):
                block_clone[k] = intermediate[k] ^ padding
            
            block_clone[b] = i # changes (last) byte of block

            guess = bytes(block_clone) + bytes(target_block) # concatenate block w/ guessed byte & target block that is being solved for
            conn.sendline(binascii.hexlify(guess)) # sends guess to server after converting to hex
            response = conn.clean().decode().strip() # captures server response to meet conditional that either ends loop or continues

            conn.close() # close connection

            # restarts above loop if "invalid padding" received
            if "invalid padding" in response: 
                continue

            # if "invalid padding" is never received, break from loop and store new plaintext byte
            
            intermediate[b] = i ^ padding
            plaintext[b] = intermediate[b] ^ (block[b]) # creates the correct modified block to be used in plaintext (ex. ""...\x01")
            
            #print("Intermediate / DC: ", intermediate)
            #print("block clone: ", block_clone)
            #print(bytes(plaintext))

            break
        #full_plaintext[j] = plaintext
    print("Plain text: ", plaintext)
print("End: ", time.time())
