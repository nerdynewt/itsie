#!/bin/env python3

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
