#!/usr/bin/env python

#import xml.etree.ElementTree as ET
import xml.etree.ElementTree as ET
import re

class ReuterRooter:
    reuterList = []

    def __init__(self, filename):
        self.reuterList = self.ReadSGM(filename)


    def ExtractReuters(self, sgmStr):
        lst = sgmStr.split("<REUTERS")
        return lst[1:] #remove first line which is garbage

    def NumberOfReuters(self):
        return len(self.reuterList)-1

    def ExtractTagData(self, reuterNumber, tag):
        if (reuterNumber < len(self.reuterList)):
            #extract data between <Tag>...</Tag>
            startTag = "<"+tag+">"
            endTag = "</"+tag+">"
            try:
                startLen = self.reuterList[reuterNumber].index(startTag) + len(startTag)
                endLen = self.reuterList[reuterNumber].index(endTag)
                ret = self.reuterList[reuterNumber][startLen:endLen]
                return re.sub("&lt;","<", ret)
            except ValueError:
                return ""
        else:
            return ""


    def ReadSGM(self, filename):
        #returns an array of reuters for the sgm file
        strList = []

        with open(filename) as f:
            for line in f:
                line = re.sub("(&#\d+;)","", line)
                line = re.sub("\t\r\n", " ", line)
                #line = re.sub("[^\x20-\x7f]+","",line)
                strList.append(line)

        sgm = ''.join(strList)
        return self.ExtractReuters(sgm)

def main():
    #get a list of reuters
    sgmRooter = ReuterRooter('reut2-001.sgm')

    print(sgmRooter.ExtractTagData(1,"BODY"))


if __name__ == '__main__':
    main()
