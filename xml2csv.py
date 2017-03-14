#! /usr/bin/env python3


import xml.etree.ElementTree
import pandas as pd
import sys, os

def checkArgs():
    if len(sys.argv) < 2:
        print("need an arg")
        sys.exit(1)
    else:
        if not os.path.isfile(sys.argv[1]):
            print("file not found: %s" % (sys.argv[1]))
            sys.exit(2)
        else:
            #print("file to parse: %s" % (sys.argv[1]))
            pass

def parseFile(filein):
    root = xml.etree.ElementTree.parse(filein).getroot()
    #print("%s, %s" % (root.tag, root.attrib))

    childTags = set()
    for child in root:
        if not child.tag.endswith('XMLSchema}schema'):
            childTags.add(child.tag)
    #print(childTags)

    
    dfs=[] # data frames
    for ctag in childTags:
        listOfDicts = []
        for child in root.findall(ctag):
            d = dict()
            for attr in child:
                d[attr.tag] = attr.text
                #print("%s %s" % (attr.tag, attr.text))

            listOfDicts.append(d)

        dfs.append(pd.DataFrame(listOfDicts)) 
    
    return dfs
if __name__ == "__main__":
    checkArgs()
    df = parseFile(sys.argv[1])
    print(df)
    for i in range(len(df)):
        outfile=sys.argv[1] + "." + str(i) + ".csv"
        df[i].to_csv(outfile)
        
