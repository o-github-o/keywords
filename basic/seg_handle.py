# encoding=utf-8

# 解决cmd命令行下输出中文字符乱码问题(必须放置在文本最前面)
from __future__ import unicode_literals
import sys
import json
import os

# 操作中文必须语句，解决字符问题
reload(sys)
sys.setdefaultencoding('utf8')

import jieba
jieba.load_userdict("../dict_file/dict.txt.big")
import jieba.posseg as pseg
import operator
import file_handle
import scrapy_handle
import html_handle

# jieba分词
# 词性过滤文件(保留形容词、副形词、名形词、成语、简称略语、习用语、动词、动语素、副动词、名动词、名词)
ALLOW_SPEECH_TAGS = ['a', 'ad', 'an', 'i', 'j', 'l', 'v', 'vg', 'vd', 'vn', 'n']

# 读入文章，分词，写入文件
# flag：True 表明此文件后续会继续被处理，所以只有分词 False，则可以美一点
# 返回分词的数量
def seg_file(originalFilePath, segFilePath, flag = True):
    stopWords = [line.strip().decode('utf-8') for line in open('../dict_file/stop_words.txt').readlines()]
    try:
        # 进行文章的读取
        fileObject = open(originalFilePath, 'r+')
        fileData = fileObject.read()

        # 进行文章的分词操作
        psegList = pseg.cut(fileData)

        # 进行分词文件的创建
        segFileObject = open(segFilePath, 'w')
        # 进行分词数量的记录
        wordCount = 0

        # 进行分词文件的记录
        for line in psegList:
            if line.flag in set(ALLOW_SPEECH_TAGS) and line.word not in stopWords and len(line.word) > 1:
                wordCount += 1
                segFileObject.write(line.word)
                segFileObject.write('\n')  # 显式写入换行

                # if flag:
                #     segFileObject.write(line.word)
                #     segFileObject.write('\n')  # 显式写入换行
                # else:
                #     segFileObject.write(str(wordCount))
                #     segFileObject.write('\t')
                #     segFileObject.write(line.word)
                #     segFileObject.write('\t')
                #     segFileObject.write(line.flag)
                #     segFileObject.write('\n')  # 显式写入换行

        return wordCount

    finally:
        pass
        # fileObject.close()
        # segFileObject.close()



# 分词后文件记录
# flag:True 降序输出 False 升序输出
def record_file(segFilePath, recordFilePath, totalCount, flag = True):
    try:
        # 计算词频
        segFileObject = open(segFilePath, 'r')  # 进行分词文件的读取
        wordDatas = {}
        for line in segFileObject:
            word = line.strip('\n')  # 去除换行符
            if wordDatas.has_key(word):
                wordDatas[word] = (wordDatas.get(word) + 1)
            else:
                wordDatas[word] = 1
        if flag:
            sortedWordDatas = sorted(wordDatas.iteritems(), key=lambda d: d[1], reverse=True)  # 降序排列
        else:
            sortedWordDatas = sorted(wordDatas.items(), key=operator.itemgetter(1))  # 升序排列

        # 进行记录文件的创建
        recordFileObject = open(recordFilePath, 'w')
        recordFileObject.write("当前文章分词后共有单词数量为： ")
        recordFileObject.write(str(totalCount))
        recordFileObject.write('\n')
        for line in sortedWordDatas:
            recordFileObject.write(line[0])
            recordFileObject.write('\t')
            recordFileObject.write(str(line[1]))
            recordFileObject.write('\n')  # 显示写入换行

    finally:
        segFileObject.close()
        segFileObject.close()


# 文件分词记录集中函数
def seg_handle(originalFileName):
    curDir = file_handle.cur_file_dir()
    originalFilePath = os.path.join(curDir, originalFileName)
    # 根据原始文章名称自动进行分词文件和记录文件的命名
    segFilePath = originalFilePath.strip('.txt') + '_seg.txt'
    recordFilePath = originalFilePath.strip('.txt') + '_record.txt'
    wordCount = seg_file(originalFilePath, segFilePath)
    record_file(segFilePath, recordFilePath, wordCount)


# 直接进行数据的分词记录
def seg_data(contentData):
    # 加载停用词文件
    # jieba.analyse.set_stop_words('dict_file/stop_words.txt')
    stopWords = [line.strip().decode('utf-8') for line in open('../dict_file/stop_words.txt').readlines()]
    # 进行文章的分词操作
    psegList = pseg.cut(contentData)
    wordDatas = {}
    for word in psegList:
        # 添加关键词长度限制,大于1
        if word.flag in set(ALLOW_SPEECH_TAGS) and word.word not in stopWords and len(word.word) > 1:
            if wordDatas.has_key(word.word):
                wordDatas[word.word] = (wordDatas.get(word.word) + 1)
            else:
                wordDatas[word.word] = 1

    sortedWordDatas = sorted(wordDatas.iteritems(), key=lambda d: d[1], reverse=True)  # 降序排列
    return sortedWordDatas


# 此下面的语句被import引入后不会执行
if __name__ == "__main__":
    print 'hello'
    # 处理文本数据
    originalFileName = 'corpus/1000005.txt'
    seg_handle(originalFileName)

    # 处理内存数据
    # 获取原始html数据
    flag = 1000001
    # flag = 1000003
    # url = 'http://www.jiemian.com/article/%d.html' % flag
    # htmlData = scrapy_handle.get_html_data(url)
    # # html数据处理
    # type, title, sub_title, date, tags, content = html_handle.get_article_data(htmlData)
    # # articleData = html_handle.get_article_data(htmlData)
    # wordsData = seg_data(content)
    # print wordsData
    # for i in range(len(wordsData)):
    #     print json.dumps(wordsData[i][0], ensure_ascii=False), wordsData[i][1]