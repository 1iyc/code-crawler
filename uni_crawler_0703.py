#! /usr/bin/env python
# coding: utf-8

import argparse
import requests
from random import uniform
from time import sleep
import csv
import re


def write_data(output_path, code, item, date, parse_item=False):
    with open(output_path, 'w', encoding="utf-8") as f:
        wr = csv.writer(f)
        for i, v in enumerate(item):
            if not parse_item:
                wr.writerow([code[i], v])
            else:
                v_sp = v.split(';')
                for v_item in v_sp:
                    wr.writerow([re.sub('\D', '', code[i]), v_item.strip()])


def request_data(uri, data, with_date=False):
    print('#'*10 + " Request Data " + '#'*10)
    code = []
    items = []
    if with_date:
        date = []

    res = requests.post(uri, data=data).json()

    last_page = res['paginationInfo']['lastPageNo']
    print("total page number:\t" + str(last_page))

    item_list = res['uls_dmst']['itemList']

    print("page...\t1")

    for i in range(len(item_list)):
        code.append(str(item_list[i]['DTRM_HS_SGN']).strip())
        items.append(str(item_list[i]['CMDT_NM']).strip())
        if with_date:
            date.append(str(item_list[i]['ENFR_DT']).strip())

    sleep_sec = uniform(1.2, 3.4)
    print("sleep..\t" + str(round(sleep_sec, 2)) + "s")
    sleep(sleep_sec)

    for i in range(2, int(last_page) + 1):
        data['pageIndex'] = str(i)
        print("page...\t" + str(i))
        res = requests.post(uri, data=data)
        item_list = res.json()['uls_dmst']['itemList']
        for j in range(len(item_list)):
            code.append(str(item_list[j]['DTRM_HS_SGN']).strip())
            items.append(str(item_list[j]['CMDT_NM']).strip())
            if with_date:
                date.append(str(item_list[j]['ENFR_DT']).strip())
        sleep_sec = uniform(1.2, 3.4)
        print("sleep..\t" + str(round(sleep_sec, 2)) + "s")
        sleep(sleep_sec)

    if with_date:
        return code, items, date
    else:
        return code, items, None


def main():
    parser = argparse.ArgumentParser(description="Crawling Item Name and Code")

    # options
    parser.add_argument('--with_date', dest="with_date", type=bool, default=False, nargs='?', const=True,
                        help="Request data with date")
    parser.add_argument('--parse_item', dest="parse_item", type=bool, default=False, nargs='?', const=True,
                        help="Parse data")

    parser.add_argument('--uri', dest="uri", type=str, default=None,
                        help="URI")
    parser.add_argument('--output_path', dest="output_path", type=str, default="./data/data.txt",
                        help="Output Data File Path")

    flags, unused_flags = parser.parse_known_args()

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

    code, item, date = request_data(flags.uri, data, flags.with_date)

    write_data(flags.output_path, code, item, date, flags.parse_item)


if __name__ == '__main__':
    main()
