import sys
import json
import xlrd

import numpy as np
import pandas as pd
import sqlite3 as sq

data = xlrd.open_workbook('another-3000.xls')

fp = file('3000.json')
word_dict = fp.read()
fp.close()

word_dict = json.loads(word_dict)

table = data.sheets()[0]
nrows = table.nrows # 获取表的行数
l = ['word', 'level', 'lenovo', 'etyma', 'meanZh', 'meanEn', 'example', 'phonetic']

content = []

for i in range(2, nrows): # 循环逐行打印
    if i == 0: # 跳过第一行
        continue
    row = table.row_values(i)[:len(l)-1]
    if row[0] in word_dict:
        row[4] = word_dict[row[0]]['mean']
        row[6] = word_dict[row[0]]['example']
        row.append(word_dict[row[0]]['phonetic'])
    else:
        row.append('')
    if len(row) != 8:
        print row[0]
    content.append(row)

print len(content)

data = pd.DataFrame(content, columns=l)

data['selfLenovo'] = ""

#data = pd.read_csv(sys.argv[1] + '.csv', index_col=False)

data['level'] = 0

#print data[:3]

con  = sq.connect('another-3000.db')

data.to_sql('word', con)
