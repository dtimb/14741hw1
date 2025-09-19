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

7c162d8434aa2d50f6d52dcaf3302f9857e2d76c0f58af61d7279e650a468879b49ceda6187c48a076caa7c0969fc358c1a99c5ba06edb8bbcb17bd7632f7a4b
cc603c4232a04cbb4d610d7bfc2af75057e2d76c0f58af61d7279e650a468879b49ceda6187c48a076caa7c0969fc358de59dbc7b172feb7042b5c74a29a0032

7c162d8434aa2d50f6d52dcaf3302f9857e2d76c0f58af61d7279e650a468879b49ceda6187c48a076caa7c0969fc358de59dbc7b172feb7042b5c74a29a0032
cc603c4232a04cbb4d610d7bfc2af75057e2d76c0f58af61d7279e650a468879



conn.close()

