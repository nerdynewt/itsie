#!/bin/env python3

import asyncio
import databaser

async def add2db():
    await databaser.connect("https://mermin.com", "Achscroft Mermin", "Cengage publications")

asyncio.run(add2db())
