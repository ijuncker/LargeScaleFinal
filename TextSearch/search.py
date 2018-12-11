import mongo_stuff
import tokenizeMsg


def getSearchResults(query):
    messageList = mongo_stuff.search_get_messages(query)

    sortedMessages = mongo_stuff.sorted_messages(messageList, query)

    return sortedMessages


