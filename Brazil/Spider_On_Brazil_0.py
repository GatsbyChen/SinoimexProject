import requests
from bs4 import BeautifulSoup as bsp
from google_translate import googleapis_translate
import time
import pyodbc
import datetime
from pybloom_live import BloomFilter
import os
from lxml import etree

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
source = 'http://www.mdic.gov.br/index.php/comercio-exterior/defesa-comercial/851-investigacoes-em-curso'
country='Brazil'
DATABASE='Brazil'

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

# def Translate(research_type, process, NCM, survey_country, applicant, trade_behavior, situation, questionnaire, recall_deadline):#翻译函数，翻译完直接存入数据库中
def Translate(all_content):
    product = str(googleapis_translate(all_content[0], from_lang='auto')).replace("'", "''")
    research_type = str(googleapis_translate(all_content[1], from_lang='auto')).replace("'","''")
    process = str(googleapis_translate(all_content[2], from_lang='auto')).replace("'", "''")
    NCM = str(googleapis_translate(all_content[3], from_lang='auto')).replace("'", "''")
    survey_country = str(googleapis_translate(all_content[4], from_lang='auto')).replace("'", "''")
    applicant = str(googleapis_translate(all_content[5], from_lang='auto')).replace("'", "''")
    trade_behavior = str(googleapis_translate(all_content[6], from_lang='auto')).replace("'", "''")
    situation = str(googleapis_translate(all_content[7], from_lang='auto')).replace("'", "''")
    questionnaire = str(googleapis_translate(all_content[8], from_lang='auto')).replace("'", "''")
    recall_deadline = str(googleapis_translate(all_content[9], from_lang='auto')).replace("'", "''")
    sql1 = "insert into dbo.Brazil_anti_trade(product,research_type, process, NCM, survey_country, applicant, trade_behavior, situation, questionnaire, recall_deadline, reptile_time) values (N'" + product + "',N'" +research_type + "',N'" +process + "',N'" +NCM + "',N'" +survey_country + "',N'" +applicant + "',N'" +trade_behavior + "',N'" + situation + "',N'" +questionnaire + "',N'" +recall_deadline + "',getdate())"
    conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 10.0};SERVER=192.168.2.160;DATABASE=result;UID=sa;PWD=1234')
    cur = conn.cursor()
    cur.execute(sql1)
    cur.commit()
    conn.close()
    return research_type

def getCon():
    global error_url#申明错误链接-全局变量
    error_url=''
    html=get_html(source)#调用get_html，根据源网址获取html
    soup=bsp(html,'lxml')#调用bsp解析html
    table = soup.find(class_="item-page").find('table')
    urllist1 = table.find_all('a')
    print(urllist1)
    urllist2  = ['http://www.mdic.gov.br' + i.get('href') for i in urllist1]
    # urllist1=soup.find(class_="item-page").find_all('table')
    # print(urllist1[0].get('href'))
    stronglist = ['Tipo de Investigação:  ', 'Processo:', 'NCM:', 'Países Investigados:', 'Peticionária:',
                  'Atos da Secretaria de Comércio Exterior:', 'Situação Atual:', 'Questionários',
                  'Prazos para resposta aos questionários:']
    for i in urllist2:
        all_content = []
        locallist = []
        contentlist = []
        html_sub = get_html(i)
        details_final = 0
        soup = bsp(html_sub, 'html.parser')
        product = soup.find(class_='documentFirstHeading').find('a').text.strip()
        all_content.append(product)
        print(product)
        table = soup.find(class_='item-page').find_all('p')
        for i in table:
            contentlist.append(i.text)
        print(contentlist)

        # for j in stronglist:
        #     locallist.append(contentlist.index(j))
        # for i in range(len(locallist)-1):
        #     details_begin = locallist[i]+1
        #     details_end =  locallist[i+1]
        #     details_final = locallist[-1]+1
        #     all_content.append(contentlist[details_begin:details_end])
        #     print(contentlist[details_begin:details_end])
        # all_content.append(contentlist[details_final:])#all_content就是要抓取的全部内容
        # print(contentlist[details_final:])
        # Translate(all_content)
        # time.sleep(3)




    html1 = get_html(urllist2[0])
    # selector = etree.HTML(html1)
    # research_type = selector.xpath('//*[@id="content-section"]/div/div[1]')
    # print(research_type)
    soup = bsp(html1, 'html.parser')
    table = soup.find(class_ = 'item-page').find_all('p')
    stronglist = ['Tipo de Investigação:  ', 'Processo:', 'NCM:', 'Países Investigados:', 'Peticionária:', 'Atos da Secretaria de Comércio Exterior:', 'Situação Atual:', 'Questionários', 'Prazos para resposta aos questionários:']
    contentlist = []
    for i in table:
        contentlist.append(i.text)
    for j in stronglist:
        print(contentlist.index(j))
    print(contentlist[20:])
    trans = Translate(contentlist[20:])
    print(trans)
    # list = ['Tipo de Investigação:  ', 'Processo:', 'NCM:', 'Países Investigados:', 'Peticionária:', 'Atos da Secretaria de Comércio Exterior:', 'Situação Atual:', 'Questionários', 'Prazos para resposta aos questionários:']
    # content = selector.xpath('//*[@id="content-section"]//div[@class="item-page"]/p[1]/span/strong/text()')
    # research_type = selector.xpath('//*[@id="content-section"]/div/div[1]/p[2]/span/text()')
    # print(research_type)
    # process = selector.xpath('//*[@id="content-section"]/div/div[1]/p[4]/span/text()')
    # print(process)
    # NCM1 = selector.xpath('//*[@id="content-section"]/div/div[1]/p[6]/span/text()')
    # NCM2 = selector.xpath('//*[@id="content-section"]/div/div[1]/p[7]/span/text()')
    # NCM = NCM1+NCM2
    # print(NCM)
    # #这里有多个国家的话需要判断
    # survey_country = selector.xpath('//*[@id="content-section"]/div/div[1]/p[9]/span/text()')
    # print(survey_country)
    # applicant = selector.xpath('//*[@id="content-section"]/div/div[1]/p[12]/span/text()')
    # print(applicant)
    # #贸易行为是url，下载文档
    # trade_behavior = selector.xpath('//*[@id="content-section"]/div/div[1]/p[14]/span/a/text()')
    # print(trade_behavior)
    # situation = selector.xpath('//*[@id="content-section"]/div/div[1]/p[16]/span/text()')
    # print(situation)
    # questionnaire = selector.xpath('//*[@id="content-section"]/div/div[1]/p[19]/a/text()')
    # print(questionnaire)
    # recall_deadline = selector.xpath('//*[@id="content-section"]/div/div[1]/p[21]/text()')
    # print(recall_deadline)
    # a = selector.xpath('//*[@id="content-section"]/div/div[1]/p[26]')
    # print(a)















getCon()
'''
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
'''