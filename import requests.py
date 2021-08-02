import requests

url = "https://api.pwnedpasswords.com/range/"
password = input("please input a password")

response = requests.request("GET", url+password)

print(response.text)