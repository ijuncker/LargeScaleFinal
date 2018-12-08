## GRPC For recieving message and search query can be put in main file

## can all put our parts in seperate files and  import to main

## GRPC will also need to be added into scalica to send the message and eventually search query to us

import pymongo
from datetime import datetime
import tokenizeMsg
import re

#connecting to database, can ignore
connection = pymongo.MongoClient("ds127644.mlab.com", 27644)
db = connection["largescale"]
db.authenticate("largescale", "root56")

#database names
message_col = db["Message"]
word_col = db["Word"]

#functions
'''
serializes the message, and updates all the words in the word index for that message
Example: the word "this" appears in document id 0, positions 2, 11, 21
The resulting data in the collection would look like:
{
    "word": "this",
    "indexed": [[0, [2, 11, 21]]]
}

If anther message with id 1 comes in, and "this" appears in positions 4, 15
The resulting updated data would look like:
{
    "word": "this",
    "indexed": [[0, [2, 11, 21]], [1, [4, 15]]]
}

@param message: JSON or dict data type
@param word_col: the Word collection in mlab
@return return: None
'''
def serialize_message_to_word(message, word_col):
    m_id = message["message_id"]
    word_table = tokenizeMsg.tokenizeMsg(message["content"])[1]
    '''
    With the resulting table, update the respective words in the collection with
    the new indexes
    '''
    for word in word_table.keys():
        if word_col.count_documents({"word": word}) > 0:
            to_modify = word_col.find_one({"word": word})
            index_info = to_modify["indexed"]
            index_info.append(word_table[word])

            word_col.update_one({"word": word}, {"$set": {"indexed": index_info}})
        else:
            to_insert = {
                "word": word,
                "indexed": [[m_id, word_table[word]]]
            }
            word_col.insert_one(to_insert)

# message = {
#     "message_id": message_col.estimated_document_count(),
#     "username": "test",
#     "content": "This is a post on Twitter, I mean Scalica",
#     "post_date": datetime.now()
# }

# message_col.insert_one(message)
# serialize_message_to_word(message, word_col)

'''
This function will return the message ids of the scalica messages from a query

@param query: String, search query
@param word_col: the Word collection in mlab
@param message_col: the Message collection in mlab
@return: set of Message ids
'''
def search_get_message_ids(query, word_col, message_col):
    ids = set()
    cursor = word_col.find({"word" : {"$in" : re.findall(r"[a-zA-Z_]+", query)}})
    for word in cursor:
        indexes = word["indexed"]
        for index in indexes:
            ids.add(index[0])
    return ids

'''
    cursor = message_col.find( {"message_id" : {"$in" : set}})
    for m in cursor:
        m['content']
'''
print(search_get_message_ids("Scalica is tight", word_col, message_col))