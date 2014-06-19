import codecs, re, os

def trigrams_words():

    dic_trigr = {}
    dic_freq = {}
    d = []
    regex = []
    did = []
    try:
        done = codecs.open('Trigrams_words_did_it.txt', 'r', 'utf-8')
        for line in done:
            line = line.strip()
            d1, d2 = line.split('^')
            did.append((d1, d2))
        done.close()
    except:
        pass

    # reads the dictionary from a prepared file
    dic = codecs.open('Trigrams_words_statistics.csv', 'r', 'utf-8')
    for line in dic:
        line = line.split('^')
        h_words = line[0]
        h_grs = line[1]
        ex = line[2]
        freq = line[3].strip()
        dic_trigr[(h_words, h_grs)] = ex
        dic_freq[(h_words, h_grs)] = freq
        d.append((h_words, h_grs))

    for i in d[::-1]:
        if i not in did:
            # goes from the end, so that the most frequent trigrams are the first ones.
            print 'You have a trigram word occurences of type ' + i[0] + ' (' + i[1] + ')'
            print '(several words can be homonymous; variants are separated with "-")'
            print 'There are ' + dic_freq[i] + ' incidences of this trigram in the dictionary.'
            print '~~~~~~~~~~~~~~~~~~~'
            print 'Look at the second word and decide which of the variants is correct: '
            words = i[0].split()
            h1, h2, h3 = i[1].split('|')
            homo = h2.split('-')
            for h in range(len(homo)):
                print str(h + 1) + '. ' + homo[h]
            print '~~~~~~~~~~~~~~~~~~~'
            print 'Consult the examples if necessary: '
            #(the word under consideration is marked with \'~\'): '
            examples = dic_trigr[i]
            examples = examples.split('|')
            for ex in range(len(examples[:3])):
                print str(ex + 1) + '. ' + examples[ex]
            print '~~~~~~~~~~~~~~~~~~~'
            action = raw_input('Input the number of the correct analysis (for example, \'2\'). ' + \
                               'If you would like to delete some analyses, enter \'d\'. ' +\
                               'If you are not sure or don\'t like this trigram, input \'0\'. ' + \
                               'If you would like to exit, input \'q\'. Please, your verdict: ')
            if action == 'q':
                break
            elif action == 'd':
                symbols = '.|?-[]()'
                deletion = raw_input('Input the numbers of analyses you want to get rid of, separated by commas' +\
                      ' in increasing order (or just the only number, for example, \'1\' or \'1,2\'): ')
                deletion = deletion.replace(' ', '')
                deleted = deletion.split(',')
                symbols = '.|?-[]()'
                ana2 = homo
                word1 = word2 = word3 = '(<w>)'
                if h1 != '':
                    ana1 = h1.split('-')
                    for ana in ana1:
                        for symbol in symbols:
                            ana = ana.replace(symbol, '\\' + symbol)
                        word1 += '(<ana lex="[^"]*" gr="' + ana + '"[^>]*></ana>)'
                    word1 += '(' + words[0] + '</w>[^<]*)'
                else:
                    word1 += '(<ana></ana>)(' + words[0] + '</w>[^<]*)'
                homo_to_delete = []
                for d in deleted:
                    homo_to_delete.append(homo[int(d) - 1])
                for h in homo:
                    for symbol in symbols:
                        h = h.replace(symbol, '\\' + symbol)
                    if h in homo_to_delete:
                        word2 += '<ana lex="[^"]*" gr="' + h + '"[^>]*></ana>'
                    else:
                        word2 += '(<ana lex="[^"]*" gr="' + h + '"[^>]*></ana>)'
                word2 += '(' + words[1] + '</w>[^<]*)'
                if h3 != u'':
                    ana3 = h3.split('-')
                    for ana in ana3:
                        for symbol in symbols:
                            ana = ana.replace(symbol, '\\' + symbol)
                        word3 += '(<ana lex="[^"]*" gr="' + ana + '"[^>]*></ana>)'
                    word3 += '(' + words[2] + '</w>[^<]*)'
                else:
                    word3 += '(<ana></ana>)(' + words[2] + '</w>[^<]*)'
                s = word1 + word2 + word3
                regex.append(s)
            elif action == '0':
                print '\n\n'
                continue
            else:
                symbols = '.|?-[]()'
                # escaping characters for regular expressions
                correct = homo[int(action) - 1]
                for symbol in symbols:
                    correct = correct.replace(symbol, '\\' + symbol)
                ana2 = homo
                word1 = word2 = word3 = '(<w>)'
                # builds regular expression for the substitution; parts that we'll need are in ().
                if h1 != u'':
                    ana1 = h1.split('-')
                    for ana in ana1:
                        for symbol in symbols:
                            ana = ana.replace(symbol, '\\' + symbol)
                        word1 += '(<ana lex="[^"]*" gr="' + ana + '"[^>]*></ana>)'
                    word1 += '(' + words[0] + '</w>[^<]*)'
                else:
                    word1 += '(<ana></ana>)(' + words[0] + '</w>[^<]*)'
                for ana in ana2:
                    for symbol in symbols:
                        ana = ana.replace(symbol, '\\' + symbol)
                    if ana == correct:
                        word2 += '(<ana lex="[^"]*" gr="' + ana + '"[^>]*></ana>)'
                    else:
                        word2 += '<ana lex="[^"]*" gr="' + ana + '"[^>]*></ana>'
                word2 += '(' + words[1] + '</w>[^<]*)'
                if h3 != '':
                    ana3 = h3.split('-')
                    for ana in ana3:
                        for symbol in symbols:
                            ana = ana.replace(symbol, '\\' + symbol)
                        word3 += '(<ana lex="[^"]*" gr="' + ana + '"[^>]*></ana>)'
                    word3 += '(' + words[2] + '</w>[^<]*)'
                else:
                    word3 += '(<ana></ana>)(' + words[2] + '</w>[^<]*)'
                s1 = word1 + word2 + word3
                regex.append(s1)
                did.append(i)
            print '\n\n'
    reg = codecs.open('Trwords_regex_for_substitution.txt', 'a', 'utf-8')
    done = codecs.open('Trigrams_words_did_it.txt', 'a', 'utf-8')
    for r in regex:
        reg.write(r + '\r\n')
    for d in did:
        done.write(d[0] + '^' + d[1] + '\r\n')
    reg.close()
    dic.close()
    done.close()

if __name__ == '__main__':
    trigrams_words()
