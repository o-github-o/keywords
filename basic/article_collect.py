# encoding=utf-8

# 解决cmd命令行下输出中文字符乱码问题(必须放置在文本最前面)
from __future__ import unicode_literals
import sys
import json
import os

# 操作中文必须语句，解决字符问题
reload(sys)
sys.setdefaultencoding('utf8')

import scrapy_handle
import html_handle
import file_handle


# 文章信息记录
def article_record(recordFilePath, articleData):
    # artcileData中包含多组信息，可选择性记录
    file_handle.write_file(recordFilePath, articleData[0])
    file_handle.write_file(recordFilePath, articleData[1])
    file_handle.write_file(recordFilePath, articleData[2])
    file_handle.write_file(recordFilePath, articleData[3])
    file_handle.write_file(recordFilePath, articleData[4])
    file_handle.write_file(recordFilePath, articleData[5])


# 文本全记录
def article_record_all():

    # 《界面》文章标签文件的抓取
    tagDatas = []
    recordCount = 0
    flag = 1000000
    # 统计文章标签来源于词频正确率
    fileCount = 0
    tagCount = 0
    while flag <= 1400000:
        baseurl = 'http://www.jiemian.com/article/%d.html' % (flag)
        # 进行文本抓取
        text = scrapy_handle.get_html_data(baseurl)
        # 进行文本信息获取
        if not text:
            flag += 1
            continue
        else:
            # 进行文本信息获取
            article_data = html_handle.get_article_data(text)
            # print article_data

            # 进行文本信息的记录(便于打印输出)
            # type = json.dumps(article_data[0], ensure_ascii=False)
            # title = json.dumps(article_data[1], ensure_ascii=False)
            # sub_title = json.dumps(article_data[2], ensure_ascii=False)
            # date = json.dumps(article_data[3], ensure_ascii=False)
            # tags = json.dumps(article_data[4], ensure_ascii=False)
            # content = json.dumps(article_data[5], ensure_ascii=False)
            # print type, title, sub_title, date, tags, content
            # print type, title, date, tags

            # 若数据为空，不进行记录操作
            if len(article_data) == 0:
                flag += 1
                continue

            # 定义储存文件类型
            file_type = {
                u"金融": "finance",
                u"理财": "financing",
                u"基金": "fund",
                u"私募": "private",
                u"股票": "shares",
                u"保险": "insurance",
                u"今日投资": "investment",
            }
            # 类型判断
            if file_type.get(article_data[0]):
                file_folder = file_type.get(article_data[0])
                recordFileName = 'corpus/' + file_folder + '/' + file_folder + '_' + str(flag) + '.txt'
            else:
                flag += 1
                continue

            # 文章数据记录
            recordFileName = file_type.get(article_data[0]) + '_' + str(flag) + '.txt'
            # 按照标签分类存储
            # 文章原始标签
            tagList = article_data[4].split(',')
            for tag in tagList:
                # 进行文件夹记录，名称为标签名
                recordPath = 'corpus/' + tag
                if not os.path.exists(recordPath):
                    os.makedirs(recordPath)
                recordFilePath = os.path.join(recordPath, recordFileName)
                # 仅存储文章标题和正文
                file_handle.write_file(recordFilePath, article_data[1])  # 类型暂时不写入，直接通过文件名区分
                file_handle.write_file(recordFilePath, article_data[2])
                file_handle.write_file(recordFilePath, article_data[5])

            fileCount += 1
            print "当前已处理文章数为： ", fileCount, "当前文章号为：", flag
            # if fileCount >= 1:
            #     break

        flag += 1
    pass

# 此下面的语句被import引入后不会执行
if __name__ == "__main__":
    print 'hello'
    # 获取原始html数据
    flag = 1000001
    # flag = 1000003
    url = 'http://www.jiemian.com/article/%d.html' % flag
    htmlData = scrapy_handle.get_html_data(url)
    # html数据处理
    type, title, sub_title, date, tags, content = html_handle.get_article_data(htmlData)
    articleData = html_handle.get_article_data(htmlData)

    # 文章记录
    recordFilePath = 'corpus/' + str(flag) + '.txt'
    article_record(recordFilePath, articleData)
    