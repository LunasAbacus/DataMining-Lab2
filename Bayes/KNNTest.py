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

def main():
    #read in pickle
    file = open("Knowledge.txt", 'rb')
    WordDic = pickle.load(file)

    #go through sgm 021 and test

if __name__ == '__main__':
    main()
