#!/bin/env python3


import re
import tldextract
from bs4 import BeautifulSoup

import itsie.lists as lists

class ContentValidationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Content:
    """
    Parses content
    """
    def __init__(self, content, url):
        soup = BeautifulSoup(content, 'lxml')
        self.url = url
        self.content = content
        try:
            self.title = soup.title.text
        except AttributeError:
            self.title = url
        self.clean = soup.get_text()
        self.links = re.findall(r'href="(http.*?)"', content, re.IGNORECASE)
        # with open('found.txt', 'a') as f:
        #     for item in self.links:
        #         f.write("%s\n" % item)

def cdn_checker(header, domain):
    """
    detects websites running on WYSIWYG services
    """
    cdn_name = None
    asp = ['X-Powered-By: ASP.NET', "x-aspnet-version"]
    wordpress = ['x-powered-by: WP Engine', 'wp-json', 'X-Cache-Engine: WP-FFPC', 'x-powered-by Wordpress', 'wpvip.com']
    cloudflare = ['server: cloudflare', '__cfuid', 'cf-cache-status', 'cf-request-id']
    drupal = ['X-Generator: Drupal', 'X-Drupal-Cache', ]
    if header.get('cf-cache-status') or header.get('cf-request-id') or header.get('server') == 'cloudflare':
        cdn_name = 'cloudflare'
    elif header.get('server') == 'squarespace':
        cdn_name = 'squarespace'
    elif header.get('x-powered-by') == "wp engine":
        cdn_name = 'wordpress'
    elif header.get('X-Generator') == "Drupal" or header.get('x-drupal-dynamic-cache') or header.get('x-drupal-cache'):
        cdn_name = 'drupal'
    elif header.get('x-aspnet-version'):
        cdn_name = 'aspnet'
    elif header.get('link'):
        if 'wp-json' in header.get('link'):
            cdn_name = 'wordpress'
    if cdn_name:
        lists.sinners.append(domain)
        raise ContentValidationError('Uses CDN:'+cdn_name)
    else:
        return True

def corporate(text, domain):
    """
    detects corporate landing websites
    """
    newsspeak = [ 'hello' ]
    newsspeak = ['Our Products', 'Terms of Use', 'Help Center', 'About Us', 'Privacy Policy','Privacy policy', 'Code of Conduct', 'Cookie Policy', 'Privacy Agreement', 'Terms of Agreement', 'Terms &amp; Conditions', 'Terms of Service', 'Terms of service' 'Contact Us', 'Terms of Use and Disclaimer', 'Press Centre', 'PRIVACY POLICY', 'Diversity', 'Terms of use', 'Privacy statement', 'Cookie policy', 'About us', 'Press releases', 'Cookie Settings', 'Contact us', 'Careers', 'Privacy', 'Leadership', 'Terms']
    for word in newsspeak:
        if '>'+word+'<' in text or '> '+word+' <' in text:
            lists.corporates.append(domain)
            raise ContentValidationError('Found newsspeak: '+word)
    return True

def validate(content, header, url):
    domain = '.'.join(tldextract.extract(url)[1:])
    cdn_checker(header, domain)
    corporate(content, domain)
