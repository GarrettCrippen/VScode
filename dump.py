import json
from athletes_df import *
from create_hashmap import *

# There are: 163800 total hashes.
# There are: 151619 unique hashes.
d=create_h()
with open('result2.json','w') as fp:
    json.dump(d,fp)