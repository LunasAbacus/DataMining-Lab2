
#!/usr/bin/env python

from TagExtractor import ReuterRooter as RR
import nltk
import re
import sys
import operator

def main():
    blacklist = []

    TopicDic = {}

    def LearnShit(BodyList, TopicDic, blacklist, TopicWords):
        for word in TopicWords:
            AddToDict(TopicDic, word, blacklist, 100)
            #plus add two word next to it, with half weight
            if (word in BodyList):
                index = BodyList.index(word)
                if (index > 0):
                    AddToDict(TopicDic, BodyList[index - 1], blacklist, 1)
                if (index < len(BodyList)- 2):
                    AddToDict(TopicDic, BodyList[index + 2], blacklist, 1)

    def WordWeight(before, Word, after):
        weight = 0
        keyList = list(TopicDic.keys())
        if (before in keyList and len(before) > 0):
            weight += TopicDic[before]/15
        if (Word in keyList):
            weight += TopicDic[Word]
        if (after in keyList and len(after) > 0):
            weight += TopicDic[after]/15
        return weight

    def ClassifyShit(wordList):
        WordWeights = {}
        for word in wordList:
            WordWeights[word] = 0

        if (len(wordList) > 2):
            WordWeights[wordList[0]] += WordWeight("", wordList[0], wordList[1])

            for i in range(1, len(wordList) - 1):
                WordWeights[wordList[i]] += WordWeight(wordList[i-1], wordList[i], wordList[i+1])

            WordWeights[wordList[-1]] += WordWeight(wordList[-2],wordList[-1], "")

        #return list of top 3 words
        sorted_body = sorted(WordWeights.iteritems(), key=operator.itemgetter(1))
        sorted_body = sorted_body[::-1]
        RetList = []
        for i in range(0, min(4, len(sorted_body))):
            #print(sorted_body[i][0] + " : " + str(sorted_body[i][1]))
            RetList.append(sorted_body[i][0])
        return RetList

    def AddToDict(daDic, word, blacklist, weight):
        if (len(word) > 2) and (word not in blacklist):
            if word in daDic:
                daDic[word] += weight
            else:
                daDic[word] = weight

    with open('stopwords.txt') as f:
        for line in f:
            blacklist.append(line.rstrip())

    for i in range(0,21):
        filename = "reut2-%s.sgm" % ("%03d" % i)
        print filename
        sgm = RR(filename)
        #for j in range(0,1):
        for j in range(0,sgm.NumberOfReuters()-1):
            TitleWords = {}
            BodyList = []
            TopicWords = []

            TitleWords = sgm.ExtractTagData(j,"TITLE").lower().split()

            topics = sgm.ExtractTagData(j,"TOPICS")
            topics = topics.lower()
            topics = re.sub("<d>","", topics)
            topics = re.sub("</d>"," ", topics)
            topics = re.sub("-"," ", topics)
            TopicWords = topics.split()


            body = sgm.ExtractTagData(j,"BODY")
            body = re.sub("[\d]"," ", body)
            body = re.sub("[^\w-]"," ", body)
            body = re.sub("- ", "", body)
            body = re.sub(" -", "", body)

            body = body.lower()
            BodyListTemp = body.split()
            BodyList = []

            #black list words
            for word in BodyListTemp:
                if (word not in blacklist):
                    BodyList.append(word)

            LearnShit(BodyList, TopicDic, blacklist, TopicWords)

            #for token in body.split():
            #    AddToDict(BodyDic, token, blacklist)


    #print("")
    sorted_body = sorted(TopicDic.iteritems(), key=operator.itemgetter(1))
    sorted_body = sorted_body[::-1]
    #for i in range(0, min(15, len(sorted_body))):
    #    print(sorted_body[i][0] + " : " + str(sorted_body[i][1]))
    #print("")
    print 'done'
    #print(str(ClassifyShit(["bannana","hamster","coffee","oil"])))
    string = """With other major banks standing to lose even more than
                BankAmerica if Brazil wheat fails to service its debt, the analysts
                said they expect the debt will be restructured, similar to way
                Mexico's debt was, minimizing soybean wheat losses to the creditor banks."""

    #print(str(ClassifyShit(string.lower().split())))

    #now test learned data
    good = 0
    bad = 0

    filename = "reut2-021.sgm"
    sgm = RR(filename)
    #get wordlist from file
    WordList = []
    #for j in range(0,sgm.NumberOfReuters()-1):
    for j in range(0,5):
        body = sgm.ExtractTagData(j,"BODY")
        body = re.sub("[\d]"," ", body)
        body = re.sub("[^\w-]"," ", body)
        body = re.sub("- ", "", body)
        body = re.sub(" -", "", body)

        body = body.lower()
        WordListTemp = body.split()
        #black list words
        for word in WordListTemp:
            if (word not in blacklist):
                BodyList.append(word)

        #print("\nClassifying test article:\n")
        guessList = ClassifyShit(WordList)
        topics = sgm.ExtractTagData(j,"TOPICS")
        topics = topics.lower()
        topics = re.sub("<d>","", topics)
        topics = re.sub("</d>"," ", topics)
        topics = re.sub("-"," ", topics)
        TopicWords = topics.split()

        match = False
        #compare lists
        for word in guessList:
            if (word in topics):
                match = True

        if (match):
            good += 1
        else:
            bad += 1

    score = good / (good + bad)
    print ("Score: " + str(score))

if __name__ == '__main__':
    main()
