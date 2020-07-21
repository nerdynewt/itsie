#!/bin/env python3

import asyncio
import aiohttp
import sys
import argparse

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
    Function to handle exceptions and inform the user
    """
    if hasattr(exception, 'value'):
        message = exception.value
    elif hasattr(exception, 'message'):
        message = exception.message
    else:
        message = ""

    name = exception.__class__.__name__

    if name == "UrlValidationError":
        console("OKBLUE", "Skipping", url, message)
    elif name == "ContentValidationError":
        console("WARNING", "Blocking", url, message)
    else:
        console("FAIL", "Exception", url, name)

async def get(url):
    """
    Main function, asynchronously requests to urls given.
    """
    import itsie.urls as urls
    import itsie.content_parser as content_parser
    import itsie.databaser as databaser
    import itsie.lists as lists
    try:
        urls.validate(url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                assert response.status == 200
                text = await response.text()
                content_parser.validate(text, response.headers, url)
                content = content_parser.Content(text, url)
                databaser.add(url, content.title, content.clean)
                # print("Successful: "+url)
                console("OKGREEN", "Indexed  ", url, "")
                lists.found.concat(content.links)
    except Exception as e:
        handle(e, url)
        pass

async def extract(urls):
    """
    Async pool function
    """
    ret = await asyncio.gather(*[get(url) for url in urls])

def main():
    """
    Console entry-point
    """
    parser = argparse.ArgumentParser(description='itsie: Web crawler for finding personal websites')
    parser.add_argument('--depth', required=False, default=False, help="Depth to search upto. Default: 3")
    parser.add_argument('--init', required=False, default=False, action="store_true", help="Initialize this directory for crawling")
    args = parser.parse_args()

    if args.init:
        import itsie.reconfig
        itsie.reconfig.init()
        return
    if args.depth:
        depth = int(args.depth)
    else:
        depth = 3
    import itsie.lists as lists
    try:
        for iteration in range(depth):
            urls = lists.todo.array
            asyncio.run(extract(urls))
            lists.todo.array = lists.trim(lists.found.array)
        lists.cleanup()
    except KeyboardInterrupt:
        lists.cleanup()

if __name__ == '__main__':
    main()
