# -*- coding:utf-8 -*-
# author: kevin
# CreateTime: 2018/8/16
# software-version: python 3.7


import time
from selenium import webdriver
from selenium.webdriver import Firefox
import os
import pandas as pd

class GetCompanyInfo(object):
    """
    爬取天眼查下的企业的信息
    """
    def __init__(self):
        """
        初始化爬虫执行代理，使用firefox访问
        """
        self.username = ''
        self.password = ''
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument('-headless')  # 无头参数
        self.geckodriver = r'geckodriver'
        self.driver = Firefox(executable_path=self.geckodriver, firefox_options=self.options)

        self.start_url = 'https://www.tianyancha.com'

    def login(self):
        """
        登录并检查状态
        :return:
        """
        # try:
        self.driver.get(self.start_url)

        #print(self.driver.get_cookies())

        username = self.index_login()
        username_pattern = username[:3] + ' **** ' + username[-4:]
        print(username_pattern)
        page = self.driver.page_source
        #print(page)
        is_login = page.find(username_pattern)

        if is_login != -1:
            print('登录成功')

    def index_login(self):
        """
        主页下的登录模式
        :return:
        """
        get_login = self.driver.find_elements_by_xpath('//a[@class="link-white"]')[0]   # 登录/注册
        print(get_login.text)
        # url为login的input
        get_login.click()
        login_by_pwd = self.driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div[2]/div/div/div[3]/div[1]/div[2]")     # 切换到手机登录
        login_by_pwd.click()
        input1 = self.driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[2]/input")     # 手机号码
        input2 = self.driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[3]/input')     # 密码
        #print(input1.get_attribute('placeholder'))
        #print(input2.get_attribute('placeholder'))
        username, password = self._check_user_pass()
        input1.send_keys(username)
        input2.send_keys(password)

        login_button = self.driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[5]')     # 点击登录
        print(login_button.text)
        time.sleep(1)   # 必须等待否则鉴别是爬虫
        login_button.click()
        return username

    def _check_user_pass(self):
        """
        检查是否有帐号密码
        :return:
        """
        if self.username and self.password:
            return self.username, self.password
        else:
            #username = input('输入您的手机号码\n')
            #password = input('输入您的密码\n')
            username = '18842647783'  #注册手机号
            password = 'sc7511779'  #密码
            return username, password

    def login_page_login(self):
        """
        url：www.tianyancha.com/login
        在这个url下的登录模式
        :return:
        """
        input1 = self.driver.find_element_by_xpath('//div[contains(@class,"in-block")'
                                                   ' and contains(@class, "vertical-top")'
                                                   ' and contains(@class, "float-right")'
                                                   ' and contains(@class, "right_content")'
                                                   ' and contains(@class, "mt50")'
                                                   ' and contains(@class, "mr5")'
                                                   ' and contains(@class, "mb5")'
                                                   ']/div[2]/div[2]/div[2]/input')

        input2 = self.driver.find_element_by_xpath('//div[contains(@class,"in-block")'
                                                   ' and contains(@class, "vertical-top")'
                                                   ' and contains(@class, "float-right")'
                                                   ' and contains(@class, "right_content")'
                                                   ' and contains(@class, "mt50")'
                                                   ' and contains(@class, "mr5")'
                                                   ' and contains(@class, "mb5")'
                                                   ']/div[2]/div[2]/div[3]/input')
        print(input1.get_attribute('placeholder'))
        input1.send_keys("")
        print(input2.get_attribute('placeholder'))
        input2.send_keys('')

        login_button = self.driver.find_element_by_xpath('//div[contains(@class,"in-block")'
                                                         ' and contains(@class, "vertical-top")'
                                                         ' and contains(@class, "float-right")'
                                                         ' and contains(@class, "right_content")'
                                                         ' and contains(@class, "mt50")'
                                                         ' and contains(@class, "mr5")'
                                                         ' and contains(@class, "mb5")'
                                                         ']/div[2]/div[2]/div[5]')

        #print(login_button.text)
        time.sleep(1)
        login_button.click()

    def get_company_info(self, company_name):
        """
        获取想要的公司信息
        :param company_name:
        :param company_onwer:
        :return:
        """
        time.sleep(1)
        page = self.driver.page_source

        index_input_company = self.driver.find_element_by_xpath('//input[@id="home-main-search"]')  # 主页搜索框

        index_input_company.send_keys(company_name)
        self.driver.find_element_by_xpath('//div[contains(@class, "input-group-btn")'
                                          ' and contains(@class, "btn")'
                                          ' and contains(@class, "-hg")'
                                          '][1]').click()  # 点击搜索
        print("搜索成功")
        #page = self.driver.page_source
        #print (page)
        "/html/body/div[2]/div/div[1]/div/div[3]/div[1]/div/div[3]/div[1]/a/em"
        # try:
        company_list = self.driver.find_element_by_xpath('.//div[contains(@class, "header")][1]/a[1]') # 获取当前页面所有公司的div
        href = company_list.get_attribute('href')
        self.driver.get(href)  # 进入公司详情页
        company = self.save_company_info()
        return company
        # except:
        #     print('没有搜索到相应的公司')
        #     return company_name

    def save_company_info(self):

        #a = self.driver.find_element_by_xpath('.//div[contains(@class, "nav-item-list list list-hover-show  nav-line")][1]/a[1]/span[1]')
        #print ('___显示手机号已是登录状态____' + a.text)

        company = ''
        # 公司名
        company_name = self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/div[1]/h1')
        company += '公司名：' + company_name.text + '\n'
        # 电话
        phone = self.driver.find_element_by_xpath('.//div[contains(@class, "detail ")][1]/div[1]/div[1]/span[2]')
        company += '电话：' + phone.text + '\n'
        # 邮箱
        email = self.driver.find_element_by_xpath('.//div[contains(@class, "detail ")][1]/div[1]/div[2]/span[2]')
        company += 'email：' + email.text + '\n'

        #e = self.driver.find_element_by_xpath('.//div[@class="detail "][1]/div[1]/div[2]/span[3]/span[1]')
        # 获取更多邮箱
        #email = self.get_email(e)
        # 网址
        try:
            link = self.driver.find_element_by_xpath('.//div[contains(@class, "detail ")][1]/div[2]/div[1]/a[1]')
        except:
            link = self.driver.find_element_by_xpath('.//div[contains(@class, "detail ")][1]/div[2]/div[1]/span[2]')
        company += '网址：' + link.text + '\n'
        print(link.text)
        # 地址
        try:
            ad = self.driver.find_element_by_xpath('.//div[contains(@class, "detail ")][1]/div[2]/div[2]/span[2]')
            address = ad.get_attribute('title')
        except:
            ad = self.driver.find_element_by_xpath('.//div[contains(@class, "detail ")][1]/div[2]/div[2]')
            address = ad.text#
        company += '地址：' + address + '\n'
        # 简介
        try:
            s = self.driver.find_element_by_xpath('.//div[contains(@class, "summary")][1]/span[3]')
            summary = self.get_summary(s)
        except:
            summary = self.driver.find_element_by_xpath('.//div[contains(@class, "summary")][1]/span[2]')
        company += '简介：' + summary.text + '\n'
        #法定代表人
        company += '法定代表人 '
        # 姓名
        name = self.driver.find_element_by_xpath('.//div[contains(@class, "humancompany")][1]/div[1]/a[1]')
        company  += '姓名：' + name.text + '\n'
        # 公司数
        company_num = self.driver.find_element_by_xpath('.//div[contains(@class, "humancompany")][1]/div[2]/span[1]')
        #company['company_num'] = '介绍：' + '他有' + company_num.text+'家公司分布如下'
        #介绍内容

        money = self.driver.find_element_by_xpath('.//div[contains(@id, "_container_baseInfo")][1]/table[1]/tbody[1]/tr[1]/td[2]/div[2]')
        money_reg = money.get_attribute('title')
        company += '注册资本' + money_reg + '\n'

        date_reg = self.driver.find_element_by_xpath('.//div[contains(@id, "_container_baseInfo")][1]/table[1]/tbody[1]/tr[2]/td[1]/div[2]/text[1]')
        company += '注册时间' + date_reg.text + '\n'


        #/html/body/div[2]/div[1]/div/div[3]/div[1]/div/div[2]/div[1]/div[2]/div[2]/table[1]/tbody/tr[3]/td/div[2]
        cancel = self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[3]/div[1]/div/div[2]/div[1]/div[2]/div[2]/table[1]/tbody/tr[3]/td/div[2]')
        company += '公司状态' + cancel.text + '\n'
        print(company)

        maincompany = self.driver.find_elements_by_xpath('.//div[contains(@class, "merge")]/div')
        maincompany_info = ''
        for com in maincompany:
            area = com.find_element_by_xpath('.//div[contains(@class, "title")][1]')
            company_detail = com.find_element_by_xpath('.//div[contains(@class, "maincompany")][1]/span[1]')
            maincompany_info += area.text + company_detail.text + ','
        company += maincompany_info + '\n'
        #工商注册号
        company_content = self.driver.find_elements_by_xpath('.//table[contains(@class, "table")'
                                                             ' and contains(@class, "-striped-col")'
                                                             ' and contains(@class, "-border-top-none")'
                                                             '][1]/tbody[1]/tr')
        business = ''
        for cont in company_content:
            company_title_1 = cont.find_element_by_xpath('.//td[1]')

            company_info_1 = cont.find_element_by_xpath('.//td[2]')
            try:
               company_title_2 = cont.find_element_by_xpath('.//td[3]')
            except:
                pass
            try:
                company_info_2 = cont.find_element_by_xpath('.//td[4]')
            except:
                pass

            business += company_title_1.text + '：' + company_info_1.text + ',' + company_title_2.text + '：' + company_info_2.text + '\n'

        company += business + '\n'
        #微信号码
        try:
            wechat = self.driver.find_element_by_xpath('.//div[contains(@class, "wechat")][1]/div[2]/div[2]/span[2]')
            company += '微信公众号：' + wechat.text + '\n'
        except:
            pass

        print(company)
        # df = pd.DataFrame()
        #
        # df.to_excel("Company_Info.xlsx", index=True, encoding="utf-8")
        return company


        #print(self.driver.page_source)
    # 得到更多邮箱
    # def get_email(self,e):
    #     e.click()
    #     email = self.driver.find_element_by_xpath('.//div[@class="body  -detail modal-scroll text-center"][1]/div[1]/div')
    #
    #     return email

    # 得到简介详情
    def get_summary(self,e):
        e.click()
        summary = self.driver.find_element_by_xpath('.//div[@class="body -detail modal-scroll"][1]')

        return summary

    #得到
    def get_company_name(self):
        f = open('company_name.txt',"r", encoding="utf-8")
        lines = f.readlines()[1:]
        return lines

    def main(self):

        self.login()

        company_name = self.get_company_name()

        for cn in company_name:
            name = cn.split()
            #self.driver.get(self.start_url)
            self.driver.get(self.start_url)
            company = self.get_company_info(name[0])
            if company == name[0]:
                res = company + '没有相关信息' + '\n'
            else:
                res = company

            write_file = os.getcwd() + '/company.txt'
            output = open(write_file, 'a')
            output.write(res)
            output.close()
        self.driver.close()


if __name__ == '__main__':

    # tt = GetCompanyInfo()
    # tt.test()
    time1 = time.time()
    new_crawl = GetCompanyInfo()
    new_crawl.main()
    time2 = time.time()
    print('用时：', int(time2-time1))