"""
This is supposed to be a docstring one day.
But for now it's just a trashcan.


# Running BrillTrainer

# Creating an instance of the class

m = BrillTrainer()

# Step 1.
# Defining the directory with corpus files, the extension of corpus files.
# You may pass printing=True as one of the arguments of this function to print the created corpus to file.
# The bigger the files in the directory are, the more transformations are generated.

m.make_POS_file(path, '.xhtml', printing=True)

# Step 2.
# Starts collecting transformations.
# printRules=True - for writing list of rules to file.
# printCorp=True - for writing the transformed corpus to file.
# maximum - to limit the maximum number of transformations.

m.run_brill(printRules=True, maximum=300)

# Step 3.
# Applies learned transformations to the files in the given directory that have the given extension.
# If the parameter "rules" is specified with path to list of transformations,
# the function opens the file and applies the rules extracted from it
# (which allows to skip steps 1 and 2 if a list of transformations is available).

m.start_apply(path, '.xhtml', rules=path)
"""

import os
import re
import time
import codecs
from lxml import etree
from collections import defaultdict


#*****************************#
# Disambiguation - Bigrams    #
#*****************************#

class GoodBigramsTrainer():
    """
    Disambiguating texts with bigrams.
    GoodBigramsTrainer searches corpus with homonimy and collects statistical information about non-ambiguous bigrams.
    Then it is possible to use this information to cope with the resting homonimy.
    """

    goodBigrs = []

    def __init__(self, path, extension, printing=False):
        """
        Starts the search.

        path: unicode string containing the path to the directory where the corpus files are stored
        extension: unicode string containing the ending of the filename, e.g. '.xhtml' or 'cheese.txt',
                   this helps to identify files that need to be searched
        printing: True or False,
                  False by default,
                  if the value is True, all bigrams are printed to file *good_bigrams.txt*
        """
        print 'Collecting good bigrams...'
        for root, dirs, files in os.walk(path):
            for fName in files:
                if fName.endswith(extension):
                    self.search_file(os.path.join(root, fName))
        print 'Good bigrams collected.\r\n'
        if printing:
            f = codecs.open(u"good_bigrams.txt", "a", "utf-8")
            f.write('\r\n'.join(self.goodBigrs))
            f.close()

    def search_file(self, fName):
        """
        Performs the search of good bigrams in a given file fName.
        Writes the result to the array goodBigrs.
        """
        try:
            root = etree.parse(fName).getroot()
            gram = []
            for se in root[1]:
                for w in range(len(se) - 1):
                    new_x = [ana for ana in se[w] if "lex" in ana.attrib]
                    new_x2 = [ana for ana in se[w + 1] if "lex" in ana.attrib]
                    arr1pos = [x.attrib["gr"].split(u',')[0] for x in new_x]
                    arr2pos = [x.attrib["gr"].split(u',')[0] for x in new_x2]
                    if len(new_x) == 1 and len(new_x2) == 1:
                        gram.append((new_x[0].tail, new_x[0].attrib[u'gr'],
                                     new_x2[0].tail, new_x2[0].attrib[u'gr']))
                    elif (len(new_x) == 2 and "PR" in arr1pos and "PRO"
                          in arr1pos) or (len(new_x2) == 2 and "PR" in arr2pos and "PRO" in arr2pos):
                        gram.append((new_x[-1].tail, new_x[-1].attrib[u'gr'],
                                     new_x2[-1].tail, new_x2[-1].attrib[u'gr']))

            for i in gram:
                bigramString = i[0] + ' ' + i[1] + ' ' + i[2] + ' ' + i[3]
                self.goodBigrs.append(bigramString)

        except:
            print "Class - GoodBigrams; function - search_file(filename); fail at %s" % fName

    def count_freq(self, printing=True):
        """
        Opens array with bigrams and counts frequency for each bigram.
        Returns a dictionary { bigram:frequency }.

        printing: True or False,
                  False by default,
                  if the value is True, all bigrams with frequencies are printed to file
                  *good_bigrams_frequency_morpho.txt*
        """
        print 'Counting frequencies...\r\n'
        d = defaultdict(int)
        for line in self.goodBigrs:
            line = line.split()
            d[line[1] + ' ' + line[3]] += 1
        if printing:
            f2 = codecs.open(u"good_bigrams_frequency_morpho.txt", "w", "utf-8")
            # writes "ana1 ana2" freq
            for key in reversed(sorted(d.keys(), key=lambda k: d[k])):
                f2.write(key + ' ' + str(d[key]) + u'\r\n')
            f2.close()
        return d

    def get_rules(self, freqs):
        """
        Opens dictionary with frequencies and rearranges it into dictionary of rules.

        Returns dictionary:
        dictionary = {anaOfWord1:[(anaOfWord2,freq),(anaOfWord3,freq),...],
                      anaOfWord1:[(anaOfWord2,freq),(anaOfWord3,freq),...],
                      anaOfWord1:[(anaOfWord2,freq),(anaOfWord3,freq),...],}
        """
        d = defaultdict(list)
        for key in freqs:
            items = key.split(' ')
            items = (items[0], items[1], freqs[key])  # ana1 ana2 freq
            d[items[0]].append((items[1], int(items[2])))
        return d

    def get_predefined(self):  # FUNCTION DOES NOT WORK
        # opens file with frequent words
        f2 = codecs.open(u'C:/Users/asus/PycharmProjects/yiddish/24.02.2014/words2.txt', 'r', 'utf-8')
        d = {}
        for line in f2:
            items = line.strip('\r\n').split(' | ')
            d[items[1].strip()] = items[0].strip()
        f2.close()
        return d

    def check_for_special_cases(self, new_x):
        stay = ""
        decide = ""
        arr = [x.attrib["gr"].split(u',')[0] for x in new_x]
        try_set = set(arr)
        if len(try_set) == 2:
            if ("PREP" in try_set) and ("PRON" in try_set):
                stay = "PREP"
            else:
                return None
            arr2 = [x for x in new_x if stay not in x.attrib["gr"]]
            arr3 = [x for x in new_x if stay in x.attrib["gr"]]
            if len(arr2) == 1:
                decide = "continue"
            return stay, decide, arr2, arr3
        else:
            return None

    def get_corpora(self, fname, check, predef):

        root = etree.parse(fname).getroot()  # get a text from the corpus

        for se in root[1]:
            for w in range(len(se)):
                var = 0
                max_f = 0
                new_x = [ana for ana in se[w]]  # array contains all anas of current word
                if len(new_x) > 1:  # if the word has multiple anas
                    # ------- these several lines do not work
                    cur_w = new_x[-1].tail  # current word
                    if cur_w in predef.keys():
                        print predef
                        parser = etree.XMLParser(remove_blank_text=True)
                        se[w] = etree.XML(predef[cur_w], parser)
                        se[w][-1].tail = cur_w
                        print etree.tostring(se[w], pretty_print=True, encoding=unicode)
                        continue
                    # ------ the end of the not-working-code
                    answer = self.check_for_special_cases(new_x)
                    if answer is not None:
                        if answer[1] == "continue":
                            continue
                        new_x = answer[2]  # MAY HAVE AN ERROR HERE!!
                    for i in xrange(len(se[w])):  # ==for ana in word:
                        se[w].remove(se[w][0])  # deleted all ana from the tree
                    if answer is not None:
                        for i in answer[3]:
                            se[w].append(i)
                            var += 1
                    # At this point, we added all ana containing PREP in PRON\PREP complexes
                    # or all ana containing AVD in verbs with prefixes like aroysgeyn.
                    # hence - need to disambiguate the resting part
                    try:
                        prevAnaList = [ana for ana in se[w - 1]]
                        if len(prevAnaList) == 1:  # if the previous word has one ana
                            for ana in se[w - 1]:
                                prev = ana.attrib[u'gr'] # ana1
                                # got ana of the previous word
                            try:
                                d = {}
                                for k in check[prev]:
                                    # look for all possible anas after the previous one
                                    for analysis in new_x:
                                        if k[0] == analysis.attrib[u'gr']:
                                            # search in the dictionary, find anas suggested by morphological parser
                                            d[k[0]] = (k[1], analysis)  # write to the dictionary
                                for x in d.keys():  # searching the most frequent ana
                                    if d[x][0] > max_f:
                                        max_f = d[x][0]
                                for x in d.keys():
                                    if d[x][0] == max_f:
                                        d[x][1].tail = None
                                        se[w].append(d[x][1])
                                        #write best ana
                            except KeyError:
                                # print "No key in dictionary"
                                pass
                    except KeyError:
                        # print "No previous word"
                        pass
                    if len(se[w]) == var:
                        for i in new_x:
                            se[w].append(i)
                    else:
                        se[w][-1].tail = cur_w

        return etree.tostring(root, pretty_print=True, encoding=unicode)

    def start_apply(self, path, extension, freq):
        check = self.get_rules(freq)  # dictionary
        predef = self.get_predefined()
        # print predef
        for root, dirs, files in os.walk(path):  # (u'./yiddish_parsed_data_xhtml'):
            for fname in files:
                if fname.endswith(extension):
                    print "Applying bigrams to %s" % os.path.join(root, fname)
                    new_text = self.get_corpora(os.path.join(root, fname), check, predef)
                    f2 = codecs.open(os.path.join(root, '_2_' + fname), 'w', 'utf-8')
                    header = '<?xml version="1.0" encoding="utf-8"?>\r\n'
                    f2.write(header)
                    f2.write(new_text)
                    f2.close()


