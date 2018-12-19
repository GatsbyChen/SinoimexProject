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
    research_type = str(googleapis_translate(' '.join(all_content[1]).strip(), from_lang='auto')).replace("'","''")
    process = str(googleapis_translate(' '.join(all_content[2]).strip(), from_lang='auto')).replace("'", "''")
    NCM = str(googleapis_translate(' '.join(all_content[3]), from_lang='auto')).replace("'", "''")
    survey_country = str(googleapis_translate(' '.join(all_content[4]), from_lang='auto')).replace("'", "''")
    applicant = str(googleapis_translate(' '.join(all_content[5]), from_lang='auto')).replace("'", "''")
    trade_behavior = str(googleapis_translate(' '.join(all_content[6]), from_lang='auto')).replace("'", "''")
    situation = str(googleapis_translate(' '.join(all_content[7]), from_lang='auto')).replace("'", "''")
    questionnaire = str(googleapis_translate(' '.join(all_content[8]), from_lang='auto')).replace("'", "''")
    recall_deadline = str(googleapis_translate(' '.join(all_content[9]), from_lang='auto')).replace("'", "''")
    sql1 = "insert into dbo.Brazil_anti_trade(product,research_type, process, NCM, survey_country, applicant, trade_behavior, situation, questionnaire, recall_deadline, reptile_time) values (N'" + product + "',N'" +research_type + "',N'" +process + "',N'" +NCM + "',N'" +survey_country + "',N'" +applicant + "',N'" +trade_behavior + "',N'" + situation + "',N'" +questionnaire + "',N'" +recall_deadline + "',getdate())"
    conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 10.0};SERVER=192.168.2.160;DATABASE=result;UID=sa;PWD=1234')
    cur = conn.cursor()
    cur.execute(sql1)
    cur.commit()
    conn.close()
    print('"'+product+'"'+' done!')
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
    stronglist = ['Tipo de Investigação', 'Processo', 'NCM', 'Países Investigados', 'País Investigado','Peticionária',
                  'Atos da Secretaria de Comércio Exterior', 'Situação Atual', 'Questionários',
                  'Prazos para resposta aos questionários']
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
            contentlist.extend(i.text.strip().split(":"))
        # print(contentlist)
        for j in stronglist:
            # try:
            #     locallist.append(contentlist.index(j))
            # except:
            #     locallist.append(0)
            try:
                locallist.append(contentlist.index(j))
            except:
                continue
        for i in range(len(locallist)-1):
            details_begin = locallist[i]+1
            details_end =  locallist[i+1]
            details_final = locallist[-1]+1
            all_content.append(contentlist[details_begin:details_end])
            print(contentlist[details_begin:details_end])
        all_content.append(contentlist[details_final:])#all_content就是要抓取的全部内容
        print(contentlist[details_final:])
        Translate(all_content)
        time.sleep(5)

def Bloom_trigger():
    html=get_html(source)#调用get_html，根据源网址获取html
    soup=bsp(html,'lxml')#调用bsp解析html
    table = soup.find(class_="item-page").find('table')
    urllist1 = table.find_all('a')
    print(urllist1)
    urllist2  = ['http://www.mdic.gov.br' + i.get('href') for i in urllist1]
    while True:
        if urllist2[0] in bf:
            time.sleep(3600)
        else:
            for i in urllist2:
                bf.add(i)
            bf.tofile(open('布隆文件/{}.blm'.format(DATABASE), 'wb'))
            getCon()
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    Bloom_trigger()


















