# -*- coding: UTF-8 -*-
import os
import whoosh
from whoosh.index import create_in, open_dir
from whoosh.fields import *

from whoosh.qparser import QueryParser
import json
import jieba
from jieba.analyse import ChineseAnalyzer
jieba.load_userdict(u"./customDict.txt")

analyzer = ChineseAnalyzer()

schema = Schema(title=TEXT(stored=True, analyzer = analyzer), url=TEXT(stored=True), content=TEXT(stored=True, analyzer=analyzer))
if not os.path.exists(u"tmp"):
    os.mkdir(u"tmp")

ix = open_dir("tmp") # for read only
# ix = create_in(u"tmp", schema) # for create new index
# writer = ix.writer()

# k = json.load(open(u'./anew.json'))
# for item in k:
#     writer.add_document(
#     title=item[u'title'],
#     url=item[u'url'],
#     content=item[u'text']
# )
# k = json.load(open(u'./bnew.json'))
# for item in k:
#     writer.add_document(
#     title=item[u'title'],
#     url=item[u'url'],
#     content=item[u'text']
# )

# writer.commit()
parser = QueryParser("content", schema=ix.schema)

def search(keyword):
    q = parser.parse(keyword)
    with ix.searcher() as searcher:
        results = searcher.search(q)
        list = []
        if (results.scored_length() > 0):
            for i in xrange(min(3, results.scored_length())):
                list.append({u"标题": results[i]['title'], u"地址": results[i]['url'], u"正文摘要": results[i].highlights("content")})
        else:
            list.append({u"标题": u"护花呤使用指南目录", u"地址": u"http://huhualing.net/bbs2/", u"正文摘要": u"请点击链接访问首页"})
        return list
