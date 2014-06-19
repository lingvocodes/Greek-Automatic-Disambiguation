import re, codecs, os
from lxml import etree

def every():
    def disamb(f):
        global unamb_bigr
        global dont
        gr2 = []
        t = codecs.open(f, 'r', 'utf-8')
        text = t.read()
        t.close()
        tree = etree.XML(text)
        for se in tree[1]:
            for w in range(len(se)):
                try:
                    if len(se[w]) == 1 and len(se[w + 1]) > 1:
    ##                    print etree.tostring(se[w], encoding = unicode), etree.tostring(se[w + 1], encoding = unicode)
                        for ana in se[w]:
                            try:
                                gr1 = ana.attrib['gr']
                            except KeyError:
                                gr1 = '-'
                        gr2 = []
                        for ana in se[w + 1]:
                            gr2.append(ana.attrib['gr'])
                            if ana.tail != '':
                                word = ana.tail
                        if word not in dont:
                            possible_gr2 = unamb_bigr[gr1]
                            dic_gr2 = {}
                            for gr in gr2:
                                dic_gr2[gr] = possible_gr2[gr]
                            max_freq = max(dic_gr2.values())
                            chosen_gr2 = []
                            for gr in dic_gr2:
                                if dic_gr2[gr] == max_freq:
                                    chosen_gr2.append(gr)
                                    break
                            for ana in range(len(se[w + 1])):
                                if se[w + 1][ana].attrib['gr'] not in chosen_gr2:
    ##                                if se[w + 1][ana].tail != '' and se[w + 1][ana].tail != None:
                                    del se[w + 1][ana]
                                    se[w + 1][-1].tail = word
    ##                        print 'result', etree.tostring(se[w + 1], encoding=unicode)
                except:
                    continue
        text = etree.tostring(tree, encoding = unicode)
        return text
                
    dont = [u'στον', u'στην', u'στο', u'στη', u'στις']
                
    unamb_bigr = {}
    b = codecs.open('Unambiguous_bigrams.csv', 'r', 'utf-8')
    for line in b:
        line = line.strip()
        bigram, frequency = line.split('^')
        gr1, gr2 = bigram.split('|')
        try:
            unamb_bigr[gr1][gr2] = int(frequency)
        except:
            unamb_bigr[gr1] = {gr2:int(frequency)}
    b.close()

    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.xhtml'):
                text = disamb(root + '/' + f)
                f_new = codecs.open(root + '/' + f, 'w', 'utf-8')
                f_new.write(text)
                f_new.close()
        for d in dirs:
            root += '/' + d

if __name__ == '__main__':
    every()
