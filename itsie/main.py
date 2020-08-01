#!/bin/env python3

import asyncio
import aiohttp
import sys
import argparse
import logging
import os
from itsie.databaser import Database
import itsie.config as config

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

last_exception = ""
exception_tally = 0

# Connecting toMySQL/sqlite database according to config file
if config.mysql:
    db = Database(
            user = config.sql.user,
            password = config.sql.password,
            database = config.sql.database
            )
else:
    db = Database('itsie.db')

def console(color, status, url, reason):
    """
    Print status to the console
    """
    bcolors = {"HEADER" : '\033[95m',
        "OKBLUE" : '\033[94m',
        "OKGREEN" : '\033[92m',
        "WARNING" : '\033[93m',
        "FAIL" : '\033[91m',
        "ENDC" : '\033[0m',
        "BOLD" : '\033[1m',
        "UNDERLINE" : '\033[4m'}

    output = bcolors[color]+status+'\t'+bcolors["ENDC"]+url
    if reason:
        output += ' ('+bcolors[color]+reason+bcolors["ENDC"]+')'
    print(output.expandtabs(20))


def handle(exception, url):
    """
    Handle exceptions and forward to console. Keep track of exception cascades and dump core if needed.
    """
    import itsie.lists as lists
    import os
    if hasattr(exception, 'value'):
        message = exception.value
    elif hasattr(exception, 'message'):
        message = exception.message
    else:
        message = ""

    name = exception.__class__.__name__
    global last_exception
    global exception_tally
    if exception_tally > 50:
        print("=========")
        console("FAIL", "Exception Cascade Encountered!", "", name)
        lists.todo.array += lists.found.array
        lists.cleanup()
        os.abort()

    if name == "UrlValidationError":
        exception_tally = 0
        console("OKBLUE", "Skipping", url, message)
    elif name == "ContentValidationError":
        exception_tally = 0
        console("WARNING", "Blocking", url, message)
    else:
        if name == last_exception:
            exception_tally += 1
        else:
            exception_tally = 0
        last_exception = name
        console("FAIL", "Exception", url, name)

def reducer(array):
    """
    Standalone function that trims down todo lists that are too big, accessed from --reduce tag
    """
    import itsie.urls as urls
    found = list()
    for url in array:
        try:
            urls.validate(url)
            found.append(url)
            console("OKGREEN", "Passed", url, "")
        except Exception as e:
            handle(e, url)
    return found


async def get(url):
    """
    Main function, asynchronously requests to urls given.
    """
    import itsie.urls as urls
    import itsie.content_parser as content_parser
    # import itsie.databaser as databaser
    import itsie.lists as lists
    # print(url)
    try:
        urls.validate(url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                assert response.status == 200
                text = await response.text()
                content_parser.validate(text, response.headers, url)
                content = content_parser.Content(text, url)
                db.add(url, content.title, content.clean)
                # print("Successful: "+url)
                global exception_tally
                exception_tally = 0
                console("OKGREEN", "Indexed  ", url, "")
                # print(content.links)
                lists.found.concat(content.links)
    except Exception as e:
        handle(e, url)
        pass

async def extract(urls):
    """
    Async pool function
    """
    ret = await asyncio.gather(*[get(url) for url in urls])

async def collect(url):
    """
    Main function, asynchronously requests to urls given.
    """
    import itsie.content_parser as content_parser
    import itsie.lists as lists
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                assert response.status == 200
                text = await response.text()
                content = content_parser.Content(text, url)
                global exception_tally
                exception_tally = 0
                console("OKGREEN", "Indexed  ", url, "")
                lists.found.concat(content.links)
    except Exception as e:
        handle(e, url)
        pass

async def collecter(urls):
    """
    Async pool function
    """
    ret = await asyncio.gather(*[collect(url) for url in urls])


def main():
    """
    Console entry-point
    """
    parser = argparse.ArgumentParser(description='itsie: Web crawler for finding personal websites')
    parser.add_argument('--depth', required=False, default=False, help="Depth to search upto. Default: 3")
    parser.add_argument('--init', required=False, default=False, action="store_true", help="Initialize this directory for crawling")
    parser.add_argument('--collect', required=False, default=False, action="store_true", help="Collect urls without adding to database")
    parser.add_argument('--reduce', required=False, default=False, action="store_true", help="Clean junk urls from todo.txt")
    args = parser.parse_args()

    if args.init:
        import itsie.reconfig
        itsie.reconfig.init()
        return
    import itsie.lists as lists
    if args.reduce:
        lists.todo.array = reducer(lists.todo.array)
        lists.todo.write()
        return
    if args.depth:
        depth = int(args.depth)
    else:
        depth = 3
    if args.collect:
        try:
            for iteration in range(depth):
                urls = lists.todo.array
                asyncio.run(collecter(urls))
                lists.todo.array = lists.trim(lists.found.array)
            lists.cleanup()
        except KeyboardInterrupt:
            lists.todo.array += lists.found.array
            lists.cleanup()
    else:
        try:
            for iteration in range(depth):
                urls = lists.todo.array
                asyncio.run(extract(urls))
                lists.todo.array = lists.trim(lists.found.array)
            lists.cleanup()
        except KeyboardInterrupt:
            lists.todo.array += lists.found.array
            lists.cleanup()

if __name__ == '__main__':
    main()
