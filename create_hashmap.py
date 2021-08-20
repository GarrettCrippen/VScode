from atheletes_df import *
from transform_names import *
from hashlib import sha1

def encode_sha1(data):
    h = sha1()
    h.update(data)
    return h.hexdigest()

def create_hashmap():
    dict = {}
    athletes = transform_data(create_df()['name'])

    for name in athletes:  
        for to_hash in athletes[name]:
            upper = encode_sha1(to_hash.encode())[:5]
            lower = encode_sha1(to_hash.encode())[5:]
            if upper not in dict:
                dict[upper]=[(lower,to_hash)]

            else:
                dict[upper].append((lower,to_hash))
                print(f'for {to_hash}: appended {lower} to {upper}, shares hash with {dict[upper][0][1]}')

    print(f'There are: {len(dict.keys())} unique hashes.')
    return dict