#*****************************#
# Disambiguation - Brill      #
#*****************************#
class Transformation():
        """
        This is created merely for storing information.
        """

        def __init__(self):
            self.score = 0
            self.rule = u''
            self.meta = ''

class BrillTrainer():
    """
    Part of Speech Disambiguation with Transformation-Based Learning.
    Has four templates checking 1 word or tag before or after the current word.
    Initializes with a directory with corpus files for generating transformations and ending of the files.
    """

    nums = 0
    orderedList = []
    frequencies = defaultdict(int)

    def __init__(self):
        print "BrillTrainer instance created."
        self.corpus = []

    def make_POS_file(self, path, extension, printing=True):
        """
        Takes a directory with corpus xhtml-files and makes one huge txt out of all texts.
        All words in the united document have POS-tags.

        path: unicode string containing the path to the directory where the corpus files are stored
        extension: unicode string containing the ending of the filename, e.g. '.xhtml' or 'cheese.txt',
                   this helps to identify files that need to be searched
        printing: True or False,
                  False by default,
                  if the value is True, the unified POS-tagged document is printed to file *corpus.txt*
        """
        self.nums = 0
        print 'BrillTrainer instance. Creating txt version of corpus with POS-tags...'
        for root, dirs, files in os.walk(path):
            for fname in files:
                if fname.endswith(extension):
                    self.transform_file(os.path.join(root, fname))
                    print '    ', fname, 'found %s words so far' % self.nums
        print 'Corpus created.\r\n'
        if printing:
            fOut = codecs.open('corpus.txt', 'a', 'utf-8-sig')
            fOut.write('\r\n'.join(self.corpus))
            fOut.close()

    def transform_file(self, fname):
        """
        Takes one file and adds its content to the unified document.
        """
        root = etree.parse(fname).getroot()  # get a text from the corpus
        for se in root[1]:
            sent = u''
            for w in xrange(len(se)):
                try:
                    curWord = se[w][-1].tail
                except:
                    print etree.tostring(se[w], encoding = unicode)
                new_x = [ana for ana in se[w]]
                for i in xrange(len(se[w])):  # ==for ana in word:
                    se[w].remove(se[w][0])  # deleted all ana from the tree
                for i in xrange(len(new_x)):
                    try:
                        new_x[i] = new_x[i].attrib['gr']
