#!/bin/env python3

import lists
import url_validator
import content_validator
import content_parser
import databaser
import requests
import pickle

bcolors = {"HEADER" : '\033[95m',
    "OKBLUE" : '\033[94m',
    "OKGREEN" : '\033[92m',
    "WARNING" : '\033[93m',
    "FAIL" : '\033[91m',
    "ENDC" : '\033[0m',
    "BOLD" : '\033[1m',
    "UNDERLINE" : '\033[4m'}

def console(color, status, url, reason):
    output = bcolors[color]+status+'\t'+bcolors["ENDC"]+url
    if reason:
        output += ' ('+bcolors[color]+reason+bcolors["ENDC"]+')'
    print(output.expandtabs(20))

newtodo = []

def cleanup():
    with open('newtodo.txt', 'w') as f:
        for item in newtodo:
            f.write("%s\n" % item)

lists.todo = list(set(lists.todo))

for i in range(0, len(lists.todo)):
    url = lists.todo[i]
    if url_validator.validate(url)[0]:
        newtodo.append(url)
        pass
    else:
        console("OKBLUE", "Skipping", url, url_validator.validate(url)[1])
        continue



print("Exiting...")
cleanup()
print("""
Crawl Job Completed
Found: %s
\033[94mSkipped:\033[0m %s
\033[92mIndexed:\033[0m %s
\033[93mBlocked:\033[0m %s
""" % (len(lists.done), len(lists.skipped), len(lists.indexed), len(lists.blocked)))
