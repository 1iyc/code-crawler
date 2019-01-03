#! /usr/bin/env python
# coding: utf-8

import argparse
import requests
from random import uniform
from time import sleep
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="Crawling Item Name and Code")

parser.add_argument('--url', dest="url", type=str, default=None,
                    help="URL, If You Want to Use Dictionary, Use '???' at Parameter Place")
parser.add_argument('--dict_file', dest="dict_file", type=str, default=None,
                    help="Dictionary File Path Used on Search")
parser.add_argument('--output_file', dest="output_file", type=str, default="./data/data.txt",
                    help="Output Data File Path")

args = parser.parse_args()


def crawling_items(url, word, output_file):
    url = url.replace("???", word)

    req = requests.get(url)

    dom = BeautifulSoup(req.content, "html.parser")

    items = dom.select("div.results-table > div.result-section > table.result-table > tbody > tr > td.desc")
    codes = dom.select("div.results-table > div.result-section > table.result-table > tbody > tr > td > a")

    f = open(output_file, 'a', encoding="utf-8")

    for data in zip(items, codes):
        f.write(data[0].text + "\t" + data[1].text[:6] + "\n")

    print(word)

    f.close()

    sleep(uniform(1.0, 10))


def main():
    word_list = list(open(args.dict_file, 'r', encoding="utf-8").readlines())
    for word in word_list:
        crawling_items(args.url, word.strip(), args.output_file)


if __name__ == '__main__':
    main()
