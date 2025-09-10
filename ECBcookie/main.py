#!/usr/bin/env python3

from pwn import *

context.proxy = (socks.SOCKS5, 'localhost', 8123) # SOCKS proxy
host = '192.168.2.99' # Remote machine name
port = 53603 # Remote port
conn = remote(host, port)
content = conn.recv(1024)
print(content)
conn.interactive()

# receive first half of admin cookie, receive second half of personal cookie. combine and respond with that, ctf flag returned.









conn.close()

