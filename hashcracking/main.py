#!/usr/bin/env python3

from pwn import *
from Crypto.Util.strxor import strxor
import hashlib
import random
import time

context.proxy = (socks.SOCKS5, 'localhost', 8123) # SOCKS proxy
host = '192.168.2.99' # Remote machine name
port = 56887 # Remote port
conn = remote(host, port)

def generate_hash(username, password):
    username = username.strip(" ")
    print(username)
    parts = username.split()
    assert len(parts) == 2
    firstname, lastname = parts[0], parts[-1]
    combined = firstname + "_" + lastname + password
    hashed = hashlib.sha256(combined.encode()).hexdigest()
    return hashed

conn.recvuntil(b"Can you crack this hash?\n")
givenHash = conn.recvline()
hashstr = givenHash.decode('utf-8').strip()

excelsior = ''

with open("hashcracking/user_list.txt", "r") as f:
    users = [line.strip() for line in f if line.strip()]
with open("hashcracking/password_list.txt", "r", ) as f:
    passwords = [line.strip() for line in f if line.strip()]

found = False


while not found:
    username = random.choice(users)
    password = random.choice(passwords)

    excelsior = generate_hash(username, password)

    print(excelsior, "----", hashstr)

    if excelsior == givenHash:
        found = True
        print("YIPPEE")


conn.close()


#conn.interactive()
#conn.recvuntil("Can you crack this hash?")
#balls = conn.recvline()




