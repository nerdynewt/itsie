#!/bin/env python3


import pkg_resources
import os
import shutil

def init():
    print("Initializing directory for crawl...")
    wd = os.getcwd()
    listfiles = ["domains.txt", "corporates.txt", "sinners.txt", "exclude.txt", "seen.txt", "todo.txt", "found.txt"]
    for listfile in listfiles:
        # print(pkg_resources.resource_exists("itsie", "data/todo.txt"))
        shutil.copy(pkg_resources.resource_filename("itsie", "data/"+listfile), wd)
    print("""
Initialization complete.
Now you can add a list of websites to crawl into todo.txt and crawl itsie without any arguments
    """
    )
