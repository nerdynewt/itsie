#!/bin/python3

from pybloomfilter import BloomFilter
import re
import tldextract

import itsie.lists as lists

class UrlValidationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def validate(url):
    """
    Makes sure url is not indexed already, blocked, etc.
    """
    domain = '.'.join(tldextract.extract(url)[1:])
    million = BloomFilter.open('million.bloom')
    if url in lists.seen.bloom:
        raise UrlValidationError("Already Indexed")
    if domain in lists.sinners.bloom:
        raise UrlValidationError("Domain in sinners")
    if domain in million:
        raise UrlValidationError("Domain too popular")
    if domain in lists.corporates.bloom:
        raise UrlValidationError("Domain in corporates")
    if lists.domains.array.count(domain) > 15:
        raise UrlValidationError("Domain Capped")
    if '?' in url:
        raise UrlValidationError("PHP query in URL")
    lists.domains.append(domain)
    lists.seen.append(url)
    return True

if __name__ == '__main__':
    import sys
    print(validate(sys.argv[1]))
