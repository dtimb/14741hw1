#!/usr/bin/python3 -u
import json
import sys
import time
import random

from Crypto.Cipher import AES

cookiefile = open("cookie.txt", "r").read().strip()
flag = open("flag.txt", "r").read().strip()
key = open("key.txt", "r").read().strip()
username = json.loads(cookiefile)["username"]

welcome = "Welcome to Secure Encryption Service version 1.{}".format(random.randint(0,99))

def pad(s):
  return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

def isvalidpad(s):
  return s[-1]*s[-1:]==s[-(s[-1]):]

def unpad(s):
  return s[:-(s[len(s)-1])]

def encrypt(m):
  IV=b"This is an IV456"
  cipher = AES.new(bytes.fromhex(key), AES.MODE_CBC, IV)
  return IV.hex()+(cipher.encrypt(pad(m).encode("utf8"))).hex()

def decrypt(m):
  cipher = AES.new(bytes.fromhex(key), AES.MODE_CBC, bytes.fromhex(m[0:32]))
  return cipher.decrypt(bytes.fromhex(m[32:]))
  

# flush output immediately
print (welcome)
print ("Here is a sample cookie: " + encrypt(cookiefile))

# Get their cookie
print ("What is your cookie?", flush=True)
cookie2 = sys.stdin.readline()
# decrypt, but remove the trailing newline first
cookie2decoded = decrypt(cookie2[:-1])

if isvalidpad(cookie2decoded):
  d=json.loads(unpad(cookie2decoded).decode('utf-8'))
  print ("username: " + d["username"])
  print ("Admin? " + d["is_admin"])
  exptime=time.strptime(d["expires"],"%Y-%m-%d")
  if exptime > time.localtime():
    print ("Cookie is not expired", flush=True)
  else:
    print ("Cookie is expired", flush=True)
  if d["is_admin"]=="true" and exptime > time.localtime() and d["username"] == username:
    print ("The flag is: " + flag, flush=True)
else:
  print ("invalid padding", flush=True)