##                        if new_x[i].startswith("PRON"):
##                            new_x[i] = ':'.join(new_x[i].split(',')[:2])
##                        else:
##                            new_x[i] = new_x[i].split(',')[0]
##                        new_x[i] = re.sub(r"\?", "", new_x[i])
                    except:
                        new_x[i] = 'ND'
                new_x = list(set(new_x))
                tag = "_".join(sorted(new_x))
                tag = re.sub("PREP_PRON:A", "PREP+PRON:A", tag)
                tag = re.sub("ADV_V", "ADV+V", tag)
                curWord += '^' + tag + ' '
                sent += curWord
                self.nums += 1
            self.corpus.append(sent)

    def run_brill(self, printRules=True, printCorp=True, maximum=500):
        """
        Starts brill disambiguation algorithm.
        Returns ordered list of transformations.

        printRules: True or False, False by default,
                  if the value is True, the list of transformations is printed to file *list-of-transformations.txt*
        printCorp: True or False, False by default,
                    if the value is True, the transformed POS-tagged document is printed to file
                    *corpus-transformed.txt*
        """
        corpus = self.corpus
        print 'Collecting transformations... ', time.asctime()
        templates = [(-1, 'tag'), (+1, 'tag'), (-1, 'word'), (+1, 'word')]
        while True:
            self.frequencies = self.freq(corpus)
            bestTransform = self.get_best_transform(templates)
            if not (bestTransform.score > 0):
                break
            corpus = self.apply_transformation(bestTransform, corpus)
            self.orderedList.append(bestTransform.rule)
            if len(self.orderedList) >= maximum:
                break
            if len(self.orderedList) % 100 == 0:
                print 'Found %s transformations so far.' % len(self.orderedList), time.asctime()
        print 'Ready. Collected all transformations.', time.asctime()
        print 'Found %s transformations.\r\n' % len(self.orderedList)
        if printRules:
            transformOut = codecs.open(u'list-of-transformations.txt', 'w', 'utf-8-sig')
            transformOut.write('\r\n'.join(self.orderedList))
            transformOut.close()
        if printCorp:
            corpusOut = codecs.open(u'corpus-transformed.txt', 'w', 'utf-8-sig')
            corpusOut.write('\r\n'.join(corpus))
            corpusOut.close()
        return self.orderedList

    def get_best_transform(self, templates):
        """
        Iterates over all templates and returns the best transformation for the current state of the corpus.
        """
        # print 'function get_best_transform', time.asctime()
        best = Transformation()
        for template in templates:
            curTransform = self.get_best_instance(template)
            if curTransform.score > best.score:
                best = curTransform
        return best

    def open_fromTags(self):
        # print 'function open_fromTags', time.asctime()
        fromTags = []
        for k in self.frequencies[0].keys():
            if '_' in k:
                fromTags.append(k)
        return fromTags

    def generate_context(self, froms, template):
        # print 'function generate_context', time.asctime()
        contexts = []
        nums = template[0]  # -1 or +1
        types = template[1]  # word or tag
        if types == "word":
            if nums == 1:
                contexts = [(nums, types, w) for w in self.frequencies[1][froms].keys()]
            elif nums == -1:
                contexts = [(nums, types, w) for w in self.frequencies[3][froms].keys()]
        elif types == "tag":
            if nums == 1:
                contexts = [(nums, types, w) for w in self.frequencies[2][froms].keys()]
            elif nums == -1:
                contexts = [(nums, types, w) for w in self.frequencies[4][froms].keys()]
        return contexts

    def get_best_instance(self, template):
        # print 'function get_best_instance', time.asctime()
        best = Transformation()
        fromTags = self.open_fromTags()
        for fromTag in fromTags:  # fromTags = all types of POS-homonymy in our corpus, e.g. N_A_PRON
            toTags = fromTag.split('_')

            contexts = self.generate_context(fromTag, template)

            for toTag in toTags:  # toTags = parts of multiple tag, e.g. N, A, PRON for N_A_PRON
                for context in contexts:  # (nums, types, item)
                    arrZ = [(toTag, tag, context) for tag in toTags if tag != toTag]
                    bestZ = max(arrZ, key=self.estimate)
                    new_score = self.inContext(toTag, context) - self.estimate(bestZ)
                    if new_score > best.score:
                        # new_rule = u"Change " + fromTag + u" to " + toTag + u" if "
                        new_rule = fromTag + u"\t" + toTag + u"\t"
                        new_rule += str(bestZ[2][0]) + u'\t' + bestZ[2][1] + u'\t' + bestZ[2][2]
                        if new_rule not in self.orderedList:
                            best.rule = new_rule
                            best.score = new_score
                            best.meta = (fromTag, toTag, bestZ[2])
        return best

    def apply_transformation(self, bestTransform, corpus):
        # print 'function apply_transformation', time.asctime()
        nums, types, item = bestTransform.meta[2]
        fromTag = bestTransform.meta[0]
        toTag = bestTransform.meta[1]
        if types == 'word':
            types = 0  # word or tag
        elif types == 'tag':
            types = 1
        for se in xrange(len(corpus)):
            corpus[se] = corpus[se].split()
            for word in xrange(len(corpus[se])):
                w = corpus[se][word].split('^')
                if w[1] == fromTag:
                    if (nums == -1 and word != 0) or (nums == 1 and word != len(corpus[se]) - 1):
                        w_other = corpus[se][word + nums].split('^')
                        if w_other[types] == item:
                            corpus[se][word] = re.sub(fromTag, toTag, corpus[se][word])
            corpus[se] = ' '.join(corpus[se])
        return corpus

    def freq(self, corpus):
        # print 'function freq', time.asctime()
        d = defaultdict(int)
        word_next, word_prev, tag_next, tag_prev = defaultdict(dict), defaultdict(dict), defaultdict(
            dict), defaultdict(dict)
        for line in corpus:
            line = line.split()
            for word in xrange(len(line)):
                try:
                    cur_w, cur_tag = line[word].split('^')
                    d[cur_tag] += 1
                    if d[cur_tag] == 1:
                        word_next[cur_tag], word_prev[cur_tag], tag_next[cur_tag], tag_prev[cur_tag] = defaultdict(
                            int), defaultdict(int), defaultdict(int), defaultdict(int)
                except:
                    continue
            if word != len(line) - 1:
                try:
                    w_next, t_next = line[word + 1].split('^')
                    word_next[cur_tag][w_next] += 1
                    tag_next[cur_tag][t_next] += 1
                except:
                    continue
            if word != 0:
                try:
                    w_prev, t_prev = line[word - 1].split('^')
                    word_prev[cur_tag][w_prev] += 1
                    tag_prev[cur_tag][t_prev] += 1
                except:
                    continue
        return d, word_next, tag_next, word_prev, tag_prev

    def inContext(self, tag, context):
        #(tag, (num, types, item))
        nums = context[0]  # -1 or +1
        if context[1] == 'word':
            if nums == 1:
                d = self.frequencies[1]
            elif nums == -1:
                d = self.frequencies[3]
        elif context[1] == 'tag':
            if nums == 1:
                d = self.frequencies[2]
            elif nums == -1:
                d = self.frequencies[4]
        item = context[2]  # word or tag
        try:
            result = d[tag][item]
            # number of times a word unambiguously tagged with tag occurs in context in the corpus
        except:
            result = 0
        return result

    def estimate(self, tup):
        # print 'function estimate', time.asctime()
        toTag, tag, context = tup
        fY, fZ = self.frequencies[0][toTag], self.frequencies[0][tag]
        contextZC = self.inContext(tag, context)
        if fZ == 0:
            return 0
        else:
            return float(fY) / fZ * contextZC

    #APPLYING BRILL

    def start_apply(self, path, extension, rules=''):
        fileNum = 1
        if rules != '':
            rules = self.open_transformations(rules)
        else:
            rules = self.orderedList
        print 'Applying learned transformations to directory %s...' % path
        for root, dirs, files in os.walk(path):
            for fname in files:
                if fname.endswith(extension):
                    p = os.path.join(root, fname)
                    print 'Processing %s , %s...' % (p, fileNum),
                    self.apply_it(p, extension, rules)
                    fileNum += 1

    def open_transformations(self, path):
        transFile = codecs.open(path, 'r', 'utf-8-sig')
        orderedList = []
        for line in transFile:
            line = line.strip()
            orderedList.append(line)
        return orderedList

    def transform_anas(self, new_x):
        arr = []
        for i in range(len(new_x)):
            try:
                a = new_x[i].attrib['gr']
