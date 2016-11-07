import sys
import json

import xml.dom.minidom

dom = xml.dom.minidom.parse(sys.argv[1])
root = dom.documentElement

items = root.getElementsByTagName('item')
print len(items)
word_dict = {}
word_count = defaultdict(int)

c = 0
for item in items:

    word = item.getElementsByTagName('word')[0].firstChild.data
    if word in word_dict:
        continue

    trans = item.getElementsByTagName('trans')[0].firstChild.data
    phonetic = item.getElementsByTagName('phonetic')[0].firstChild.data
 
    mean_list, example_list = parse_tran(trans)
    mean_str = ''.join(mean_list)
    example_str = ''.join(example_list)

    word_dict[word] = {'phonetic': phonetic, 'mean': mean_str, 'example': example_str}

print len(word_dict)
fp = file('3000.json', 'w')
fp.write(json.dumps(word_dict, ensure_ascii=True,indent=2))
fp.close()

def parse_tran(tran):
    means = tran.split(tran[0])

    mean_list = []
    example_list = []
    for mean in means[1:]:

        symbol = u'\u2663'
        lines = mean.split(symbol)

        meaning = lines[0][5:]
        #print meaning,
        mean_list.append(meaning)

        zh_mean = meaning.split(u'：')[0]

        for l in lines[1:]:
            if l[0] == u'例':
                #print zh_mean, l[3:],
                example_list.append(zh_mean + ': '+ l[3:])


    #print len(mean_list), len(example_list)
    return mean_list, example_list