from __future__ import division
import os, codecs, re
from lxml import etree
# Counts and writes down types of homonymy and their frequencies and
# homonymous words and their frequencies

def every(turn):
    


    def count_homonymy(fname, root):
        text_file = codecs.open(root + '/' + fname, 'r', 'utf-8')
        global number_of_homo
        global tags
        global tokens
        for line in text_file:
            token = re.search('<w>', line)
            if token != None:
                tokens += 1
            tag = re.findall('(?:<ana[^/]*/>|<ana[^>]*></ana>)', line)
            tags += len(tag)
            homonymy = re.search('((?:<ana[^/]*/>|<ana[^>]*></ana>)){2,}(?!(στο|στον|στην|στις|στα|στους|στων|στου))', line, flags = re.U)
            if homonymy != None:
                number_of_homo += 1

    def which_homonymy(fname, root):
##        global l
        text_file = codecs.open(root + '/' + fname, 'r', 'utf-8')
        text = text_file.read()
        text = text.replace('<head></head>\r\n', '').replace('<body>\r\n', '').replace('</body>\r\n', '')
        global dict_of_homo
        global dict_of_words
##        try:
        tree = etree.XML(text)
        for se in tree:
            for word in se:
                if len(word) > 1:
                    word_info = []
                    for ana in word:
                        try:
                            lex = ana.attrib['lex']
                            gr = ana.attrib['gr']
                        except:
                            lex = ''
                            gr = ''    
                        if ana.tail != '':
                            word_occurence = ana.tail
                        word_info.append((lex, gr))
                    type_of_homo = ''
                    for info in word_info:
                        type_of_homo += info[0] + ',' + info[1] + '-'
                    type_of_homo = type_of_homo[:-1]
                    try:
                        dict_of_homo[type_of_homo] += 1
                    except:
                        dict_of_homo[type_of_homo] = 1
                    try:
                        dict_of_words[word_occurence] += 1
                    except:
                        dict_of_words[word_occurence] = 1
