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


def crawl_google_image(keywords, image_dir, ban_list):
    uri = "https://www.google.co.kr/search?"

    for keyword in keywords:
        params = {
            "q": keyword,
            "tbm": "isch"
        }

        html_object = req.get(uri, params)

        if html_object.status_code == 200:
            soup = BeautifulSoup(html_object.text, "html.parser")
            img_data = soup.findAll("img")

            count = 1
            for i in img_data[1:]:
                if ban_list:
                    if any(word in i.previous_element.attrs['href'] for word in ban_list):
                        continue

                t = urlopen(i.attrs['src']).read()
                print(i.attrs['src'])

                if t.startswith(b'\xff\xd8\xff\xe0'):
                    filename = os.path.join(image_dir, keyword) + '_' + str(count) + '.jpg'
                else:
                    filename = os.path.join(image_dir, keyword) + '_' + str(count) + '.png'

                with open(filename, "wb") as f:
                    f.write(t)
                    count += 1

                if count == 6:
                    break

        sleep(uniform(1.3, 5.3))


def image_crawl(list_path, image_dir, ban_list):
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    f = open(list_path, 'r', encoding='utf-8')
    rdr = csv.reader(f)

    for line in rdr:
        code = line[0]
        item = re.sub('[/]', '_', line[1])
        keywords = line[2:]
        item_dir = os.path.join(image_dir, code, item)
        if not os.path.exists(item_dir):
            os.makedirs(item_dir)
            try:
                crawl_google_image(keywords, item_dir, ban_list)
                print(rdr.line_num, item, "Finished")
            except:
                with open('./data/error.log', 'a') as f:
                    f.write(str(rdr.line_num) + '\t' + item + '\n')


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

        w_row = [code, real_keyword]

        if len(splited_keyword) > 4:
            for i in range(4, len(splited_keyword) + 1):
                segments_keyword = ' '.join(splited_keyword[:i])
                w_row.append(segments_keyword)
        else:
            w_row.append(parsed_keyword)
        wr.writerow(w_row)
        # if real_keyword != parsed_keyword:
        #     print(code, '\t\t', real_keyword, '\t\t', parsed_keyword)
    f.close()
    g.close()

    print("#### CSV Parsing End ####")


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

    parser.add_argument('--ban_list_path', dest="ban_list_path", type=str, default="./data/ban_list.txt",
                        help="Ban List Path")

    flags, unused_flags = parser.parse_known_args()

    if not os.path.isfile(flags.output_path):
        make_search_list(flags.csv_path, flags.output_path, flags.skip_column)

    ban_list = None

    if os.path.isfile(flags.ban_list_path):
        ban_list = []
        with open(flags.ban_list_path, 'r', encoding='utf-8') as f:
            for word in f:
                ban_list.append(word.strip())
        if len(ban_list) == 0:
            ban_list = None

    image_crawl(flags.output_path, flags.image_dir, ban_list)


if __name__ == '__main__':
    main()
