#-*- encoding:utf-8 -*-

import os
import json
import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence

# 获取文本关键词
def getTextKeywords(filename, count = 5, path = 'corpus'):
    # filepath = os.path.join(path, filename)
    file = codecs.open(filename, 'a+', 'utf-8')
    text = file.read()

    # 添加自定义文件
    # 结束词、词性、分词标记均可自己定义

    # 词性保留文件
    # allow_speech_tags = ['an', 'i', 'j', 'l', 'n', 'nr', 'nrfg', 'ns', 'nt', 'nz', 't', 'v', 'vd', 'vn', 'eng']

    # 词性保留文件(去除动词的关键短语)
    allow_speech_tags = ['an', 'i', 'j', 'l', 'n', 'nr', 'nrfg', 'ns', 'nt', 'nz', 'eng']
    # 关键词处理
    tr4w = TextRank4Keyword()                               # 默认方式
    # tr4w = TextRank4Keyword(None, allow_speech_tags)      # 去除指定词性单词
    tr4w.analyze(text=text, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
    keyWords = []
    for item in tr4w.get_keywords(count, word_min_len=2):
        # unicodestring = item.word
        # utf8string = unicodestring.encode("utf-8")
        # keyWords.append(utf8string)
        keyWords.append(item.word)
    return keyWords

if __name__ == "__main__":
    print "hello"
    filePath = 'corpus/1000005.txt'
    print json.dumps(getTextKeywords(filePath, 10), ensure_ascii=False)