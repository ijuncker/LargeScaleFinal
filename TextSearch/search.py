import mongo_stuff
import tokenizeMsg


def getSearchResults(query):

    ids = mongo_stuff.search_get_message_ids(query, mongo_stuff.word_col)

    messageList = mongo_stuff.search_get_messages_from_ids(ids, mongo_stuff.word_col, mongo_stuff.message_col)

    sortedMessages = mongo_stuff.sorted_messages(messageList, query, mongo_stuff.message_col, mongo_stuff.word_col)



