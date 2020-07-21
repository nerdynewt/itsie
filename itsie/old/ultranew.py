#!/bin/env python3

import asyncio
import aiohttp
import time

import lists
import url_validator
import content_validator
import content_parser
import databaser


urls = lists.todo
found = list()
amount = len(lists.todo)

async def get(url):
    try:
        url_validator.validate(url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                assert response.status == 200
                text = await response.text()
                content_validator.validate(text, response.headers)
                # assert content_validator.validate(text, response.headers)
                content = content_parser.Content(text, url)
                databaser.add(url, content.title, content.clean)
                print("Successful: "+url)
                return content.links
    except Exception as e:
        pass
        print("Exception: "+url+str(e.__class__))


async def extract(urls):
    ret = await asyncio.gather(*[get(url) for url in urls])
asyncio.run(extract(urls))
