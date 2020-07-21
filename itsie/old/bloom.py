#!/bin/env python3

from pybloomfilter import BloomFilter
import re

bf = BloomFilter.open('seen.bloom')
# bf = BloomFilter(10000000, 0.01, 'seen.bloom')
# with open("corporates.txt") as f:
#     for word in f:
#         bf.add(word.rstrip())

# bf.add('sketchywebsite.net')

domain = "https://splitbrain.org/"

#reg = re.compile(r'https?://(?:[a-z]+?\.)?(?:www\.)?([a-zA-Z0-9]+?\.[a-z]+)')
#if reg.match(url):
    #domain = reg.findall(url)[0]
#else:
    #domain = url

print(domain in bf)
