#!/bin/env python3

import lists
import url_validator
import content_validator
import content_parser
import databaser
import requests
import asyncio



newtodo = []


lists.todo = list(set(lists.todo))
urls = lists.todo

# for i in range(0, len(lists.todo)):
#     url = lists.todo[i]
#     if url_validator.validate(url)[0]:
#         newtodo.append(url)
#         pass
#     else:
#         console("OKBLUE", "Skipping", url, url_validator.validate(url)[1])
#         continue

async def get(url):
    try:
        url_validator.validate(url)
        print("Successful: "+url)
    except Exception as e:
        pass
        print("Exception: "+url+str(e.__class__))


async def extract(urls):
    ret = await asyncio.gather(*[get(url) for url in urls])
asyncio.run(extract(urls))

with open('newtodo.txt', 'w') as f:
    for item in lists.valid:
        f.write("%s\n" % item)
