#-------------------------------------------------------------------------------
# Name:        Dumb Bayes Learner
# Purpose:
#
# Author:      Nathan Jacobs
#
# Created:     26/09/2013
# Copyright:   (c) Shiro_Raven 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

def main():

    TitleWordList = {}

    def Learn():
        pass

    def WriteLearnedWeights():
        pass

    #train on data.txt the learning set of sgm 000-020

    title = ""

    #go through line by line until next title found
    with open('output.txt','r') as file:
        for line in file:
            if ("\t" not in line):
                title = line
                titlewords = line.split()
                for word in titlewords:
                    if (word in list(TitleWordList.keys())):
                        #update value

            else:
                #ignore


if __name__ == '__main__':
    main()
