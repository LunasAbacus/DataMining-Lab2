
#!/usr/bin/env python

from TagExtractor import ReuterRooter as RR
import nltk
import re
import sys
import operator
import pickle

#Hold each non-topic word
#fill with topic words as found
class WordWeight:

    def __init__(self):
        self.wordWeights = {}
        self.topicWord = ""

    def AddTopicWord(self,word, distance):
        distance = distance + 1
        word = word.lower()
        if (self.wordWeights.has_key(word)):
            self.wordWeights[word] += 100/distance
        else:
            self.wordWeights[word] = 100/distance

    def GetLikelyTopicWord(self):
        if (len(self.topicWord) > 0):
            return self.topicWord
        else:
            sorted_topics = sorted(self.wordWeights.iteritems(), key=operator.itemgetter(1))
            self.topicWord = sorted_topics[-1][0]
            return self.topicWord

def main():
    blacklist = []

    WordDic = {}

    def Learn(bodyWords, titleWords, topicWords, kDistance):
        #find index of word in words list and sample k-nearest neighbors

        for topic in topicWords:
            #find every index of topic word
            bodyIndexes = []
            for i in range(0, len(bodyWords) - 1):
                if(bodyWords[i] == topic):
                    bodyIndexes.append(i)

            titleIndexes = []
            for i in range(0, len(titleWords) - 1):
                if(titleWords[i] == topic):
                    titleIndexes.append(i)

            #for each index add every word, within k distance
            # from index, with topic word
            for index in bodyIndexes:
                for i in range(max(0, index - kDistance), min(len(bodyWords) - 1, index + kDistance)):
                    if (not WordDic.has_key(bodyWords[index])):
                        WordDic[bodyWords[index]] = WordWeight()
                    WordDic[bodyWords[index]].AddTopicWord(bodyWords[i], abs(index-i))

            for index in titleIndexes:
                for i in range(max(0, index - kDistance), min(len(titleWords) - 1, index + kDistance)):
                    if (not WordDic.has_key(titleWords[index])):
                        WordDic[titleWords[index]] = WordWeight()
                    WordDic[titleWords[index]].AddTopicWord(titleWords[i], abs(index-i))

    with open('stopwords.txt') as f:
        for line in f:
            blacklist.append(line.rstrip())

    for i in range(0,21):
        filename = "reut2-%s.sgm" % ("%03d" % i)
        print filename
        sgm = RR(filename)
        for j in range(0,sgm.NumberOfReuters()-1):
            TitleWords = []
            BodyList = []
            TopicWords = []

            TitleWordsTemp = sgm.ExtractTagData(j,"TITLE").lower().split()
            for word in TitleWordsTemp:
                if (len(word) > 2 and word not in blacklist):
                    TitleWords.append(word)

            topics = sgm.ExtractTagData(j,"TOPICS")
            topics = topics.lower()
            topics = re.sub("<d>","", topics)
            topics = re.sub("</d>"," ", topics)
            topics = re.sub("-"," ", topics)
            TopicWordsTemp = topics.split()
            TopicWords = []

            for word in TopicWordsTemp:
                if (len(word) > 2 and word not in blacklist):
                    TopicWords.append(word)

            if (len(TopicWords) > 0):
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
                    if (len(word) > 2 and word not in blacklist):
                        BodyList.append(word)

                Learn(BodyList, TitleWords, TopicWords, 50)

    #save WordDic for later use
    fileW = open("K=50.txt", "wb")
    pickle.dump(WordDic, fileW)

if __name__ == '__main__':
    main()
