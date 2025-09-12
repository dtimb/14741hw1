#!/usr/bin/env python3

from pwn import *
from Crypto.Util.strxor import strxor

context.proxy = (socks.SOCKS5, 'localhost', 8123) # SOCKS proxy
host = '192.168.2.99' # Remote machine name
port = 62339 # Remote port
conn = remote(host, port)
content = conn.recv(1024)

conn.sendline(b'1')
conn.sendline((b'\x00'*34).decode('latin-1'))

conn.recvuntil("Your encrypted message is  ")

key = conn.recvline()[:-1].decode()

conn.sendline(b'2')
conn.recvuntil("0 : ")

ciphertext = conn.recvline()[:-1].decode()

conn.close()

key = bytes.fromhex(key)
ciphertext = bytes.fromhex(ciphertext)

flag = strxor(key, ciphertext)

print(flag)

#conn.interactive()