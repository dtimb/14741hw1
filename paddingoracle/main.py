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

givenCookie = conn.recvline()
#givenCookie = givenCookie.decode()
#conn.sendline(givenCookie)

IV = b"This is an IV456"
IV = binascii.hexlify(IV)
givenCookie = binascii.hexlify(givenCookie)

block1 = givenCookie[:32]
block2 = givenCookie[32:64]
block3 = givenCookie[64:96]
block4 = givenCookie[96:128]
block5 = givenCookie[128:160]
block6 = givenCookie[160:192]
block7 = givenCookie[192:]

print(strxor(IV, block1).decode())

"""
print("Given Cookie: ", givenCookie)
print("Given Cookie length: ", len(givenCookie))
print("Block length: ", len(block1))
print(block1)
print(block2)
print(block3)
print(block4)
print(block5)
print(block6)
print(block7)
"""

conn.interactive()






conn.close()

