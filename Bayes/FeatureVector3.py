
#!/usr/bin/env python

from TagExtractor import ReuterRooter as RR
import nltk
import re
import sys
import operator

def main():
    blacklist = []

    LearnedDictionry = {}

    def LearnKNearest(topicList, titleList, bodyDic):

        def AddWord(word, addWord, amount):
            if (word in list(LearnedDictionry.keys())):
                if (addWord in LearnedDictionry[word]):
                    LearnedDictionry[word][addWord] += amount
                else:
                    LearnedDictionry[word][addWord] = amount
            else:
                bla = {}
                bla[addWord] = 1
                LearnedDictionry[word] = bla

        #judge words by distance from each other
        tempDic = {}
        tempBlack = []

        #for each topic word, search for neighbors in text
        for topic in topicList:
            if (topic in titleList):
                titleIndex = titleList.index(topic)
                if (titleIndex > 1):
                    AddWord(topic, titleList[titleIndex - 1], 1)
                if (titleIndex < len(topicList) - 2):
                    AddWord(topic, titleList[titleIndex + 1], 1)
            if (topic in bodyDic):
                sorted_body = sorted(bodyDic.iteritems(), key=operator.itemgetter(1))
                for i in range(0, min(3, len(sorted_body))):
                    AddWord(topic, sorted_body[i][0], sorted_body[i][1])

    def AddToDict(daDic, word, blacklist):
        if (len(word) > 2) and (word not in blacklist):
            if word in daDic:
                daDic[word] += 1
            else:
                daDic[word] = 1

    with open('stopwords.txt') as f:
        for line in f:
            blacklist.append(line.rstrip())

    for i in range(0,1):
        filename = "reut2-%s.sgm" % ("%03d" % i)
        print filename
        sgm = RR(filename)
        for j in range(0,1):
        #for j in range(0,sgm.NumberOfReuters()-1):
            TitleWords = {}
            BodyDic = {}
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
            for token in body.split():
                AddToDict(BodyDic, token, blacklist)

            if (len(TopicWords) > 0):
                LearnKNearest(TopicWords, TitleWords, BodyDic)

        print("Learned value cocoa: " + str(LearnedDictionry["cocoa"]))

        print 'done'

if __name__ == '__main__':
    main()
