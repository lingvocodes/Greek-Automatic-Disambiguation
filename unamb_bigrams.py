import re, codecs, os
from lxml import etree

def every():

    dic_bigr = {}

    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.xhtml'):
                t = codecs.open(root + '/' + f, 'r', 'utf-8')
                text = t.read()
                try:
                    tree = etree.XML(text)
                    for body in tree:
                        for se in body:  
                            for word in range(len(se) - 1):
                                if len(se[word]) == 1 and len(se[word + 1]) == 1:
                                    try:
                                        for ana in se[word]:
                                            gr1 = ana.attrib['gr']
                                    except KeyError:
                                        gr1 = '-'
                                    try:
                                        for ana in se[word + 1]:
                                            gr2 = ana.attrib['gr']
                                    except KeyError:
                                        gr2 = '-'
                                    bigram = gr1 + '|' + gr2
                                    try:
                                        dic_bigr[bigram] += 1
                                    except:
                                        dic_bigr[bigram] = 1
                except:
                    print f
        for d in dirs:
            root += '/' + d

    b = codecs.open('Unambiguous_bigrams.csv', 'w', 'utf-8')
    for i in sorted(dic_bigr.keys(), key = lambda k: dic_bigr[k]):
        b.write(i + '^' + str(dic_bigr[i]) + '\n')
    b.close()
    
if __name__ == '__main__':
    every()

    
