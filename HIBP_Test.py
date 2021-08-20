from hashlib import sha1

import requests


def encode_sha1(data):
    h = sha1()
    h.update(data)
    return h.hexdigest()


def main():
    password_plain = input("input a password: ")
    password_sha1 = encode_sha1(password_plain.encode())
    
    key_upper = password_sha1[:5]
    url = "https://api.pwnedpasswords.com/range"
    response = requests.get(f"{url}/{key_upper}")

    key_lower = password_sha1[5:].upper()

    pwnd = False
    breached = 0
    for hash in response.text.splitlines():
        if key_lower in hash:
            pwnd = True
            breached=int(hash.split(':')[1])
            break

    print(f"{password_plain} has been pwn'd {breached} times")


if __name__ == '__main__':
    main()