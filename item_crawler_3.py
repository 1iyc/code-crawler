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

parser.add_argument('--start_page', dest="start_page", type=int, default=1,
                    help="Start Page Number")

args = parser.parse_args()


def crawling_items(url, word, output_file, start_page=1):
    url = url.replace("???", word)
    url_page = url.replace("@@@", str(start_page))

    req = requests.get(url_page)

    dom = BeautifulSoup(req.content, "html.parser")

    codes = dom.select("div.display_table > div.display_row1 > p > span")
    pages = dom.select("div#pages > div#pages > a")
    try:
        last_page = int(pages[-2].text)
    except IndexError:
        sleep(uniform(1.0, 10.1))
        print("Nothing " + word)
        return 1
    except ValueError:
        last_page = 2

    f = open(output_file, 'a', encoding="utf-8")

    for code in codes:
        # f.write(data.text + "\n")
        items = dom.select("div.display_table > div.display_row2 > p#" + code.text + " > span > a")
        for item in items:
            f.write(item.text + "\t" + code.text + "\n")

    f.close()

    start_page += 1

    if start_page < last_page and start_page < 21:
        sleep(uniform(1.0, 10.1))
        crawling_items(url, word, output_file, start_page)

    print(word)

    sleep(uniform(1.0, 10.1))


def main():
    word_list = list(open(args.dict_file, 'r', encoding="utf-8").readlines())
    for word in word_list:
        crawling_items(args.url, word.strip(), args.output_file, args.start_page)


if __name__ == '__main__':
    main()
