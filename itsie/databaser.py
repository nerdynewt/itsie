#!/bin/env python3

import asyncio
import aiomysql
import mysql.connector

class Database:
    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            import mysql.connector
            self.host = 'localhost'
            self.user = kwargs.get('user')
            self.password = kwargs.get('password')
            self.database = kwargs.get('database')
            self.connection = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database
                )
            self.cursor = self.connection.cursor()
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS itsie_index(
                url VARCHAR(200),
                title VARCHAR(200),
                body TEXT,
                FULLTEXT (url,title,body)
                );""")
        else:
            import sqlite3
            self.database = args[0]
            self.connection = sqlite3.connect(self.database)
            self.cursor = self.connection.cursor()
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS itsie_index(
                url VARCHAR(200),
                title VARCHAR(200),
                body TEXT
                );""")

    def add(self, url, title, content):
        if not url or not title or not content:
            return False
        try:
            sql = f'INSERT INTO itsie_index (url, title, body) VALUES ("{url}", "{title}", "{content}")'
            # val = (url, title, content)
            self.cursor.execute(sql)
            self.connection.commit()
            return True
        except mysql.connector.errors.DataError:
            return False

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

        # import argparse
        # parser = argparse.ArgumentParser(description='itsie: Web crawler for finding personal websites')
        # parser.add_argument('--collect', required=False, default=False, action="store_true", help="Collect urls without adding to database")
        # args, unknown = parser.parse_known_args()
        # if args.collect:
        #     return True



    # def initialize(self):
    #     print("Initializing Database {self.path}...")
    #     self.cursor.execute("""CREATE TABLE IF NOT EXISTS itsie_index(
    #             url VARCHAR(200),
    #             title VARCHAR(200),
    #             body TEXT
    #             );""")
        #     """CREATE TABLE IF NOT EXISTS itsie_index (
        #     id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
        #     url VARCHAR(200),
        #     title VARCHAR(200),
        #     body TEXT,
        #     FULLTEXT (url,title,body)
        #     );
        #     """
        # )
        # self.cursor.execute(
        #     """CREATE TABLE books (
        # title varchar(255) NOT NULL,
        # author varchar(255) NOT NULL
        # );"""
        # )

