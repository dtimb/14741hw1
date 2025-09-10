#!/usr/bin/python3 -u
import sys
import time
import random
import string

from Crypto.Cipher import AES

admin_cookie = open("cookie.txt", "r").read().strip()
flag = open("flag.txt", "r").read().strip()

key = ''.join(random.choice(string.digits + 'abcdef') for _ in range(32))

# random version number in welcome is haha funny
welcome = "Welcome to ECB Secure Encryption Service version 1.{}".format(random.randint(0,99))

# f(x) converts key from hex to bytes, encrypts w/ AES using ECB mode and stores in cipher var
def encrypt(m):
  cipher = AES.new(bytes.fromhex(key), AES.MODE_ECB)
  return cipher.encrypt(m.encode("utf8")).hex() # 

def decrypt(m):
  cipher = AES.new(bytes.fromhex(key), AES.MODE_ECB)
  return (cipher.decrypt(bytes.fromhex(m))).decode('utf-8')
  


# flush output immediately
print (welcome)
print (len(admin_cookie))
print ("Here is an admin cookie: " + encrypt(admin_cookie))
print ("But here is yours: " + encrypt("I am not an administrator. This cookie expires 2030-11-01......."))

# Get their cookie
print ("What is your cookie?", flush=True)
cookie2 = sys.stdin.readline()
# decrypt, but remove the trailing newline first
cookie2decoded = decrypt(cookie2[:-1])
print (cookie2decoded)

if cookie2decoded.startswith('I am yes an admin'):
   exptime=time.strptime(cookie2decoded[47:57],'%Y-%m-%d')
   if exptime > time.localtime():
      print ("Cookie is not expired")
      print ("The flag is: " + flag, flush=True)
   else:
      print ("Cookie is expired", flush=True)
else:
   print ("No flag for you!", flush=True)
