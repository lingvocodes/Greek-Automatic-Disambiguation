import codecs, re, os
from change_program import change

goal = raw_input('Hey, I\'m a jinn and will grant your wish. What do you want?\n' +\
                 'If you want to disambiguate by words, enter \'words\'. \n' +\
                 'If you want to disambiguate by bigrams, enter \'bigrams\'. \n' +\
                 'If you want to disambiguate by trigrams, enter \'trigrams\'. \n' +\
                 'If you want to disambiguate by word occurences in bigrams, enter \'bwords\'. \n' +\
                 'If you want to disambiguate by word occurences in trigrams, enter \'trwords\'. \n' +\
                 'If you don\' want anything from me, enter \'q\'. ' +\
                 'Ok, let\'s go: ')
if goal == 'words' or goal == 'bigrams' or goal == 'trigrams' or goal == 'bwords' or goal == 'trwords':
    if goal == 'words':
        change(1)
        from Monograms_data_for_substitution import monograms
        monograms()
    elif goal == 'bigrams':
        change(2)
        from Bigrams_data_for_substitution import bigrams
        bigrams()
    elif goal == 'bwords':
        change(4)
        from Bigrams_words_data_for_substitution import bigrams_words
        bigrams_words()
    elif goal == 'trwords':
        change(5)
        from Trigrams_words_data_for_substitution import trigrams_words
        trigrams_words()
    elif goal == 'trigrams':
        change(3)
        from Trigrams_data_for_substitution import trigrams
        trigrams()
    want_to_substitute = raw_input('\nDo you want to execute substitution right now? ' +\
                                   '(enter \'yes\' or \'no\') ')
    if want_to_substitute == 'yes':
        from Now_substitute import substitute
        substitute()
    elif want_to_substitute == 'no':
        print 'Okay.'
        quit
elif goal == 'q':
    quit
