import requests

url = "https://api.pwnedpasswords.com/range/"
password1 = input("please input a password")

response = requests.request("GET", url+password)

print(response.text)