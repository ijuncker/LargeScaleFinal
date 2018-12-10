## GRPC For recieving message and search query can be put in main file

## can all put our parts in seperate files and  import to main

## GRPC will also need to be added into scalica to send the message and eventually search query to us

import pymongo
from datetime import datetime
import tokenizeMsg
import re
import math

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
    word_table = tokenizeMsg.tokenizeMsg(message["content"])
    '''
    With the resulting table, update the respective words in the collection with
    the new indexes
    '''
    for word in word_table.keys():
        if word_col.count_documents({"word": word}) > 0:
            to_modify = word_col.find_one({"word": word})
            index_info = to_modify["indexed"]
            index_info.append([m_id, word_table[word]])

            word_col.update_one(
                {"word": word}, 
                {
                    "$set": {
                        "indexed": index_info
                            }
                })
        else:
            to_insert = {
                "word": word,
                "indexed": [[m_id, word_table[word]]]
            }
            word_col.insert_one(to_insert)

# message = {
#     "message_id": message_col.count_documents({}),
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
@return: set of Message ids
'''
def search_get_message_ids(query, word_col):
    ids = set()
    cursor = word_col.find({
        "word" : {
            "$in" : tokenizeMsg.tokenizeSearch(query)
            }
        })
    for word in cursor:
        indexes = word["indexed"]
        for index in indexes:
            ids.add(index[0])
    
    return ids

'''
For Eddie's scoring method, returns a list of messages.
For reference, the Message object looks like this:
Message{
    "message_id": int
    "content": String
    "username": String
    "date_posted": Datetime
}

@param ids: set of ids
@param message_col: Message collection on mlab
@return: list of messages
'''
def search_get_messages_from_ids(ids, word_col, message_col):
    ids = search_get_message_ids("Scalica test", word_col)
    cursor = message_col.find({
        "message_id" : {
            "$in" : list(ids)
        }
    })
    message_list = []
    for message in cursor:
        message_list.append(message)

    return message_list


########################## SCORING STUFF ########################
def get_tf_idf(mess_in, word_in, mess_count_in, word_doc_count_in):
    # Split message into lists of words. 
    mess_list = tokenizeMsg.tokenizeMsg(mess_in).keys()
    
    # Calculate tf = term frequency = (# times word occurs in message) / (# words in message).
    tf = mess_list.count(word_in / len(mess_list))
    
    # Calculate idf = inverse document frequency = (# messages / # messages containing word).
    # mess_count -> from message_sort()
    # word_doc_count -> from message_sort()
    idf = math.log(mess_count_in / word_doc_count_in)

    # Calculate td_idf : (tf * idf)
    tf_idf = tf * idf
    return tf_idf


def sorted_messages(mess_list_in, query_in, message_col, word_col):
    mess_score_list = [] # List with (message_id, score)
    # print(mess_list_in[0]["content"]) # one message
    mess_count = message_col.count_documents({}) # Count of all messages. 
    
    # Loop through all messages.
    for message in mess_list_in:
        # Finds all 
        cursor = word_col.find({
            "word" : {
                "$in" : tokenizeMsg.tokenizeSearch(query_in)
                }
            })
        # For each word in the query
        for word in cursor:
            mess_score = 0
            word_doc_count = len(word["indexed"]) # Count of all words
            mess_score += get_tf_idf(message["content"], word, mess_count, word_doc_count)
        
        # Add to mess_score_list
        mess_score_list.append(message["message_id"], mess_score)
    
    return message
    

# message_sort([], "Scalica Twitter", message_col, word_col)

