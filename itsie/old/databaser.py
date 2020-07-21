#!/bin/env python3

import asyncio
import aiomysql
import mysql.connector

# async def add(url, title, content):
#     print("added!")
#     mydb = await aiomysql.connect(
#             host = "localhost",
#             user = "vishnu",
#             password = "CrapWeasel",
#             db = "search_index"
#             )
#     cursor = await mydb.cursor()
#     try:
#         sql = "INSERT INTO pycrawl_index (url, title, body) VALUES (%s, %s, %s)"
#         val = (url, title, content)
#         await cursor.execute(sql, val)
#         await mydb.commit()
#         mydb.close()
#         return True
#     except mysql.connector.errors.DataError:
#         return False

# def add(url, title, content):
#     asyncio.run(connect(url, title, content))

mydb = mysql.connector.connect(
        host = "localhost",
        user = "vishnu",
        password = "CrapWeasel",
        database = "search_index"
        )

mycursor = mydb.cursor()

def add(url, title, content):
    if not url or not title or not content:
        return False
    try:
        sql = "INSERT INTO pycrawl_index (url, title, body) VALUES (%s, %s, %s)"
        val = (url, title, content)
        mycursor.execute(sql, val)
        mydb.commit()
        return True
    except mysql.connector.errors.DataError:
        return False
