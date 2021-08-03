from sha1 import sha1
import requests

url = "https://api.pwnedpasswords.com/range/"
password = sha1(input("input a password: ").encode())

hashSlice = password[:5]
key = password[5:-1]

print("Key: ", key,"\n\n")
#Make an api call for HaveIBeenPwned
response = requests.request("GET", url+hashSlice)

print(response.text)