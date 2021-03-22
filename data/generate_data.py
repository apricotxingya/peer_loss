# -*- coding: UTF-8 -*-
# @Time    : 2021/3/7
# @Author  : xiangyuejia@qq.com
# Apache License
# Copyright©2020-2021 xiangyuejia@qq.com All Rights Reserved
import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_file', type=str, help='input file', default='')
parser.add_argument('--output_label', type=str, help='output_file', default='')
parser.add_argument('--output_sent', type=str, help='output_file', default='')
args = parser.parse_args()

with open(args.input_file, 'r', encoding='utf8') as fin:
    data = [json.loads(l.strip()) for l in fin.readlines()]
with open(args.output_label, 'r', encoding='utf8') as fout_label:
    with open(args.output_sent, 'r', encoding='utf8') as fout_sent:
        for d in data:
            label = d['label']
            sent = d['sentence']
            print(label, file=fout_label)
            print(sent, file=fout_sent)