#!/bin/env python3

from pybloomfilter import BloomFilter
import re

class List:
    """
    Class to read lists from disk, create regex and bloom filters, and finally write them back to disk on crawl completion
    """
    def __init__(self, path):
        print("Loading "+path+"...")
        self.path = path
        with open(path) as f:
            array = f.readlines()
        array = [x.strip() for x in array]
        array = list(set(array))
        self.array = array
        if path == "exclude.txt":
            self.regex = re.compile('(?:% s)' % '|'.join(self.array))
        self.bloom = BloomFilter(10000000, 0.01)
        self.bloom.update(self.array)

    def append(self, element):
        self.bloom.add(element)
        self.array.append(element)

    def concat(self, elements):
        self.array += elements

    def write(self):
        with open(self.path, 'w') as f:
            for item in self.array:
                f.write("%s\n" % item)


def trim(todo):
    """
    Removes already seen urls and excluded urls from given list
    """
    todo = [i for i in todo if not exclude.regex.search(i)]
    todo = [i for i in todo if not i in seen.bloom]
    return todo


def cleanup():
    """
    Writes lists back to disk
    """
    print("Writing lists back to disk...")
    todo.write()
    found.write()
    seen.write()
    sinners.write()
    corporates.write()
    exclude.write()
    domains.write()
    print("Exiting...")


print("Loading lists from disk...")
todo = List('todo.txt')
found = List('found.txt')
seen = List('seen.txt')
sinners = List('sinners.txt')
corporates = List('corporates.txt')
exclude = List('exclude.txt')
domains = List('domains.txt')
todo.array = trim(todo.array)
print("Load complete")
