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
from datetime import datetime

context.log_level = "critical" # hides non-critical pwntools errors i.e. JSON errors in this case (meant for clean terminal)

# interact w/ socket

context.proxy = (socks.SOCKS5, 'localhost', 8123) # SOCKS proxy
host = '192.168.2.99' # Remote machine name
port = 64822 # Remote port
conn = remote(host, port)

#content = conn.recv(1024)
#print(content)
#print(conn)
#conn.interactive()

# interact w/ local script
#conn = process(["python3", "paddingoracle/pkcs7.py"])
#content = conn.recv(1024)
#print(content)

#conn.interactive()

#conn.recvline()
conn.recvuntil(b"Here is a sample cookie: ")

ciphertext = conn.recvline().decode().strip()

conn.close()

IV = b"This is an IV456" # initialization vector
blocks_list = [ciphertext[i:i+32] for i in range(0, len(ciphertext), 32)] # create a list of all the blocks based on the received ciphertext

new_plaintext = b'exampleexampleex'
modified_block = bytearray()
saved_DC = []

#conn.close() # close after initial connection (re-opened in loop below)

# print out blocks for debugging
def enumerate_blocks(b):
    print(f"# of blocks: {len(b)}")

    for i, b in enumerate(b):
        print(f"Block {i}: {b}")

#conn = remote(host, port)
print("Start: ", datetime.now())
for j in range(len(blocks_list)-1, 0, -1):
    target_block = bytearray.fromhex(blocks_list[j])
    block = bytearray.fromhex(blocks_list[j-1])

    plaintext = bytearray(16) # create list intended for storage of plaintext
    DC = bytearray(16)

    for b in range(15,-1,-1):

        padding = 16 - b

        # iterates through every possible byte until correct padding is found
        for i in range(256):
            time.sleep(0.1)
            conn = remote(host, port) # re-opens process every time iterated


            conn.recvline()

            
            block_clone = block[:] # create a copy of original block [c-1]
            
            for k in range(15, b, -1):
                block_clone[k] = DC[k] ^ padding
            
            block_clone[b] = i # changes (last) byte of block
        
            guess = bytes(block_clone) + bytes(target_block) # concatenate block w/ guessed byte & target block that is being solved for
            #response = conn.recvline()
            #print(response)
            conn.sendline(binascii.hexlify(guess)) # sends guess to server after converting to hex
            response = conn.clean().decode().strip() # captures server response to meet conditional that either ends loop or continues
            #conn.close() # close connection

            # restarts above loop if "invalid padding" received
            if "username: " not in response: 
                conn.close()
                continue

            # if "invalid padding" is never received, break from loop and store new plaintext byte
            
            DC[b] = i ^ padding
            plaintext[b] = DC[b] ^ (block[b]) # creates the correct modified block to be used in plaintext (ex. ""...\x01")
            
            #print("DC / DC: ", DC)
            #print("block clone: ", block_clone)
            #print(bytes(plaintext))

            break
        #full_plaintext[j] = plaintext
    print("Plain text: ", plaintext)
    saved_DC.append(plaintext[:])

print("End: ", datetime.now())

conn.close()

conn = remote(host, port)

conn.recvuntil(b"Here is a sample cookie: ")

print("Saved DC: ", saved_DC)
chosen_index = 3
DC = saved_DC[2]
target_block = bytearray.fromhex(blocks_list[chosen_index])

new_plaintext = bytearray(b' "false", "expir')
new_plaintext[2:7] = b'true"'

modified_block = bytearray(16)

new_iv = strxor(bytes(DC), strxor(bytes.fromhex(blocks_list[2]), bytes(new_plaintext)))
print("DC: ", DC)
#fartballs = DC[3] ^ target_block[2]

#for i in range(16):
    #modified_block[i] = DC[3] ^ target_block[2] ^ new_plaintext[i]

final_ciphertext = new_iv + bytes(target_block)
#print("Modified_block: ", modified_block.hex())
print("Final ciphertext: ", final_ciphertext.hex())

conn.sendline(final_ciphertext.hex())
response = conn.clean().decode().strip()
print(response)