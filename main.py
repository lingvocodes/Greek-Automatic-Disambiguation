# coding: utf-8

from __future__ import division
import os, codecs, re, time
from lxml import etree
from collections import defaultdict

#***********************#
#   0 - statistics 1    #
#***********************#
print 'statistics 1', time.asctime()
from statistics import every
every('1')

#*********************#
#   1 - interactive   #
#*********************#

print 'interactive', time.asctime()
from Now_substitute_trigrams import substitute
substitute()
from Now_substitute_bigrams import substitute
substitute()

#*******************#
#   2 - bigrams     #
#*******************#

print 'bigrams', time.asctime()
from unamb_bigrams import every
every()
from bigrams_disamb import every
every()


#*******************#
#   3 - Brill       #
#*******************#

print 'Brill', time.asctime()
from ultimate import Transformation, BrillTrainer
# NB!!! PATH
directory = os.getcwd()
m = BrillTrainer()
m.make_POS_file(directory, '.xhtml', printing=True)
m.run_brill(printRules=True, maximum=600)
m.start_apply(directory, '.xhtml')


#***********************#
#   3' - statistics 2   #
#***********************#

print 'statistics 2', time.asctime()
from statistics import every
every('2')
