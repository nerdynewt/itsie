#!/bin/python

import asyncio
import aiohttp
import time
import requests
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

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36' }

def console(color, status, url, reason):
    output = bcolors[color]+status+'\t'+bcolors["ENDC"]+url
    if reason:
        output += ' ('+bcolors[color]+reason+bcolors["ENDC"]+')'
    print(output.expandtabs(20))

def cleanup():
    with open('todo.txt', 'w') as f:
        for item in lists.todo:
            f.write("%s\n" % item)
    with open('done.txt', 'w') as f:
        for item in lists.done:
            f.write("%s\n" % item)
    with open('domains.txt', 'w') as f:
        for item in lists.domains:
            f.write("%s\n" % item)
    #     pickle.dump(lists.todo, f)
    # with open('done.txt', 'wb') as f:
    #     pickle.dump(lists.done, f)


async def get(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                print(response.headers)
                resp = await response.text()
                # resp = await response.text()
                # assert resp.status == 200
                print("Successfully got url {} with response of length {}.".format(url, len(resp)))
                # print(resp)
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))


async def main(urls, amount):
    ret = await asyncio.gather(*[get(url) for url in urls])
    print("Finalized all. ret is a list of len {} outputs.".format(len(ret)))


urls = lists.todo
amount = len(lists.todo)
print(urls)

# for url in urls:
#     try:
#         requests.get(url)
#         print("Got "+url)
#     except:
#         print("Not got"+url)


start = time.time()
asyncio.run(main(urls, amount))
end = time.time()

print("Took {} seconds to pull {} websites.".format(end - start, amount))
#!/bin/env python3

exit()

while lists.todo:
    url = lists.todo.pop(0)
    lists.done.append(url)
    if url_validator.validate(url)[0]:
        pass
    else:
        lists.skipped.append(url)
        console("OKBLUE", "Skipping", url, url_validator.validate(url)[1])
        continue
    try:
        response = requests.get(url, timeout=10, headers=headers)
    except KeyboardInterrupt:
        break
    except:
        console("FAIL", "Not Resolved", url, "")
        continue
    if response.encoding == None:
        console("FAIL", "Bad Encoding", url, "")
        continue
    if response.status_code != 200:
        console("FAIL", str(response.status_code), url, "")
        continue
    validation = content_validator.validate(response.text, response.headers)
    if validation[0]:
        content = content_parser.Content(response.text, url)
        lists.todo += content.links
        lists.indexed.append(url)
        if databaser.add(url, content.title, content.clean):
            console("OKGREEN", "Indexed  ", url, "")
        else:
            console("FAIL", "Too Long", url, "")
    else:
        lists.add(url, validation[1])
        lists.blocked.append(url)
        console("WARNING", "Blocking", url, validation[2])
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
