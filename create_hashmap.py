from atheletes_df import *
from transform_names import *
from hashlib import sha1

def encode_sha1(data):
    h = sha1()
    h.update(data)
    return h.hexdigest()

dict = {}
password_variations = transform_data(create_df()['name'])
for hash in password_variations:    
    upper = encode_sha1(hash.encode())[:5]
    if upper not in dict:
        dict[upper]=hash
    else:
        print(f'duplicate {dict[upper]} to {hash}')

print(len(dict))