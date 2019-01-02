#! /usr/bin/env python
# coding: utf-8

import argparse
import re

parser = argparse.ArgumentParser(description="Item List to Dictionary List")

parser.add_argument('--input_file', dest="input_file", type=str, default="./data/data.txt",
                    help="Input Data File Path")
parser.add_argument('--output_file', dest="output_file", type=str, default="./data/dict.txt",
                    help="Output Data File Path")
parser.add_argument('--na_file', dest="na_file", type=str, default="./data/na.txt",
                    help="Delete NA Word in NA File Path\nBe Processed at the Last")
parser.add_argument('--raw', dest="raw", type=bool, default=True,
                    help="If Input File is Raw, True")

args = parser.parse_args()


def make_dict(input_file, output_file, na_file, raw=True):
    data_list = list(open(input_file, 'r', encoding="utf-8").readlines())
    na_list = list(open(na_file, 'r', encoding="utf-8").readlines())
    na_list = [x.strip() for x in na_list]

    cnt = 0
    print("TOTAL: " + str(len(data_list)))

    dict_list = []

    if raw:
        for data in data_list:

            data = re.sub(r'[\.]', '', data.strip().upper())
            data = re.sub(r'[^A-Z\-]', ' ', data)
            data = [x.strip('-') for x in data.split() if x not in na_list and len(x) > 1 and len(set(x)) > 1]
            data = list(set(data))

            if len(data):
                for i in range(len(data) - 1):
                    dict_list.append(data[i])
                    dict_list.append(data[i] + "+" + data[i+1])
                dict_list.append(data[len(data) - 1])

            cnt += 1

            if cnt % 100 == 0:
                print(cnt)

        dict_list = list(set(dict_list))

    f = open(output_file, 'w', encoding="utf-8")
    for dic in dict_list:
        f.write(dic + "\n")
    f.close()


def main():
    make_dict(args.input_file, args.output_file, args.na_file, args.raw)


if __name__ == '__main__':
    main()
