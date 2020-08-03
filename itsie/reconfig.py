#!/bin/env python3


import pkg_resources
import os
import shutil
import itsie.config

def init():
    print("Initializing directory for crawl...")
    wd = os.getcwd()
    listfiles = ["domains.txt", "corporates.txt", "sinners.txt", "exclude.txt", "seen.txt", "todo.txt", "found.txt", "million.bloom"]
    for listfile in listfiles:
        # print(pkg_resources.resource_exists("itsie", "data/todo.txt"))
        shutil.copy(pkg_resources.resource_filename("itsie", "data/"+listfile), wd)
    if not itsie.config.mysql:
        shutil.copy(pkg_resources.resource_filename("itsie", "data/index.php"), wd)
    print("""
Initialization complete.
Now you can add a list of websites to crawl into todo.txt and crawl itsie without any arguments
    """
    )
