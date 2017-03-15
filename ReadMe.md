# BrainHoleEnglish

脑洞英语

Brain hole ideas list in [创意脑洞](http://sndnyang.github.io/NaoDong-list.html)

对创意脑洞里脑洞英语的实现， 目前只有 单词部分功能， 以后完善， 并实现 文学学习等脑洞。

In short:

1. recite words using mnemotechny
2. practice in the way of which Benjamin Franklin wrote in his autobiography

Now only a part of functions of reciting words

## Technic

1. Jquery + IndexedDB -- the code is in a very bad form of organization mixing Jquery with pure Javascript.
2. Python Flask + ProgreSQL on Openshift. But it seems to be too slow. Waiting (TTFB) is too long. Maybe I will transit to Google app engine. However my main website is still planned to stay on Openshift. Therefore, it will be a severe issue on user informations.

use virtualenv

pip install -r requirements.txt

the first run to create the database or production, run  python application

for local use and develop

    run python debug.py  

open localhost:5002



大概流程：

1. views.py 首页读取 "http://localhost/books.txt", 得到db文件放置位置（没有保存在本地数据库中），显示在 词库 页面
2. 词库 页面点击， 下载词库， 并添加到 我的词库 页面
3. 我的词库页面 选择词库，即可学习
4. 设置页面。
5. 学习模式分为纯看（回忆）， 纯练（看中翻给例句填单词），和混合（熟练度2以上，随机进行回忆和填空）
