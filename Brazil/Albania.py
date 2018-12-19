# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 16:24:30 2018

@author: E430C-3013
"""

import requests
from bs4 import BeautifulSoup as bsp
from google_translate import googleapis_translate
import time
import pyodbc
import datetime
from pybloom_live import BloomFilter
import os
from lxml import etree
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }

source = 'https://telegrafi.com/'
country='Albania'
DATABASE='Albania'

if os.path.exists('布隆文件/{}.blm'.format(DATABASE)):#判断布隆文件是否存在
    bf =BloomFilter.fromfile(open('布隆文件/{}.blm'.format(DATABASE),'rb'))
else:
    bf = BloomFilter(1000000,0.001)  
    
def get_html(url,count=1):#获取html
	if count > 3:#请求超过三次就返回空
		return None
	try:
		r=requests.get(url,headers=headers,timeout=15)#请求html，超时设为15秒
		return r.text
	except:
		count+=1
		return get_html(url,count)  

def Translate(originaltitle,createtime,author,originalcontent,articlesource,label,keyword,url,originaldetails):#翻译函数，翻译完直接存入数据库中
#    print('_____________原始内容_______________{}'.format(originaldetails))
    details=''
    Englishdetails=''
    length1=len(originaldetails)
    number=length1//1000
    for nn in range(number+1):
        contentx=originaldetails[nn*1000:(nn+1)*1000]
        details=details+str(googleapis_translate(contentx,from_lang='auto')).replace("'","''")
        Englishdetails=Englishdetails+str(googleapis_translate(contentx,from_lang='auto',to_lang='en')).replace("'","''")
    Englishcontent = str(googleapis_translate(originalcontent, from_lang='auto', to_lang='en')).replace("'","''")
    Englishtitle = str(googleapis_translate(originaltitle, from_lang='auto', to_lang='en')).replace("'","''")
    content = str(googleapis_translate(originalcontent, from_lang='auto')).replace("'","''")
    title = str(googleapis_translate(originaltitle, from_lang='auto')).replace("'","''")
    sql1 = "insert into Albania (title,originaltitle,createtime,author,content,originalcontent,articlesource,source,label,keyword,country,url,Englishtitle,Englishcontent,details,originaldetails,Englishdetails,currenttime) values (N'" + title + "',N'" +originaltitle + "',N'" +createtime + "',N'" +author + "',N'" +content + "',N'" +originalcontent + "',N'" +articlesource + "',N'" +source + "',N'" +label + "',N'" +keyword + "',N'" +country + "',N'" +url + "',N'" +Englishtitle + "',N'" +Englishcontent + "',N'" +details + "',N'" +originaldetails + "',N'" +Englishdetails + "',GETDATE())"
    conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 10.0};SERVER=192.168.2.8;DATABASE=Yuqing;UID=sa;PWD=sinoimex2004*')
    
#    sql1 = "insert into yuqing (title,originaltitle,createtime,author,content,originalcontent,articlesource,source,label,keyword,country,url,Englishtitle,Englishcontent,details,originaldetails,Englishdetails,currenttime) values (N'" + title + "',N'" +originaltitle + "',N'" +createtime + "',N'" +author + "',N'" +content + "',N'" +originalcontent + "',N'" +articlesource + "',N'" +source + "',N'" +label + "',N'" +keyword + "',N'" +country + "',N'" +url + "',N'" +Englishtitle + "',N'" +Englishcontent + "',N'" +details + "',N'" +originaldetails + "',N'" +Englishdetails + "',GETDATE())"
#    conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 10.0};SERVER=localhost;DATABASE=Yuqing;UID=sa;PWD=sinoimex2004*')
    cur = conn.cursor()
    cur.execute(sql1)
    cur.commit()
    conn.close()

def get_next_page(url):#加载下一页
    html=get_html(url)
    if html:#如果获取到了html
        soup=bsp(html,'html.parser')
        try:
            nextpage=soup.find(class_="load-more").get('href')#通过获取到的html中"load-more"标签和它的属性
        except:
            nextpage=''#找不到的话就下一页为空
        return nextpage

def getCon():
    global error_url#申明错误链接-全局变量
    error_url=''    
    urllist2=[]
    html=get_html(source)#调用get_html，根据源网址获取html

    soup=bsp(html,'lxml')#调用bsp解析html
    urllist1=soup.find(class_="main-menu").find_all('a')[0:85]
    for url1 in urllist1:
        urllist2.append(url1.get('href'))
    urllist2.remove('https://telegrafi.com/lajme/')
    urllist2.remove('https://telegrafi.com/ekonomi/')
    urllist2.remove('https://telegrafi.com/sport/')
    urllist2.remove( 'https://telegrafi.com/magazina/')
    urllist2.remove('https://telegrafi.com/kultura/')
    urllist2.remove('https://telegrafi.com/femra/')
    urllist2.remove('https://telegrafi.com/stili/')
    urllist2.remove('https://telegrafi.com/shendetesi/')
    urllist2.remove('https://telegrafi.com/kuzhina/')
    urllist2.remove('https://telegrafi.com/auto/')
    urllist2.remove('https://telegrafi.com/teknologji/')
    urllist2.remove('https://telegrafi.com/fun/')
    # urllist2.remove('https://telegrafi.com/rusia-2018/')
    urllist2.remove('https://telegrafi.com/sport/livescore/')
    urllist2.remove('https://telegrafi.com/category/lajme/maqedoni/')
    for k in urllist2:
        label=k.split('/')[4]#将第五块，e.g. lajme/maqedoni 作为标签
        for j in range(0,1000):
            if j==0:#爬取第一页时
                base_url=k#基础url还是等于第一页的url
            else:
                nextpage=get_next_page(base_url)#不是第一页时就进行下一页
                if nextpage=='':#下一页为空则跳出循环
                    break
                else:
                    base_url=nextpage#否则一直循环爬取下一页
            print('正在爬列表页 '+str(base_url))
            html1=get_html(base_url)#调用函数获取html
#            soup1=bsp(html1,'html.parser')
#            print(label)
#            titlelist=soup1.find(class_="row cat-list").find_all(class_="col-md-24 cat-box cat-color-"+label+"" )
#            length=len(titlelist)
            selector = etree.HTML(html1)#etree解析html
            titlelist=selector.xpath('/html/body/div[7]/div/div[1]/div[2]/div/a/@href')#xpath获取新闻标题链接
            for i in titlelist:#
                url=i
                error_url=url
                if url in bf:#判断url是否在布隆文件中
                    break
                else:
                    bf.add(url)#没有的话，先将url添加到布隆文件中
                    print('正在爬详情页 '+ url)
                    html=get_html(url)#获取新闻的html
                    if html:#如果获取到html的话，用bsp解析
                        soup=bsp(html,'html.parser')
                        try:
                            originaltitle=soup.find(class_="col-md-24 article-title").find('h1').text.strip().replace("'","''")#soup找originaltitle
                        except:
                            originaltitle=soup.find(class_="article-heading").find('h1').text.strip().replace("'","''")#不成功的话，换一个class_找
                        try:#抓取并处理文章创建的时间
                            time1=soup.find(class_="col-sm-6 article-published-at tar col-xs-12 col-sm-push-15").text.strip()
                            timearray=time.strptime(time1,'%d.%m.%Y • %H:%M')
                            createtime=time.strftime("%Y/%m/%d %H:%M",timearray)
                            print(createtime)
                        except:#抓取失败的话，直接使用当前的时间代替
                            createtime=datetime.datetime.now().strftime('%Y/%m/%d %H:%M')
                        articlesource=''
                        author=''
                        keyword=''
                        try:
                            originalcontent=soup.find(class_="col-md-23").find('p').text.strip().replace("'","''")#抓源内容
                            conlen=len(originalcontent)#内容长度
                            if conlen>230:
                                originalcontent=originalcontent[:231].replace("'","''")#内容长度限制231个字节之内
                            else:
                                originalcontent=originalcontent.replace("'","''")
                        except:
                            originalcontent=''
                        originaldetails=''
                        try:
                            article=soup.find(class_="col-md-23").find_all('p')#抓取所有文章
                            for itemn in article:
                                if itemn.text.strip()=='':
                                    continue
                                originaldetails=originaldetails+itemn.text.strip().replace("'","''")+'\n'
                        except:
                            originaldetails=soup.find(class_="article-body").text.replace("'","''")
                        if originalcontent=='':
                            originalcontent=originaldetails[0:230]#源内容如果为空，则用源详情代替（取230个字节）
                        Translate(originaltitle,createtime,author,originalcontent,articlesource,label,keyword,url,originaldetails)#调用google_translate对抓取的内容进行翻译
                        url=''#下次循环之前将url附为空值
            bf.tofile(open('布隆文件/{}.blm'.format(DATABASE),'wb'))
            if url in bf:#接着上一个break，如果url还在里面的话，继续跳出循环
                break
    print('爬取完成')
        
def main():#主函数
    getCon()
def run():
    try:
        main()    
    except:
        name='Albania'
        source='https://telegrafi.com/'
        country='Albania'
        stoptime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        import traceback
        error=str(traceback.format_exc()).replace("'","''")
        sql_insert="insert into ErrorMessage(name,source,country,stoptime,error,error_url,infostatus) values('"+name+"','"+source+"','"+country+"','"+stoptime+"','"+error+"','"+error_url+"','否')"
        conn=pyodbc.connect(r'DRIVER={SQL Server Native Client 10.0};SERVER=192.168.2.8,1433;DATABASE=Error;UID=sa;PWD=sinoimex2004*')
        cur=conn.cursor()
        cur.execute(sql_insert)
        cur.commit()
        conn.close()  
        sql_update="update logmessage set is_error=1 where process_name='"+name+"' and id=(select MAX(id) from logmessage where process_name='"+name+"' ) "
        conn1=pyodbc.connect(r'DRIVER={SQL Server Native Client 10.0};SERVER=localhost;DATABASE=Error;UID=sa;PWD=sinoimex2004*')
        cur1=conn1.cursor()
        cur1.execute(sql_update)
        cur1.commit()
        conn1.close()  
      
if __name__ == '__main__':
   main()
