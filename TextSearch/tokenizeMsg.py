import nltk
import re

def tokenizeSearch(initial_search):
    regexTokens= re.sub("[^a-zA-Z0-9#@ ]+",'', initial_search).lower().split()
    stop_words = set(nltk.corpus.stopwords.words('english'))

    allStop = True
    for word in regexTokens:
        if word not in stop_words:
            allStop = False

    if allStop == False:
        withoutStop = []
        for word in regexTokens:
            if word not in stop_words:
                withoutStop.append(word)
        return withoutStop
    else:
        return regexTokens

def tokenizeMsg(initial_message):
    regexTokens= re.sub("[^a-zA-Z0-9#@ ]+",'', initial_message).lower().split()
    # regexTokens = nltk.TweetTokenizer().tokenize(regexString)
    index = {}
    for x in range(len(regexTokens)):
        if regexTokens[x] in index:
            index[regexTokens[x]].append(x)
        else:
            index[regexTokens[x]] = [x]
    return index
    

