#!/bin/env python3

import lists
import re
import console

class UrlValidationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def validate(url):
    reg = re.compile(r'https?://(?:[a-z]+?\.)?(?:www\.)?([a-zA-Z0-9]+?\.[a-z]+)')
    if reg.match(url):
        domain = reg.findall(url)[0]
    else:
        domain = url
    if url in lists.indexed:
        raise UrlValidationError("Already Indexed")
        # return False, "Already Indexed"
    if lists.domains.count(domain) > 15:
        raise UrlValidationError("Domain Capped")
        # return False, "Domain capped"
    if re.findall(lists.exclude.regex_string, url):
        raise UrlValidationError("URL found in exclude")
        # return False, "URL found in exclude"
    elif re.findall(lists.sinners.regex_string, url):
        raise UrlValidationError("URL found in sinners")
        # return False, "URL found in sinners"
    elif re.findall(lists.corporates.regex_string, url):
        raise UrlValidationError("URL found in corporates")
        # return False, "URL found in corporates"
    elif '?' in url:
        raise UrlValidationError("PHP query in URL")
        # return False, "PHP query in URL"
    else:
        lists.domains.append(domain)
        lists.valid.append(url)
        return True

# def validate(url):
    # reg = re.compile(r'https?://(?:[a-z]+?\.)?(?:www\.)?([a-zA-Z0-9]+?\.[a-z]+)')
    # if reg.match(url):
    #     domain = reg.findall(url)[0]
    # else:
    #     domain = url
    # if check(url, domain)[0]:
    #     return True
    # else:
    #     console.console("OKBLUE", "Skipping", url, check(url)[1])
    #     return False



if __name__ == '__main__':
    import sys
    print(validate(sys.argv[1]))
