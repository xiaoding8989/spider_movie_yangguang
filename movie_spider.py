# usr/bin/env python
# -*-coding:utf-8 -*-
import time
import pymysql
import re
import urllib
class Mysqldb(object):
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        passwd="123456",
        db="spider",
        charset="utf8"
    )
    cur=conn.cursor()

    # def insertmovie(self, title, url, content):
    #     # print title,url,content
    #     sql = "insert into movie(title,url,content) VALUES ('%s','%s','%s')" % (title, url, content)
    #     self.cur.execute(sql)
    #     self.conn.commit()
    def insertmovie(self,sql2):
        # print title,url,content
        sql = "insert into movie(title,url,content) VALUES"
        sql+=sql2
        print "the sql is:",sql
        self.cur.execute(sql)
        self.conn.commit()

mdb=Mysqldb()
domain="http://www.ygdy8.net"
def getList(i):
    url_list=[]
    url="http://www.ygdy8.net/html/gndy/oumei/list_7_"+str(i)+".html"
    print url
    html=urllib.urlopen(url)
    text=html.read()
    text=text.decode("gbk","ignore").encode("utf-8")
    #print text
    reg = re.compile(r'<td height="26">.*?<a href="(.*?)" class="ulink">.*?(《.*?》).*?</a>.*?</td>', re.S)
    #reg = re.compile(r'<td height="26">.*?<a href="(.*?)" class="ulink">',re.S)
    items=re.findall(reg,text)
    for item in items:
        try:
           url=domain+item[0]
           url_list.append(url)
        except Exception,e:
            print e
    return url_list


sql1=""
def getmovie(url):
    global sql1
    html = urllib.urlopen(url)
    text = html.read()
    text = text.decode("gbk", "ignore").encode("utf-8")
    pattern_title=re.compile(r'<title>.*?(《.*?》).*?</title>',re.S)
    pattern = re.compile(r"◎简　　介<br /><br />　　(.*?)<br />", re.S)
    title=pattern_title.findall(text)
    content = pattern.findall(text)
    try:
        title=title[0]
        content = content[0]
    except Exception,e:
        print "the problem url is:",url,"title is :",title,"content is :",content,"problem is:",e
    sql2 = title, url, content
    sql1 +=str(sql2)+","
    sql1=sql1[:-1]
    #通过实例mdb调用插入数据的方法，将获取的数据插入数据库
    # try:
    #     mdb.insertmovie(title,url,content)
    #     print "insert db success"
    # except Exception,e:
    #     print "insert moviedb is problem is url is:",url,"title:",title,"content:",content
    #     print e


i=1
while i<=155:
    print "i is:",i
    url_list=getList(i)
    for url in url_list:
        getmovie(url)
    i+=1
    #print "the sql1 is :",sql1
    try:
        mdb.insertmovie(sql1)
        print "insert db success."
    except Exception,e:
        print "insert db probled is:",e

    break
    #time.sleep(5)

