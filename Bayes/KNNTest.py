#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Shiro_Raven
#
# Created:     28/09/2013
# Copyright:   (c) Shiro_Raven 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import pickle
import operator
import re
from KNNPlease import WordWeight
from TagExtractor import ReuterRooter as RR

def Classify(bodyWords, titleWords, WordDic):
	#go through all words keeping a dict of potential Topics and weights

	TopicWeights = {}

	for word in bodyWords:
		if(WordDic.has_key(word)):
			topicWord = WordDic[word].GetLikelyTopicWord()
			if (TopicWeights.has_key(topicWord)):
				TopicWeights[topicWord] += 1
			else:
				TopicWeights[topicWord] = 1

	for word in titleWords:
		if(WordDic.has_key(word)):
			topicWord = WordDic[word].GetLikelyTopicWord()
			if (TopicWeights.has_key(topicWord)):
				TopicWeights[topicWord] += 3
			else:
				TopicWeights[topicWord] = 3

	#return list of top 3 words
	sorted_topics = sorted(TopicWeights.iteritems(), key=operator.itemgetter(1))
	sorted_topics = sorted_topics[::-1]

	temp = []
	for pair in sorted_topics[0:5]:
		temp.append(pair[0])

	return temp

def main():
	blacklist = []

	score = 0.0
	total = 0.0

	with open('stopwords.txt') as f:
		for line in f:
			blacklist.append(line.rstrip())

    #read in pickle
	file = open("k=5.txt", 'rb')
 	WordDic = pickle.load(file)

    #go through sgm 021 and test
	filename = "reut2-017.sgm"
 	sgm = RR(filename)
	for j in range(0,sgm.NumberOfReuters()-1):
		TitleWords = []
		BodyList = []
		TopicWords = []

		#print("\n" + sgm.ExtractTagData(j,"TITLE"))
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


		mine = Classify(BodyList, TitleWords, WordDic)
		your = TopicWords

		#compare mine to your
		total += 1
		if (len(your) == 0):
			score += 1
			#total -= 1
		else:
			#print (str(mine))
			#print (str(your) + "\n")
			for word in mine:
				if (word in your):
					score += 1
					total += 1

	print("Score: " + str(score/total))

if __name__ == '__main__':
    main()
