## GRPC For recieving message and search query can be put in main file

## can all put our parts in seperate files and  import to main

## GRPC will also need to be added into scalica to send the message and eventually search query to us

import pymongo

connection = pymongo.MongoClient("ds127644.mlab.com", 27644)
db = connection["largescale"]
db.authenticate("largescale", "root56")

print(db.list_collection_names())

