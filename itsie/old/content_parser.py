#!/bin/env python3

import re
import lists
from bs4 import BeautifulSoup

def compress(text):
    text = re.sub(r'[^A-Za-z ]', ' ', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\r', ' ', text)
    text = re.sub(r' +', ' ', text)
    return text


class Content:
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
        with open('found.txt', 'a') as f:
            for item in self.links:
                f.write("%s\n" % item)
