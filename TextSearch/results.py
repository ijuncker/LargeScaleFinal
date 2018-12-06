# Get the query and connect to database.

# Use query to find relevant messages. 

# Sort releveant messages using calc_score 

import re
import math
# Score Calculation Function
"""
@param message_in - inputted message
@param query_in - inputted query
@returns - TF if one word
         - sum of TF_IDF if more than one word. 
"""
def calc_score(message_in, query_in):
    # Split query and message into lists of words. 
    mess_list = re.findall(r"[a-zA-Z_]+", message_in)
    query_list = re.findall(r"[a-zA-Z_]+", query_in)

    # Calculate tf = term frequency = (# times word occurs in message) / (# words in message).
    # (For first word in query)
    tf = mess_list.count(query_list[0]) / len(mess_list)

    # Calculate idf = inverse document frequency = (# messages / # messages containing word).
    # (For first word in query)
    mess_cnt = 0            # Database has total count of messages.
    word_in_mess_cnt = 0    # Database has array (1st layer) in Word for number of messages with the word : len(array)
    idf = math.log(mess_cnt / word_in_mess_cnt)

    # Calculate td_idf : (tf * idf)
    tf_idf = tf * idf 
    
    # If query is one word: Return tf of that word. 
    if len(query_list) == 1:
        return tf_idf
    
    else:
        score = 0
        # Iterate through each query word and calculate the tf_idf and sum them. 
        for word in query_list:
            tf = mess_list.count(word / len(mess_list))
            word_in_mess_cnt = 0    # Database has array (1st layer) in Word for number of messages with the word : len(array)
            idf = math.log(mess_cnt / word_in_mess_cnt)
            tf_idf = tf * idf 
            score += tf_idf
        return score
    



