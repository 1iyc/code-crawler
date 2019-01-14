#! /usr/bin/env python
# coding: utf-8

import argparse
import requests
from fake_useragent import UserAgent
from random import randint
from random import uniform
from time import sleep
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="Arrange Dictionary File for Async Crawler")

parser.add_argument('--dict_file', dest="dict_file", type=str, default=None,
                    help="Dictionary File Path Used on Search")
parser.add_argument('--finished_file', dest="finished_file", type=str, default="./data/finished_data.txt",
                    help="Output Data File Path")

args = parser.parse_args()


def crawling_items(uri, proxy_uri, word, output_file, start_page=1, last_page=0):
    if type(proxy_uri) == str:
        proxies_req = requests.get(proxy_uri, headers={'User-Agent': UserAgent().random})
        proxies_dom = BeautifulSoup(proxies_req.content, "html.parser")
        proxies_tr = proxies_dom.select("table > tbody > tr")

        proxies = []
        for row in proxies_tr:
            proxies.append({
                "http": row.select("td")[0].text+":" + row.select("td")[1].text,
                "https": row.select("td")[0].text+":" + row.select("td")[1].text,
            })

        try:
            proxy = proxies[randint(0, len(proxies) - 1)]
        except Exception as e:
            print(proxy)
            print(len(proxy))
            print(e)
            crawling_items(uri, args.proxy_uri, word, output_file, start_page, last_page)
        print("[ {} ]  PROXY IP\t{}".format(word, proxy['http']))
    else:
        proxy = proxy_uri

    uri = uri.replace("???", word)
    uri_page = uri.replace("@@@", str(start_page))

    try:
        req = requests.get(uri_page, proxies=proxy, timeout=5)
    except requests.exceptions.ProxyError:
        print("[ {} ]  PROXY ERROR!!!".format(word))
        crawling_items(uri, args.proxy_uri, word, output_file, start_page, last_page)
        return 0
    except requests.exceptions.Timeout:
        print("[ {} ]  TIMEOUT ERROR!!!".format(word))
        crawling_items(uri, args.proxy_uri, word, output_file, start_page, last_page)
        return 0
    except (ConnectionRefusedError, requests.exceptions.ConnectionError):
        print("[ {} ]  CONNECTION ERROR!!!".format(word))
        crawling_items(uri, args.proxy_uri, word, output_file, start_page, last_page)
        return 0
    except Exception as e:
        print("[ {} ]  UNEXPECTED ERROR!!! {}".format(word, e))
        crawling_items(uri, args.proxy_uri, word, output_file, start_page, last_page)
        return 0

    dom = BeautifulSoup(req.content, "html.parser")

    codes = dom.select("div.display_table > div.display_row1 > p > span")

    if not last_page:
        pages = dom.select("div#pages > div#pages > a")
        try:
            last_page = int(pages[-2].text)
            print("[ {} ]  TOTAL PAGE\t{}".format(word, last_page-1))
            if last_page > 21:
                last_page = 21
        except IndexError:
            print("[ {} ]  NOT EXISTED".format(word))
            return 1
        except ValueError:
            last_page = 2
            print("[ {} ]  TOTAL PAGE\t{}".format(word, last_page-1))

    f = open(output_file, 'a', encoding="utf-8")

    for code in codes:
        # f.write(data.text + "\n")
        items = dom.select("div.display_table > div.display_row2 > p#" + code.text + " > span > a")
        for item in items:
            f.write(item.text + "\t" + code.text + "\n")

    f.close()

    print("[ {} ]  {}/{}".format(word, start_page, last_page-1))

    start_page += 1

    if start_page < last_page and start_page < 21:
        sleep(uniform(0.01, 0.05))
        crawling_items(uri, proxy, word, output_file, start_page, last_page)

    sleep(uniform(0.05, 0.1))


def main():
    word_list = list(open(args.dict_file, 'r', encoding="utf-8").readlines())
    for word in word_list:
        print("[ {} ]  STARTED!!!".format(word.strip()))
        crawling_items(args.uri, args.proxy_uri, word.strip(), args.output_file, args.start_page)


if __name__ == '__main__':
    main()