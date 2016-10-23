# usr/bin/env python
# -*-coding:utf-8 -*-
import urllib
import re
import threading
from threading import Thread

gMovieurlLis=[]
gCondition=threading.Condition()

#构建消费者，任务是从生产者那里获取url，调用getmovie方法消费url
class Consumer(Thread):
    def run(self):
        global gMovieurlLis
        global gCondition
        print ('%s started'% threading.currentThread())
        while True:
            gCondition.acquire()
            print('%s: trying to download movie. Queue length is %d' % (threading.current_thread(), len(gMovieurlLis)))
            while len(gMovieurlLis)==0:
                gCondition.wait()
                print('%s: waken up. Queue length is %d' % (threading.current_thread(), len(gMovieurlLis)))
            url=gMovieurlLis.pop()
            #在下载之前就将锁释放掉，关键数据是gMovieurlLis列表里的数据用锁对它进行保护就是
            gCondition.release()
            getmovie(url)


class Producer(Thread):
    def run(self):
        global gMovieurlLis
        global gCondition
        print('%s started' % threading.current_thread())
        i=1
        while i<=155 :   #不停地往金库里放钱
            movies = getList(i)
            gMovieurlLis.extend(movies)
            gCondition.acquire()  #上锁
            print('%s: Produced %d. Left %d' % (threading.current_thread(),len(movies),len(gMovieurlLis)))
            gCondition.notify_all()  #这时门口排了很长的队，需要通知所有人
            gCondition.release()   #通知完后释放锁
            i+=1

#获取电影Url的代码
domain = "http://www.ygdy8.net"
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

#从获取的url里下载电影的名字与简介的代码：
def getmovie(url):
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

    #通过实例mdb调用插入数据的方法，将获取的数据插入数据库
    # try:
    #     mdb.insertmovie(title,url,content)
    #     print "insert db success"
    # except Exception,e:
    #     print "insert moviedb is problem is url is:",url,"title:",title,"content:",content
    #     print e

if __name__=="__main__":
    Producer().start()
    for i in range(5):
        Consumer().start()


