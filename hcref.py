#! /usr/bin/python2
# -*- coding: utf-8 -*-

import textwrap
import sys
import requests
from bs4 import BeautifulSoup

TEXTWIDTH = 100
URL = "https://httpstatuses.com/"

class color:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def http_code(code):
    
    try:
        url = requests.get(URL + "%s" % code)
        url.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        sys.exit(1)
    
    soup = BeautifulSoup(url.content, features="html.parser")
    article = soup.find_all("article", "code container")

    print("Class: %s" % article[0].h2.text.encode('utf-8'))
    print("Title: %s" % article[0].h1.text.encode('utf-8'))

    li = article[0].find_all("li")
    rfc_url = li[0].a['href']
    rfc_section = li[0].a.text
    print("RFC: %s, URL: %s\n" % (rfc_section, rfc_url))

    i = 0;
    p = article[0].find_all("p")
    while i < len(p):
        if not p[i].code:
            print("%s\n" % textwrap.fill(p[i].text.encode('utf-8'), TEXTWIDTH))
        i += 1


def list_codes():

    try:
        url = requests.get(URL)
        url.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        sys.exit(1)

    soup = BeautifulSoup(url.content, features="html.parser")
    codes = soup.find_all("div", "container codes")

    i = 0
    li = codes[0].find_all("li")
    while i < len(li):
        if not li[i].h2:
            print(" %s" % li[i].text.encode('utf-8'))
        else:
            print(color.BOLD + color.YELLOW + "\n%s:" % li[i].h2.text.encode('utf-8') + color.ENDC)
        i += 1

if __name__ == "__main__":

    if sys.argv[1].isdigit() and range(100, 599):
        http_code(sys.argv[1])
    elif sys.argv[1] == "list":
        list_codes()
    else:
        print("usage: <list> | <code>")
        sys.exit(1)
