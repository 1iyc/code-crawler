#! /usr/bin/env python

import argparse
import re
import os

parser = argparse.ArgumentParser(description="Text File to Csv File")

# I&O file
parser.add_argument('--input_file', dest="input_file", type=str, default="./data/data_statistic.txt", help="Data File")

args = parser.parse_args()


def txt_to_csv(input_file):
    dir_path = os.path.dirname(os.path.realpath(input_file))
    output_path = os.path.join(dir_path, 'data_statistic.csv')

    data_list = list(open(input_file, 'r', encoding="utf-8").readlines())

    f = open(output_path, 'w', encoding="utf-8")

    for line in data_list:
        line = line.split('\t')
        for word in line:
            f.write(word.strip() + ", ")
        f.write(+ "\n")


def main():
    txt_to_csv(args.input_file)


if __name__ == '__main__':
    main()
