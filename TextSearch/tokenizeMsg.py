import nltk
import re

def tokenizeSearch(initial_search):
    ##get rid of all punctation except for #s and @s and then split the string

    regexTokens= re.sub("[^a-zA-Z0-9#@ ]+",'', initial_search).lower().split()
    stop_words = set(nltk.corpus.stopwords.words('english'))

    ## check if the query consists of only stop words

    allStop = True
    for word in regexTokens:
        if word not in stop_words:
            allStop = False

    ## if all the words are not stop words, remove stop words from the query and return an array
    ## otherwise return the unmodified regex array containing all the stop words.
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
    index = {}

    ## if the word is in the dictionary, then just add the next position to the array associated with the word
    ## go through the tokens and if the word is not in the dictionary, add it and append the position of the word
    for x in range(len(regexTokens)):
        if regexTokens[x] in index:
            index[regexTokens[x]].append(x)
        else:
            index[regexTokens[x]] = [x]
    return index
    

