import sys
import xlrd
import numpy as np
import pandas as pd
import sqlite3 as sq

reload(sys)
sys.setdefaultencoding('utf8')

data = xlrd.open_workbook(sys.argv[1])
table = data.sheets()[0]
nrows = table.nrows # 获取表的行数
l = ['word', 'level', 'lenovo', 'etyma', 'meanZh', 'meanEn', 'example', 'phonetic']

content = []

for i in range(1, nrows): # 循环逐行打印
    if i == 0: # 跳过第一行
        continue
    row = table.row_values(i)[:len(l)]
    if len(row) > 8:
        print len(row), row
        sys.exit()
    content.append(row)

print len(content)

data = pd.DataFrame(content, columns=l)

data['selfLenovo'] = ""

#data = pd.read_csv(sys.argv[1] + '.csv', index_col=False)

data['level'] = 0

#print data[:3]

con  = sq.connect(sys.argv[2] + '.db')

data.to_sql('word', con)

f = file("books.txt", "w")

import datetime

now = datetime.datetime.now()  

s = "再要你命三千 http://7xt8es.com1.z0.glb.clouddn.com/naodong/word/another-3000.db %d(%s更新)" % (len(content), now.strftime('%Y-%m-%d-%H:%M:%S'))

f.write(s)

f.close()