##                if a.startswith("PRON"):
##                    a = ':'.join(a.split(',')[:2])
##                else:
##                    a = a.split(',')[0]
                a = re.sub(r"\?", "", a)
            except:
                a = 'ND'
            arr.append(a)
        arr = list(set(arr))
        tag = "_".join(sorted(arr))
##        tag = re.sub("PREP_PRON:A", "PREP+PRON:A", tag)
##        tag = re.sub("ADV_V", "ADV+V", tag)
        # print tag
        return tag

    def get_toTag(self, gr):
        if gr.startswith("PRON"):
            gr = ':'.join(gr.split(',')[:2])
        else:
            gr = gr.split(',')[0]
        return gr

    def apply_it(self, path, extension, rules):
        changes = 0
        root = etree.parse(path).getroot()  # get a text from the corpus
        for t in rules:
            fromTag, toTag, position, types, context = t.split('\t')
            position = int(position)
            for se in root[1]:
                for w in range(len(se)):
                    new_x = [ana for ana in se[w]]
                    try:
                        cur_w = new_x[-1].tail  # current word
                    except:
                        continue
                    for i in xrange(len(se[w])):  # ==for ana in word:
                        se[w].remove(se[w][0])  # deleted all ana from the tree
                    if len(new_x) > 1:
                        a = new_x
                        tag = self.transform_anas(a)
                        if tag == fromTag:
                            try:
                                if types == 'tag':
                                    other = self.transform_anas([ana for ana in se[w + position] if w + position != -1])
                                elif types == 'word':
                                    other = [ana for ana in se[w + position] if w + position != -1][-1].tail
                                if other == context:
                                    new_x2 = [ana for ana in new_x if
                                              ana.attrib['gr'].startswith(toTag.replace(':', ','))]
                                    changes += 1
                                    for x in new_x2:
                                        x.tail = None
                                        se[w].append(x)
                            except IndexError:
                                pass
                            except AttributeError:
                                print [ana for ana in se[w]][-1].tail
                    if len(se[w]) == 0:
                        for i in new_x:
                            se[w].append(i)
                    else:
                        se[w][-1].tail = cur_w

        out = etree.tostring(root, pretty_print=True, encoding=unicode)
        fOut = codecs.open(path.replace(extension, extension), 'w', 'utf-8-sig')
        fOut.write(out)
        fOut.close()
        print "%s changes" % changes


