import codecs, os, re

def change(number):
    if number == 1:
        wanted = 'Monograms'
        unwanted1 = 'Bigrams'
        unwanted2 = 'Trigrams'
        unwanted3 = 'Bwords'
        unwanted4 = 'Trwords'
    elif number == 2:
        wanted = 'Bigrams'
        unwanted1 = 'Monograms'
        unwanted2 = 'Trigrams'
        unwanted3 = 'Bwords'
        unwanted4 = 'Trwords'
    elif number == 3:
        wanted = 'Trigrams'
        unwanted1 = 'Monograms'
        unwanted2 = 'Bigrams'
        unwanted3 = 'Bwords'
        unwanted4 = 'Trwords'
    elif number == 4:
        wanted = 'Bwords'
        unwanted1 = 'Monograms'
        unwanted2 = 'Bigrams'
        unwanted3 = 'Bigrams'
        unwanted4 = 'Trwords'
    elif number == 5:
        wanted = 'Trwords'
        unwanted1 = 'Monograms'
        unwanted2 = 'Bigrams'
        unwanted3 = 'Bwords'
        unwanted4 = 'Trigrams'
    p = codecs.open('Now_substitute.py', 'r', 'utf-8')
    program = ''
    for line in p:
        if line.startswith('##'):
            if wanted in line:
                line = line.replace('##', '')
        if not line.startswith('##') and (unwanted1 in line or unwanted2 in line or unwanted3 in line or unwanted4 in line):
            program += '##' + line      
        else:
            program += line
    p.close()
    n = codecs.open('Now_substitute.py', 'w', 'utf-8')
    n.write(program)
    n.close()

    