##        except:
##            l.write(root + '/' + fname + '\n')

    def monograms(fname, root):
        global l
        text_file = codecs.open(root + '/' + fname, 'r', 'utf-8')
        text = text_file.read()
        text = text.replace('<head></head>', '').replace('<body>', '').replace('</body>', '')
        try:
            tree = etree.XML(text)
            for se in tree:
                for index in range(len(se) - 1):
                    if len(se[index]) > 1:
                        if index != 0 or index != 1:
                            monogr = u''
                            try:
                                word_0 = se[index - 2][-1].tail + se[index - 2].tail
                            except IndexError:
                                word_0 = u''
                            try:
                                word_1 = se[index - 1][-1].tail + se[index - 1].tail
                            except IndexError:
                                word_1 = u''
                            for ana in se[index]:
                                monogr += ana.attrib['gr'] + '-'
                            monogr = monogr[:-1]
                            h_word = se[index][-1].tail
                            word_2 = se[index][-1].tail + se[index].tail
                            try:
                                word_3 = se[index + 1][-1].tail + se[index + 1].tail
                            except IndexError:
                                word_3 = u''
                            try:
                                word_4 = se[index + 2][-1].tail + se[index + 2].tail
                            except IndexError:
                                word_4 = u''
                            example = word_0 + word_1 + word_2 + word_3 + word_4
                            example = example.replace('\n', ' ')
                            try:
                                if len(monogr_ex[(h_word, monogr)]) < 20:
                                    monogr_ex[(h_word, monogr)].append(example)
                            except:
                                monogr_ex[(h_word, monogr)] = [example]
                            try:
                                monogr_count[(h_word, monogr)] += 1
                            except:
                                monogr_count[(h_word, monogr)] = 1
        except:
            l.write(root + '/' + fname + '\n')

    def bigrams(fname, root):
        global l
        text_file = codecs.open(root + '/' + fname, 'r', 'utf-8')
        text = text_file.read()
        text = text.replace('<head></head>', '').replace('<body>', '').replace('</body>', '')
        try:
            tree = etree.XML(text)
            for se in tree:
                for index in range(len(se) - 1):
                    if len(se[index]) > 1:
                        if index != 0 or index != 1:
                            bigr_1 = ''
                            bigr_2 = ''
                            try:
                                word_0 = se[index - 2][-1].tail + se[index - 2].tail
                                try:
                                    for ana in se[index - 1]:
                                        bigr_1 += ana.attrib['gr'] + '-'
                                except KeyError:
                                    bigr_1 = ''
                                word_before_h = se[index - 1][-1].tail
                                word_1 = se[index - 1][-1].tail + se[index - 1].tail
                            except IndexError:
                                word_0 = ''
                                word_1 = ''
                                bigr_1 = ''
                            for ana in se[index]:
                                bigr_2 += ana.attrib['gr'] + '-'
                            h_word = se[index][-1].tail
                            h_gr = bigr_2[:-1]
                            word_2 = se[index][-1].tail + se[index].tail
                            try:
                                word_3 = se[index + 1][-1].tail + se[index + 1].tail
                            except IndexError:
                                word_3 = ''
                            try:
                                word_4 = se[index + 2][-1].tail + se[index + 2].tail
                            except IndexError:
                                word_4 = ''
                            bigr_words = word_before_h + ' ' + h_word
                            bigr = bigr_1[:-1] + '|' + bigr_2[:-1]
                            example = word_0 + word_1 + word_2 + word_3 + word_4
                            example = example.replace('\n', ' ')
                            try:
                                if len(bigr_ex[bigr]) < 20:
                                    bigr_ex[bigr].append(example)
                            except:
                                bigr_ex[bigr] = [example]
                            try:
                                if len(bigr_words_ex[(bigr_words, bigr)]) < 20:
                                    bigr_words_ex[(bigr_words, bigr)].append(example)
                            except:
                                bigr_words_ex[(bigr_words, bigr)] = [example]
                            try:
                                bigr_count[bigr] += 1
                            except:
                                bigr_count[bigr] = 1
                            try:
                                bigr_words_count[(bigr_words, bigr)] += 1
                            except:
                                bigr_words_count[(bigr_words, bigr)] = 1
        except:
            l.write(root + '/' + fname + '\n')
        
    def trigrams(fname, root):
        global l
        text_file = codecs.open(root + '/' + fname, 'r', 'utf-8')
        text = text_file.read()
        text = text.replace('<head></head>', '').replace('<body>', '').replace('</body>', '')
        try:
            tree = etree.XML(text)
            for se in tree:
                for index in range(len(se) - 1):
                    if len(se[index]) > 1:
                        if index != 0 or index != 1:
                            trigr_1 = ''
                            trigr_2 = ''
                            trigr_3 = ''
                            try:
                                word_0 = se[index - 2][-1].tail + se[index - 2].tail
                                try:
                                    for ana in se[index - 1]:
                                        trigr_1 += ana.attrib['gr'] + '-'
                                except KeyError:
                                    trigr_1 = ''
                                word_1 = se[index - 1][-1].tail + se[index - 1].tail
                                word_before_h = se[index - 1][-1].tail
                            except IndexError:
                                word_0 = ''
                                word_1 = ''
                                trigr_1 = ''
                            for ana in se[index]:
                                trigr_2 += ana.attrib['gr'] + '-'
                            h_word = se[index][-1].tail
                            h_gr = trigr_2[:-1]
                            word_2 = se[index][-1].tail + se[index].tail
                            try:
                                for ana in se[index + 1]:
                                    trigr_3 += ana.attrib['gr'] + '-'
                            except KeyError:
                                trigr_3 = ''
                            try:
                                word_3 = se[index + 1][-1].tail + se[index + 1].tail
                                word_after_h = se[index + 1][-1].tail
                            except:
                                word_3 = ''
                            try:
                                word_4 = se[index + 2][-1].tail + se[index + 2].tail
                            except:
                                word_4 = ''
                            trigr_words = word_before_h + ' ' + h_word + ' ' + word_after_h
                            trigr = trigr_1[:-1] + '|' + trigr_2[:-1] + '|' + trigr_3[:-1]
                            example = word_0 + word_1 + word_2 + word_3 + word_4
                            example = example.replace('\n', ' ')
                            try:
                                if len(trigr_ex[trigr]) < 20:
                                    trigr_ex[trigr].append(example)
                            except:
                                trigr_ex[trigr] = [example]
                            try:
                                trigr_count[trigr] += 1
                            except:
                                trigr_count[trigr] = 1
                            try:
                                if len(trigr_words_ex[(trigr_words, trigr)]) < 20:
                                    trigr_words_ex[(trigr_words, trigr)].append(example)
                            except:
                                trigr_words_ex[(trigr_words, trigr)] = [example]
                            try:
                                trigr_words_count[(trigr_words, trigr)] += 1
                            except:
                                trigr_words_count[(trigr_words, trigr)] = 1
        except:
            l.write(root + '/' + fname + '\n')
                    
    def main(fname, root):
        which_homonymy(fname, root)
        count_homonymy(fname, root)
        trigrams(fname, root)
        bigrams(fname, root)
        monograms(fname, root)

    number_of_homo = 0
    global number_of_homo
    tags = 0
    global tags
    tokens = 0
    global tokens
    dict_of_homo = {}
    global dict_of_homo
    dict_of_words = {}
    global dict_of_words
    trigr_count = {}
    global trigr_count
    trigr_ex = {}
    global trigr_ex
    bigr_count = {}
    global bigr_count
    bigr_ex = {}
    global bigr_ex
    monogr_count = {}
    global monogr_count
    monogr_ex = {}
    global monogr_ex
    bigr_words_ex = {}
    global bigr_words_ex
    bigr_words_count = {}
    global bigr_words_count
    trigr_words_ex = {}
    global trigr_words_ex
    trigr_words_count = {}
    global trigr_words_count
    

    l = codecs.open('log.txt', 'w', 'utf-8')
    global l
    for root, dirs, files in os.walk(u'.'):
        for fname in files:
            if fname.endswith(u'.xhtml'):
