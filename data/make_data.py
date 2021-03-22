# -*- coding: UTF-8 -*-
# @Time    : 2021/3/7
# @Author  : xiangyuejia@qq.com
# Apache License
# Copyright©2020-2021 xiangyuejia@qq.com All Rights Reserved
from tqdm import tqdm
import pandas as pd
import json

# file_xlsx = 'test.xlsx'
# file_json = 'test.jsonl'
# file_out = 'test.csv'
file_xlsx = 'train.xlsx'
file_json = 'train.jsonl'
file_out = 'train.csv'


data_xlsx = []
df = pd.read_excel(file_xlsx)
data = df.values
for d in data:
    data_xlsx.append([d[0],d[2]])

data_json = []
with open(file_json, 'r') as fin:
    ot = fin.readline()
    while ot:
        t = ot.strip()
        if len(t) == 0:
            continue
        o = json.loads(t)
        data_json.append(o['features'][0]['layers'][0]['values'])
        ot = fin.readline()
# data_json = data_json[1:]
print('len of xlsx: ', len(data_xlsx))
print('len of json: ', len(data_json))
out_data = []
head = ['target']
print('dim: ', len(data_json[0]))
for i in range(len(data_json[0])):
    head.append(str(i+1))
out_data.append(head)
for a,b in tqdm(zip(data_xlsx, data_json)):
    out_data.append([a[0]] + b)

df = pd.DataFrame(out_data)
df.to_csv(file_out, index=False, header=False)
