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
context.proxy = (socks.SOCKS5, 'localhost', 8123) # SOCKS proxy
host = '192.168.2.99' # Remote machine name
port = 64822 # Remote port
conn = remote(host, port)
content = conn.recv(1024)


print(content)
conn.interactive()

conn.close()