##                print fname
                main(fname, root)
##                print number_of_homo
##                print 'tokens', tokens, ', tags', tags
##                print tags/tokens
##                print '\n'
        for dirname in dirs:
            root = root + '/' + dirname
##    print number_of_homo
##    print 'tokens', tokens, ', tags', tags
##    print tags/tokens
    z = codecs.open('Overall%s.txt' % turn, 'w', 'utf-8')
    z.write(str(number_of_homo) + '\n' + 'tokens ' + str(tokens) + 'tags ' + str(tags) + '\n' + str(tags/tokens))
##    homo_stat = codecs.open('Homonymy_statistics%s.csv' % turn, 'w', 'utf-8-sig')
##    for homo in sorted(dict_of_homo.keys(), key = lambda k: dict_of_homo[k]):
##        homo_stat.write(homo + ';' + str(dict_of_homo[homo]) + '\r\n')
##    word_stat = codecs.open('Homonymous_word_statistics%s.csv' % turn, 'w', 'utf-8')
##    for word in sorted(dict_of_words.keys(), key = lambda k: dict_of_words[k]):
##        word_stat.write(word + ';' + str(dict_of_words[word]) + '\r\n')
    trigr_stat = codecs.open('Trigrams_statistics%s.csv' % turn, 'w', 'utf-8-sig')
    for tr in sorted(trigr_count.keys(), key = lambda k: trigr_count[k]):
##        trigr_stat.write(trigr + ';' + str(trigr_count[trigr]) + '\r\n')
        line = tr + '^'
        for example in trigr_ex[tr]:
            line += example + '|'
        line = line[:-1] + '^'
        line += str(trigr_count[tr]) + '\n'
        trigr_stat.write(line)
##    trigr_words_stat = codecs.open('Trigrams_words_statistics.csv', 'w', 'utf-8-sig')
##    for tr in sorted(trigr_words_count.keys(), key = lambda k: trigr_words_count[k]):
####        trigr_stat.write(trigr + ';' + str(trigr_count[trigr]) + '\r\n')
##        line = tr[0] + '^' + tr[1] + '^'
##        for example in trigr_words_ex[tr]:
##            line += example + '|'
##        line = line[:-1] + '^'
##        line += str(trigr_words_count[tr]) + '\n'
##        trigr_words_stat.write(line)
    bigr_stat = codecs.open('Bigrams_statistics%s.csv' % turn, 'w', 'utf-8-sig')
    for b in sorted(bigr_count.keys(), key = lambda k: bigr_count[k]):
##        trigr_stat.write(trigr + ';' + str(trigr_count[trigr]) + '\r\n')
        line = b + '^'
        for example in bigr_ex[b]:
            line += example + '|'
        line = line[:-1] + '^'
        line += str(bigr_count[b]) + '\n'
        bigr_stat.write(line)
##    bigr_words_stat = codecs.open('Bigrams_words_statistics.csv', 'w', 'utf-8-sig')
##    for b in sorted(bigr_words_count.keys(), key = lambda k: bigr_words_count[k]):
####        trigr_stat.write(trigr + ';' + str(trigr_count[trigr]) + '\r\n')
##        line = b[0] + '^' + b[1] + '^'
##        for example in bigr_words_ex[b]:
##            line += example + '|'
##        line = line[:-1] + '^'
##        line += str(bigr_words_count[b]) + '\n'
##        bigr_words_stat.write(line)
##    monogr_stat = codecs.open('Monograms_statistics.csv', 'w', 'utf-8-sig')
##    for m in sorted(monogr_count.keys(), key = lambda k: monogr_count[k]):
####        trigr_stat.write(trigr + ';' + str(trigr_count[trigr]) + '\r\n')
##        line = m[0] + u'^' + m[1] + '^'
##        for example in monogr_ex[m]:
##            line += example + u'|'
##        line = line[:-1] + u'^'
##        line += str(monogr_count[m]) + '\n'
##        monogr_stat.write(line)
##    word_stat.close()
##    homo_stat.close()
    trigr_stat.close()
    bigr_stat.close()
##    monogr_stat.close()
##    bigr_words_stat.close()
##    trigr_words_stat.close()
    l.close()
    
    

if __name__ == '__main__':
    every(1)
