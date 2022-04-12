#!/usr/bin/python3

import argparse
import nltk 
from nltk.corpus import brown

def subfinder(mylist, pattern):
    if mylist == []:
        return None
    for i in range(len(mylist)):
        if mylist[i] == pattern[0] and mylist[i:i+len(pattern)] == pattern:
            return i
    return None

def main():
    parser = argparse.ArgumentParser(description='Identify sentences that contain at least two NE.')
    parser.add_argument("-i", "--input", help='input file', required=True)
    parser.add_argument("-n", "--ne", help='NE file', required=True)
    parser.add_argument("-o", "--output", help='output file', required=True)

    args = parser.parse_args()

    namelist = []
    with open(args.ne, 'r') as n:
        namedict = {}
        for ne in n:
            ne = ne.strip()
            length = len(ne.split(" "))
            if length not in namedict.keys():
                namedict[length] = []
            namedict[length].append(ne)
    for n in sorted(list(namedict.keys()), reverse=True):
        namelist += namedict[n]

    with open(args.output, "w") as o:
        with open(args.input, 'r') as i:
            for text in i:
                sentences = nltk.sent_tokenize(text)
                tok_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
                for sentence in tok_sentences:
                    #print("New sentence")
                    sentence2 = sentence[:]
                    counter = 0
                    for name in namelist:
                        index = subfinder(sentence, name.split(" "))
                        while index != None:
                            #print("Found " + name + " " + str(counter))
                            counter += 1
                            del sentence[index:index+len(name)]
                            index = subfinder(sentence, name.split(" "))
                    if counter > 1:
                        o.write(" ".join(sentence2) + "\n")

if __name__ == '__main__':
    main()
