import os, codecs,re

def substitute():
##    reg = codecs.open('Monograms_regex_for_substitution.txt', 'r', 'utf-8')
##    reg = codecs.open('Bigrams_regex_for_substitution.txt', 'r', 'utf-8')
    reg = codecs.open('Trigrams_regex_for_substitution.txt', 'r', 'utf-8')
##    reg = codecs.open('Bwords_regex_for_substitution.txt', 'r', 'utf-8')
##    reg = codecs.open('Trwords_regex_for_substitution.txt', 'r', 'utf-8')

    regex = []
    for line in reg:
        line = line.strip()
        regex.append(line)
    reg.close()

    for root, dirs, files in os.walk('.'):
        # takes all the files in the folder and subfolders and writes new 'xhtml's
        for f in files:
            if f.endswith('.xhtml') and not f.endswith('-disamb.xhtml'):
                text = codecs.open(root + '/' + f, 'r', 'utf-8')
                t = text.read()
                text.close()
                for r in regex:
                    parenth = re.findall('\(', r, flags = re.I|re.U)
                    r_new = ''
                    for p in range(1, len(parenth) + 1):
                        r_new += '\\' + str(p)
                    t = re.sub(r, r_new, t, flags = re.U|re.I)
                new_text = codecs.open(f, 'w', 'utf-8')
                new_text.write(t)
                new_text.close()
        for d in dirs:
            root = root + '/' + d

if __name__ == '__main__':
    substitute()


