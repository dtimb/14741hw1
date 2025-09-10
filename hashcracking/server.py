import hashlib
import random
import time

def generate_hash(username, password):
    names = username.split(" ")
    assert len(names) == 2
    firstname, lastname = names[0], names[1]
    combined = firstname + "_" + lastname + password
    hashed = hashlib.sha256(combined.encode()).hexdigest()
    return hashed

def main():

    username = random.choice(open("user_list.txt", "r").read().split("\n"))
    password = random.choice(open("password_list.txt", "r").read().split("\n"))

    hash_to_guess = generate_hash(username, password)

    print("Can you crack this hash?")
    print(hash_to_guess)

    username = input("Enter username: ")
    password = input("Enter password: ")
    print("Checking credentials", end='', flush=True)
    for i in range(10):
        time.sleep(1)
        print(".", end="", flush=True)
    print()
    hashed_credentials = generate_hash(username, password)
    
    if hashed_credentials == hash_to_guess:
        with open("flag", "r") as file:
            print(f"Access granted! Flag: {file.read()}")
    else:
        print("Access denied!")

if __name__ == "__main__":
    main()
