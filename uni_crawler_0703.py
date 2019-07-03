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
    data = {'pageIndex': '1',
            'pageUnit': '100',
            'orderColumns': 'ENFR_DT+desc',
            'rrdcNo': '0072019002205',
            'reffNo': '',
            'dtrmHsSgn': '',
            'stDt': '19000101',
            'edDt': '20190703',
            'srwr': '',
            'srchYn': 'Y',
            'scrnTp': 'WDTH',
            'sortColm': '',
            'sortOrdr': '',
            'atntSrchTp': '',
            'docId': '',
            'cmdtNm': '',
            'cmdtDesc': '',
            'dtrmRsnCn': '',
            'scrnId': '',
            'srchReffNo': '',
            'srchDtrmHsSgn': '',
            'srchStDt': '1900-01-01',
            'srchEdDt': '2019-07-03',
            'srchCmdtNm': '',
            'srchCmdtDesc': '',
            'srchDtrmRsnCn': '',
            'srchSrwr': '',
            'pagePerRecord': '100',
            'initPageIndex': '1',
            'ULS0203037S_F1_savedToken': '88AR16TZ6PZ52CJ1C5KMWAJ43KW1WKC1',
            'savedToken': 'ULS0203037S_F1_savedToken',
            'txtEnfrDt': '20190531',
            'txtDtrmHsSgn': '8477.80-0000',
            'attchFileGrpId': 'PCA-20190529-00002959574IH4Pv',
            'attchFileGrpId': 'PCA-20190529-00002959575RNAIc'}
    data = {
        'pageIndex': '1',
        'pageUnit': '100',
        'orderColumns': 'ENFR_DT+desc',
        'rrdcNo': '0072019002205',
        'reffNo': '',
        'dtrmHsSgn': '',
        'stDt': '19000101',
        'edDt': '20190704',
        'srchStDt': '1900-01-01',
        'srchEdDt': '2019-07-04',
    }
    header = {
        'Host': 'unipass.customs.go.kr',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://unipass.customs.go.kr/clip/index.do',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'isAjax': 'true',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Length': '604',
        'Connection': 'keep-alive',
        'Cookie': 'WMONID=s3eCz2rGLbq; JSESSIONID=0001fEVgPyCVIQfXpD5o_ZCCW29ynIHUDvorW1vPWgXBU4SXjvuVYVvZ2ZwmCIZ3DG0e4vdJCW0-tZK2QKeH7LnRo15E5qRXm0iGIPvCgxbSN97FQtrZs1ip_ZafM7q_jHbS:eul21',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'}
    res = requests.post(args.url, data=data)
    # print(res.json())
    last_page = res.json()['paginationInfo']['lastPageNo']
    item_list = res.json()['uls_dmst']['itemList']

    f = open("data_0704.txt", 'w', encoding="utf-8")
    g = open("data_date_0704.txt", 'w', encoding="utf-8")

    for i in range(len(item_list)):
        f.write(item_list[i]['DTRM_HS_SGN'] + '\t' + item_list[i]['CMDT_NM'] + '\n')
        g.write(item_list[i]['ENFR_DT'] + item_list[i]['DTRM_HS_SGN'] + '\t' + item_list[i]['CMDT_NM'] + '\n')

    for i in range(2, int(last_page) + 1):
        data['pageIndex'] = str(i)
        res = requests.post(url, data=data)
        item_list = res.json()['uls_dmst']['itemList']
        for i in range(len(item_list)):
            f.write(item_list[i]['DTRM_HS_SGN'] + '\t' + item_list[i]['CMDT_NM'] + '\n')
            g.write(item_list[i]['ENFR_DT'] + '\t' + item_list[i]['DTRM_HS_SGN'] + '\t' + item_list[i]['CMDT_NM'] + '\n')
        sleep(uniform(1.2, 3.4))


if __name__ == '__main__':
    main()
