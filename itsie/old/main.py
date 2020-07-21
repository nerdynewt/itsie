#!/bin/python

import requests
import json
import re
import sys
import mysql.connector
import url_validator


# mydb = mysql.connector.connect(
#         host = "localhost",
#         user = "vishnu",
#         password = "CrapWeasel",
#         database = "search_index"
#         )

# mycursor = mydb.cursor()


ooga = list()
ooga.append(sys.argv[1])
done = list()
alls = list()
domains = list()
jsons = list()

# with open('exclude.txt') as f:
#     exclude = f.readlines()
# with open('sinners.txt') as f:
#     exclude += f.readlines()
# with open('corporates.txt') as f:
#     exclude += f.readlines()
# exclude = [x.strip() for x in exclude]
# temp = '(?:% s)' % '|'.join(exclude)
# temp = temp.replace('.', '\.')


class Url:
    def __init__(self, raw):
        self.raw = raw
        self.title = raw
        self.valid = url_validator.validate(raw)
        self.blocked = False
        self.text = "none"
        try:
            self.domain = re.findall(r'https?://(?:[a-z]+?\.)?([a-zA-Z0-9]+?\.[a-z]+)', self.raw)[0]
        except:
            self.domain = "none"
        if domains.count(self.domain) > 15:
            self.blocked = True
            return
        domains.append(self.domain)
        if re.findall(r'https?://.*', raw):
            self.valid = True
        if re.findall(temp, raw) or '?' in raw:
            # print(re.findall(temp, raw))
            self.blocked = True
            return
        try:
            self.response = requests.get(raw)
            self.links = re.findall(r'href="(http.*?)"', self.response.text, re.IGNORECASE)
            self.ext_links = re.findall(r'href="(http.*?)"', self.response.text, re.IGNORECASE)
            # print(self.ext_links)
            # rx = re.compile(self.domain)
            # self.ext_links = [x for x in self.links if not re.findall(self.domain, x)]
            self.headers = self.response.headers
            self.text = self.response.text
            try:
                self.title = re.search('(?<=<title>).+?(?=</title>)', url.text, re.DOTALL).group().strip()
            except:
                pass
        except:
            self.valid = False
            return
        if cdn(self.headers)[1]:
            self.blocked = True
            with open('sinners.txt', 'a') as f:
                f.write(self.domain+'\n')
            return
        if corporate(self.text):
            self.blocked = True
            with open('corporates.txt', 'a') as f:
                f.write(self.domain+'\n')
            return


# def compress(text):
#     text = re.sub(r'[^A-Za-z ]', ' ', text)
#     text = re.sub(r'\n', ' ', text)
#     text = re.sub(r'\r', ' ', text)
#     text = re.sub(r' +', ' ', text)
#     return text

# def dbadd(url, title, content):
#     if not url or not title or not content:
#         return False
#     sql = "INSERT INTO search_index (url, title, content) VALUES (%s, %s, %s)"
#     val = (url, title, content)
#     mycursor.execute(sql, val)
#     mydb.commit()
#     return True



for i in range(1,20):
    # with open ('resutls.html', 'a') as f:
    #     f.write('<h1> Iteration '+str(i)+'</h1><ul>')
    while ooga:
        link = ooga.pop(0)
        url = Url(link)
        # print(re.findall(r'<title>(.*)</title>', url.text, re.MULTILINE))
        if url.valid and not url.blocked and url.raw not in done:
            with open ('resutls.html', 'a') as f:
                f.write('<li><a href="'+url.raw+'">'+url.raw+'</a></li>\n')
        with open ('search.json', 'w') as f:
            f.write(json.dumps(jsons))
            print(url.raw)
            one = {}
            one["title"] = url.title
            one["url"] = link
            one["category"] = "category"
            one["tags"] = "tags"
            one["date"] = "date"
            one["description"] = compress(url.text)
            jsons.append(one)
            print(dbadd(link, url.title, compress(url.text)))
            done.append(link)
            try:
                ooga += url.ext_links
                # print(ooga)
                alls += url.ext_links
                # print(str(json))
            except:
                pass
    # with open ('resutls.html', 'a') as f:
    #     f.write('</ul>')
            # for asdf in url.ext_links:
            #     # print(asdf)
    print(i)
