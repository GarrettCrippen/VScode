from sha1 import sha1
import requests

url = "https://api.pwnedpasswords.com/range/"
input = input("input a password: ")
password = sha1(input.encode())

hashSlice = password[:5]
key = password[5:].upper()


#print("Key: %s \n" %key)
#Make an api call for HaveIBeenPwned
response = requests.request("GET", url+hashSlice)


#split payload by newline
pwned = False
hashes = response.text.split('\n')
for hash in hashes:
    if key in hash and not pwned:
        pwned = True
        times = hash.split(':')[1]

print(type(times))

print(F'Password {input} has been pwned {times} timezzzzzzz.')