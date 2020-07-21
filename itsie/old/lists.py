#!/bin/env python3

from configurator import Config
from types import SimpleNamespace
import re

"""
Reads blocklists from disk and exposes them as lists or regex matches
"""

class Blacklist:
    def __init__(self, blacklist):
        self.blacklist = blacklist
        with open(self.blacklist) as f:
            self.raw_list = f.readlines()
            self.raw_list = [x.strip() for x in self.raw_list]
            self.regex_string = '(?:% s)' % '|'.join(self.raw_list)


exclude = Blacklist('exclude.txt')
sinners = Blacklist('sinners.txt')
corporates = Blacklist('corporates.txt')
with open('todo.txt') as f:
    todo = f.readlines()
    todo = [x.strip() for x in todo]
with open('done.txt') as f:
    done = f.readlines()
    done = [x.strip() for x in done]
with open('domains.txt') as f:
    domains = f.readlines()
    domains = [x.strip() for x in domains]
# todo = ['http://linas.org/']
# done = []
# domains = []
skipped = []
indexed = []
blocked = []
found = []
valid = []

# temp = temp.replace('.', '\.')
def add(url, path):
    reg = re.compile(r'https?://(?:[a-z]+?\.)?(?:www\.)?([a-zA-Z0-9]+?\.[a-z]+)')
    if reg.match(url):
        with open(path, 'a') as f:
            f.write(reg.findall(url)[0]+'\n')
