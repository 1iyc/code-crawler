#! /usr/bin/env python
# coding: utf-8

import argparse
import asyncio
import aiohttp
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from random import randint
import requests

parser = argparse.ArgumentParser(description="Crawling Item Name and Code via Multiple Proxy Server with Async")

parser.add_argument('--uri', dest="uri", type=str, default=None,
                    help="URI, If You Want to Use Dictionary, Use '???' at Parameter Place"
                         "and If URI Page Number Has Page Number, Use '@@@' at Page Number Place")
parser.add_argument('--proxy_uri', dest="proxy_uri", type=str, default=None,
                    help="Proxy Site URI")

parser.add_argument('--dict_file', dest="dict_file", type=str, default=None,
                    help="Dictionary File Path Used on Search")
parser.add_argument('--output_file', dest="output_file", type=str, default="./data/data.txt",
                    help="Output Data File Path")
parser.add_argument('--output_dir', dest="output_dir", type=str, default="./data/output",
                    help="Output Data Directory Path")
parser.add_argument('--finished_file', dest="finished_file", type=str, default="./data/finished_data.txt",
                    help="Finished Data File Path")

args = parser.parse_args()

# async def parse_item():


async def get_proxy():
    async with aiohttp.request("GET", args.proxy_uri, headers={'User-Agent:': UserAgent().random}) as res:
        row = BeautifulSoup(await res.text(), "html.parser").select("table > tbody > tr")[randint(0, 20)].select("td")
        print("GET PROXY")
        return "http://" + row[0].text + ":" + row[1].text


async def multi_crawling(semaphore, word):
    await semaphore.acquire()
    print("[{}] STARTED".format(word))
    uri_word = args.uri.replace("???", word)
    uri_page = uri_word.replace("@@@", '1')

    last_page = 0
    try:
        async with aiohttp.request("GET", uri_page, headers={'User-Agent:': UserAgent().random},
                                   proxy=await get_proxy()) as res:
            print(word, BeautifulSoup(await res.text(), "html.parser").select("div#pages > div#pages > a")[-2].text)
    except Exception as e:
        print(word, e)

    await asyncio.sleep(2)
    semaphore.release()


async def main(loop):
    word_list = list(open(args.dict_file, 'r', encoding="utf-8").readlines())
    crawler_semaphore = asyncio.Semaphore(value=20)
    await asyncio.wait([multi_crawling(crawler_semaphore, word.strip()) for word in word_list])
    print("Main Coroutine")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    print("[!!! FINISHED !!!]")
    loop.close()
