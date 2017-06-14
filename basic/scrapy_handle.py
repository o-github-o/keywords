# encoding=utf-8

# 解决cmd命令行下输出中文字符乱码问题(必须放置在文本最前面)
from __future__ import unicode_literals
import sys
import json
import os

# 操作中文必须语句，解决字符问题
reload(sys)
sys.setdefaultencoding('utf8')

import requests

# url爬取
def get_html_data(url):
    # 进行文本抓取
    response = requests.get(url)
    if response.status_code != 200:
        return False
    else:
        return response.text

# 此下面的语句被import引入后不会执行
if __name__ == "__main__":
    print 'hello'
    flag = 1000001
    url = 'http://www.jiemian.com/article/%d.html' % flag
    htmlData = get_html_data(url)
    print htmlData
    