#*****************************#
# Disambiguation - Rules      #
#*****************************#

class RulesTrainer():

    def __init__(self):
        self.rules = self.openRules()
        for root, dirs, files in os.walk(u'.'):
            for fname in files:
                if fname.endswith(u'.xhtml'):
                    self.applyRules(os.path.join(root, fname), self.rules)

    def openRules(self):
        root = etree.parse(u"ruleMir.xml").getroot()
        arr = []
        for rule in root[1]:
            arr.append(rule.attrib["input"])
        return root[1], arr

    def oneRule(self, cur_w, rule, se, w, new_x):
        countIf = 0
        ifResult = []
        for tag in rule:
            if tag.tag == "if":
                countIf += 1
                pos = tag.attrib["pos"].split(',')
                pos_num = [int(pos[i]) for i in range(len(pos))]
                res = []
                for n in pos_num:
                    try:
                        # HERE I NEED TO WRITE MORE, SO THAT ALL TAGS OF THE PREVIOUS WORD ARE CHECKED,
                        # NOT ONLY THE FIRST ONE
                        for y in range(len(se[w + n])):
                        # AND SO THAT PIECES OF MORPHOLOGICAL ANALYSIS ARE SEARCHED
                        # NOT AS A WHOLE ONE STRING, BUT PART BY PART
                            if (tag.text in se[w + n][y].attrib["gr"]) == tag.attrib["type"]:
                                res += True
                    except (KeyError, IndexError):
                        continue
                if True in res:
                    ifResult += True
            if (tag.tag == "do") and (len(ifResult) == countIf):
                if tag.attrib["operation"] == "set":
                    for ana in new_x:
                        if tag.text in ana.attrib["gr"]:
                            ana.tail = None
                            se[w].append(ana)
                    se[w][-1].tail = cur_w
                if tag.attrib["operation"] == "del":
                    for ana in new_x:
                        ana.tail = None
                        se[w].append(ana)
                    for ana in se[w]:
                        if tag.text in ana.attrib["gr"]:
                            ana.getparent().remove(ana)
                    se[w][-1].tail = cur_w
        return se[w]

    def applyRules(self, fname, allRules):
        arr = allRules[1]
        rules = allRules[0]
        fOut = codecs.open(fname.replace(u'.xhtml', u'CHeck.xhtml'), 'w', 'utf-8')
        root = etree.parse(fname).getroot()
        for se in root[1]:
            for w in range(len(se)):
                new_x = [ana for ana in se[w]]  # got all ana
                if len(new_x) > 1:
                    cur_w = new_x[-1].tail  # got current word
                    if cur_w in arr:
                        for i in xrange(len(se[w])):  # ==for ana in word:
                            se[w].remove(se[w][0])  # deleted all ana from the tree
                        for rule in rules:
                            if cur_w == rule.attrib["input"]:
                                se[w] = self.oneRule(cur_w, rule, se, w, new_x)
                        if len(se[w]) == 0:
                            for i in new_x:
                                se[w].append(i)
        fOut.write(etree.tostring(root, pretty_print=True, encoding=unicode))
        fOut.close()

        
##directory = os.getcwd()
##m = BrillTrainer()
####m.make_POS_file(u'F:\\курсовая\\sandbox\\new 2', '.xhtml', printing=True)
##m.make_POS_file(directory, '.xhtml', printing=True)
##m.run_brill(printRules=True, maximum=300)
##m.start_apply(directory, '.xhtml')
####m.start_apply(u'F:\\курсовая\\sandbox\\new 2', '.xhtml')
