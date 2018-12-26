#! /usr/bin/env python

import requests
from random import uniform
from time import sleep
from bs4 import BeautifulSoup


for i in range(922, 10000):
    f = open('C:/data/code_list.txt', 'a', encoding="utf-8")

    code = "%04d" % i
    print(code)
    BASE_URL = "{}".format(code)

    req = requests.get(BASE_URL)

    dom = BeautifulSoup(req.content, "html.parser")

    col = dom.select("table > tbody > tr > td.ac")

    for item in col:
        if len(item.text) == 6:
            f.write(item.text + "\n")

    f.close()

    sleep(uniform(3.0, 10.0))

