import nltk
import re

def tokenizeMsg(initial_message):
    regexString= re.sub("[^a-zA-Z0-9#@ ]+",'', initial_message)
    regexTokens = nltk.TweetTokenizer().tokenize(regexString)

    stop_words = set(nltk.corpus.stopwords.words('english'))

    withoutStop = []

    for word in regexTokens:
        if word.lower() not in stop_words and word not in ():
            withoutStop.append(word)

    index = {}
    for x in range(len(withoutStop)):
        if withoutStop[x].lower() in index:
            index[withoutStop[x].lower()].append(x)
        else:
            index[withoutStop[x]] = [x]
    return (withoutStop, index)


if __name__ == "__main__":
    print(tokenizeMsg("@Jimmy that's party was awesome #party. What were they doing. We jumped and were running. Awesome party:;<>,?}{?}"))

