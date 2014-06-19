import codecs, re, os

def monograms():

    dic_monogr = {}
    dic_freq = {}
    d = []
    regex = []
    did = []
    try:
        done = codecs.open('Monograms_did_it.txt', 'r', 'utf-8')
        for line in done:
            line = line.strip().split(';')
            did.append((line[0], line[1]))
        done.close()
    except:
        pass

    # reads the dictionary from a prepared file
    dic = codecs.open('Monograms_statistics.csv', 'r', 'utf-8')
    for line in dic:
        line = line.split('^')
        w = line[0]
        h = line[1]
        ex = line[2]
        freq = line[3].strip()
        dic_monogr[(w, h)] = ex
        dic_freq[(w, h)] = freq
        d.append((w, h))

    for i in d[12400::-1]:
        if i not in did:
            # goes from the end, so that the most frequent trigrams are the first ones.
            print 'You have a monogram of type ' + i[0] + ' - ' + i[1]
            print 'There are ' + dic_freq[i] + ' incidences of this monogram in the dictionary.'
            print '~~~~~~~~~~~~~~~~~~~'
            print 'Look at the second word and decide which of the variants is correct: '
            homo = i[1].split('-')
            for h in range(len(homo)):
                print str(h + 1) + '. ' + homo[h]
            print '~~~~~~~~~~~~~~~~~~~'
            print 'Consult the examples if necessary: '
            #(the word under consideration is marked with \'~\'): '
            examples = dic_monogr[i]
            examples = examples.split('|')
            for ex in range(len(examples[:3])):
                print str(ex + 1) + '. ' + examples[ex]
            print '~~~~~~~~~~~~~~~~~~~'
            action = raw_input('Input the number of the correct analysis (for example, \'2\'). ' +\
                               'If you would like to delete some analyses, enter \'d\'. ' +\
                               'If you are not sure or don\'t like this trigram, input \'0\'. ' +\
                               'If you would like to exit, input \'q\'. Please, your verdict: ')
            if action == 'q':
                break
            elif action == 'd':
                symbols = '.|?-[]()'
                deletion = raw_input('Input the numbers of analyses you want to get rid of, separated by commas' +\
                      ' in increasing order (or just the only number, for example, \'1\' or \'1,2\'): ')
                deletion = deletion.replace(' ', '')
                deleted = deletion.split(',')
                print deleted
                word = '(<w>)'
                homo_to_delete = []
                for d in deleted:
                    homo_to_delete.append(homo[int(d) - 1])
                symbols = '.|?-[]()'
                for h in homo:
                    for symbol in symbols:
                        h = h.replace(symbol, '\\' + symbol)
                    if h in homo_to_delete:
                        word += '<ana lex="[^"]*" gr="' + h + '"[^>]*></ana>'
                    else:
                        word += '(<ana lex="[^"]*" gr="' + h + '"[^>]*></ana>)'
                word += '([^<]*</w>[^<]*)'
                s = word
                regex.append(s)
            elif action == '0':
                print '\n\n'
                continue
            else:
                symbols = '.|?-[]()'
                # escaping characters for regular expressions
                correct = homo[int(action) - 1]
                print correct
                for symbol in symbols:
                    correct = correct.replace(symbol, '\\' + symbol)
                ana = i[1].split('-')
                word2 = '(<w>)'
                # builds regular expression for the substitution; parts that we'll need are in ().
                for a in ana:
                    for symbol in symbols:
                        a = a.replace(symbol, '\\' + symbol)
                    if a == correct:
                        word2 += '(<ana lex="[^"]*" gr="' + a + '"[^>]*></ana>)'
                    else:
                        word2 += '<ana lex="[^"]*" gr="' + a + '"[^>]*></ana>'
                word2 += '([^<]*</w>[^<]*)'
                s1 = word2
                regex.append(s1)
                did.append(i)
            print '\n\n'
    reg = codecs.open('Monograms_regex_for_substitution.txt', 'a', 'utf-8')
    done = codecs.open('Monograms_did_it.txt', 'a', 'utf-8')
    for r in regex:
        reg.write(r + '\r\n')
    for d in did:
        done.write(d[0] + ';' + d[1] + '\r\n')
    reg.close()
    dic.close()
    done.close()

if __name__ == '__main__':
    monograms()
