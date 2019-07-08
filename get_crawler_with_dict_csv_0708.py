#! /usr/bin/env python
# coding: utf-8

import argparse
import requests
from random import uniform
from time import sleep
from bs4 import BeautifulSoup
import csv
import traceback
import sys


def crawling_items(uri, word, output_path):
    print("start:\t" + str(word))
    params = {'hsNo': word}

    req = requests.get(uri, params=params)

    dom = BeautifulSoup(req.content, "html.parser")

    table_rows = dom.select("tbody > tr")

    with open(output_path, 'a', encoding="utf-8") as f:
        wr = csv.writer(f)
        for row in table_rows:
            items = row.select("td")
            items = [item.text.strip() for item in items]
            items.append(str(word))
            wr.writerow(items)

    sleep_time = uniform(0.5, 2.7)

    print("sleep.." + str(sleep_time))
    sleep(sleep_time)
    print("end  :\t" + str(word))


def main():
    parser = argparse.ArgumentParser(description="Crawling Item Name and Code")

    # options
    parser.add_argument('--uri', dest="uri", type=str, default=None,
                        help="URI")
    parser.add_argument('--dict_path', dest="dict_path", type=str, default="./data/dict.csv",
                        help="Dictionary File Path Used on Search")
    parser.add_argument('--output_path', dest="output_path", type=str,
                        default="./data/get_crawler_with_dict_csv_output.csv", help="Output Data File Path")

    flags, unused_flags = parser.parse_known_args()

    word_list = list(open(flags.dict_path, 'r', encoding="utf-8").readlines())
    for word in word_list:
        try:
            crawling_items(flags.uri, word.strip(), flags.output_path)
        except:
            traceback.print_exc()
            print(" Unexpected error:", sys.exc_info()[0])
            with open("data/err.log", 'a', encoding="utf-8") as f:
                f.write(str(word.strip()) + '\n')


if __name__ == '__main__':
    main()
