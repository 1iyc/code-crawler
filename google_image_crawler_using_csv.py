#! /usr/bin/env python
# coding: utf-8

import argparse
import requests as req
from random import uniform
from time import sleep
import csv
import re
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen


def crawl_google_image(keyword):
    uri = "https://www.google.co.kr/search?"

    params = {
        "q": keyword,
        "tbm": "isch"
    }

    html_object = req.get(uri, params)

    if html_object.status_code == 200:
        bs_object = BeautifulSoup(html_object.text, "html.parser")
        img_data = bs_object.find_all("img")

        for i in enumerate(img_data[1:]):
            # 딕셔너리를 순서대로 넣어줌
            t = urlopen(i[1].attrs['src']).read()

            filename = "b" + str(i[0] + 1) + '.png'

            with open(filename, "wb") as f:
                f.write(t)


def image_crawl(list_path, image_dir):
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    f = open(list_path, 'r', encoding='utf-8')
    rdr = csv.reader(f)

    for line in rdr:
        code = line[0]
        item = re.sub('[/]', '_', line[1])
        if not os.path.exists(os.path.join(image_dir, code, item)):
            os.makedirs(os.path.join(image_dir, code, item))
            crawl_google_image(line[2])


def make_search_list(csv_path, output_path, skip_column):
    print("##### Parse CSV #####")

    f = open(csv_path, 'r', encoding='utf-8')
    rdr = csv.reader(f)

    g = open(output_path, 'w', encoding='utf-8', newline='')
    wr = csv.writer(g)

    if skip_column:
        next(rdr, None)

    for line in rdr:
        code = line[0]
        real_keyword = line[1]
        parsed_keyword = re.sub('[^a-zA-Z\- ]+', ' ', real_keyword)
        parsed_keyword = ' '.join([w for w in parsed_keyword.split() if len(w) > 1])

        splited_keyword = parsed_keyword.split()
        if len(splited_keyword) > 4:
            for i in range(4, len(splited_keyword) + 1):
                segments_keyword = ' '.join(splited_keyword[:i])
                wr.writerow([code, real_keyword, segments_keyword])
        else:
            wr.writerow([code, real_keyword, parsed_keyword])
        # if real_keyword != parsed_keyword:
        #     print(code, '\t\t', real_keyword, '\t\t', parsed_keyword)
    f.close()
    g.close()


def main():
    parser = argparse.ArgumentParser(description="Crawling Google Image using CSV File")

    # options
    parser.add_argument('--csv_path', dest="csv_path", type=str, default="./data/list.csv",
                        help="Input CSV File Path")

    parser.add_argument('--output_path', dest="output_path", type=str, default="./data/parsed_list.csv",
                        help="Output Parsed CSV File Path")

    parser.add_argument('--skip_column', dest="skip_column", type=bool, default=False, nargs='?', const=True,
                        help="Parse data")

    parser.add_argument('--image_dir', dest="image_dir", type=str, default="./data/image",
                        help="Output Image Directory Path")

    flags, unused_flags = parser.parse_known_args()

    if not os.path.isfile(flags.output_path):
        make_search_list(flags.csv_path, flags.output_path, flags.skip_column)

    image_crawl(flags.output_path, flags.image_dir)


if __name__ == '__main__':
    main()
