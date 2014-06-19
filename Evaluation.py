from __future__ import division
import codecs, os, re
from lxml import etree

legend = ['method', 'ambLevelOriginal', 'ambLevelDisamb', 'ambLevelProcessed',
          'precision (%)', 'recall (%)', 'F1-measure', 'excellentWork', 'fairWork', 'badWork']
results = [legend]

##methods = ('brill_all', 'brill_pos', 'bigrams', 'trigrams')
methods = ['user_bigr', 'user_bigr_brill_all', 'ultimate', 'final']

for method in methods:
    print method, 'makedonia-87696-' + method + '.xhtml'
    excellent = 0
    good = 0
    bad = 0
    ambOrig = 0
    touch = 0
    originalTree = etree.parse('makedonia-87696-original.xhtml').getroot()
##    processedTree = etree.parse('makedonia-87696-original_' + method + '.xhtml').getroot()
    processedTree = etree.parse('makedonia-87696-' + method + '.xhtml').getroot()
    disambTree = etree.parse('makedonia-87696-disamb.xhtml').getroot()

    original = codecs.open('makedonia-87696-original.xhtml', 'r', 'utf-8')
##    processed = codecs.open('makedonia-87696-original_' + method + '.xhtml', 'r', 'utf-8')
    processed = codecs.open('makedonia-87696-' + method + '.xhtml', 'r', 'utf-8')
    disamb = codecs.open('makedonia-87696-disamb.xhtml', 'r', 'utf-8')
    orig = original.read()
    proc = processed.read()
    dis = disamb.read()

    origWords = len(re.findall('<w>', orig))
    procWords = len(re.findall('<w>', proc))
    disWords = len(re.findall('<w>', dis))
    origTags = len(re.findall('<ana', orig))
    procTags = len(re.findall('<ana', proc))
    disTags = len(re.findall('<ana', dis))
    origAmbWords = len(re.findall('(<ana[^>]*></ana>){2,}', orig))
    param = [(origWords, origTags), (procWords, procTags), (disWords, disTags)]

    for se in xrange(len(originalTree[1])):
        for word in xrange(len(originalTree[1][se])):
            try:
                anasOrig = [ana.attrib['gr'] for ana in originalTree[1][se][word]]
                anasProc = [ana.attrib['gr'] for ana in processedTree[1][se][word]]
                anasDisamb = [ana.attrib['gr'] for ana in disambTree[1][se][word]]
            except:
                anasOrig = anasProc = anasDisamb = ['-']
            if len(anasOrig) != len(anasProc):
                touch += 1
                if len(anasOrig) > 1:
                    ambOrig += 1
                if anasDisamb == []:
                    print etree.tostring(disambTree[1][se][word], encoding = unicode)
                else:
                    if anasDisamb[0] in anasProc:
                        if anasProc == anasDisamb:
                            excellent += 1
                        else:
                            good += 1
                    else:
                        bad += 1
    ambLevel = [pair[1]/pair[0] for pair in param]
    try:
        precision = excellent/touch*100
        print precision
    except:
        precision = 'Error'
    recall = touch/origAmbWords*100
    try:
        f1Measure = float(2)*float(precision)*float(recall)/(precision + recall)
    except:
        f1Measure = 'Error'
    results.append([method, ambLevel[0], ambLevel[2], ambLevel[1], precision,
                   recall, f1Measure, excellent, good, bad])

result = codecs.open('EvaluatedDisambiguation.csv', 'w', 'utf-8-sig')
result.write('Precision = correctChanges_in_Processed / allChanges_in_Processed\n' +
             'Recall = allChanges_in_Processed / allAmbTags_in_Original\n' +
             'excellentWork = correctly disambiguated\n' +
             'fairWork = partly disambiguated (still several variants, one of them is correct)\n' +
             'badWork = incorrectly disambiguated!!!\n')
for r in results:
    line = ''
    for item in r:
        line += str(item) + '\t'
    line += '\n'
    result.write(line)
result.close()
