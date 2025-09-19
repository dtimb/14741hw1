#!/usr/bin/env python3

from pwn import *
from Crypto.Util.strxor import strxor

context.proxy = (socks.SOCKS5, 'localhost', 8123) # SOCKS proxy
host = '192.168.2.99' # Remote machine name
port = 62339 # Remote port
conn = remote(host, port)
content = conn.recv(1024)

conn.sendline(b'1')
conn.sendline((b'\x00'*34).decode())

conn.recvuntil("Your encrypted message is  ")
ciphertext = conn.recvline()[:-1].decode()

conn.sendline(b'2')
conn.recvuntil("0 : ")

ciphertext2 = conn.recvline()[:-1].decode()

conn.close()

ciphertext = bytes.fromhex(ciphertext)
ciphertext2 = bytes.fromhex(ciphertext2)

#print(ciphertext)
#print(ciphertext2)

flag = strxor(ciphertext, ciphertext2)

print(flag)

