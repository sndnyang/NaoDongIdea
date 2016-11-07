# 说明

[创意脑洞](http://sndnyang.github.io/NaoDong-list.html)

对创意脑洞里脑洞的实现， 目前只有 单词部分功能， 以后完善， 并实现 文学学习等脑洞。

从zhimind知维图拆分出来， 安装 virtualenv， 安装 pip install -r requirements.txt

运行 python debug.py  

打开 localhost:5002

用 python application 创建数据库后运行， 但数据库设置等没有上传， 需要自设。

大概流程：

1. views.py 首页读取 "http://localhost/books.txt", 得到db文件放置位置（没有保存在本地数据库中），显示在 词库 页面
2. 词库 页面点击， 下载词库， 并添加到 我的词库 页面
3. 我的词库页面 选择词库，即可学习
4. 设置页面设置一组词个数。

[zhimind](http://zhimind.com) 这个网站就是知维图，为什么不放上来？ 因为喜欢做梦， 哪怕知道是做梦， 总有做梦的权力。 另外代码质量也很烂， 不敢上传。