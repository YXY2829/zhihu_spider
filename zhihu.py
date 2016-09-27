#coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent
import MySQLdb
import time
import re

class Zhihu(object):
    def __init__(self,driver,account,passwd):
        self.url = 'https://www.zhihu.com'
        self.driver=driver
        self.account=account
        self.passwd=passwd

    def login(self,):
        self.driver.get(self.url)
        self.driver.find_element_by_link_text(u'登录').click()
        account=self.driver.find_element_by_name('account')
        account.send_keys(self.account)
        passwd=self.driver.find_element_by_name('password')
        passwd.send_keys(self.passwd)
        passwd.send_keys(Keys.ENTER)
        print self.driver.title
        if u'首页' in self.driver.title:
            print 'Login Success!'
        else:
            print 'Login Failure!'

    def get_info(self,):
        time.sleep(1)
        self.driver.get('https://www.zhihu.com/people/yxy2829')
        print self.driver.title
        name=self.driver.title[:-5]
        userAgree=self.driver.find_element_by_class_name('zm-profile-header-user-agree').text
        userThanks=self.driver.find_element_by_class_name('zm-profile-header-user-thanks').text
        followee=self.driver.find_element_by_xpath("//div[contains(@class, 'zm-profile-side-following')]/a[1]").text
        follower=self.driver.find_element_by_xpath("//div[contains(@class, 'zm-profile-side-following')]/a[2]").text
        ask=self.driver.find_element_by_xpath('//div[contains(@class,"profile-navbar")]/a[2]').text
        answer=self.driver.find_element_by_xpath('//div[contains(@class,"profile-navbar")]/a[3]').text
        # title=self.driver.find_element_by_xpath('//div[contains(@class,"profile-navbar")]/a[4]').text
        # collection=self.driver.find_element_by_xpath('//div[contains(@class,"profile-navbar")]/a[5]').text
        # publicEditor=self.driver.find_element_by_xpath('//div[contains(@class,"profile-navbar")]/a[6]').text
        followee_url=self.driver.find_element_by_xpath("//div[contains(@class, 'zm-profile-side-following')]/a[1]").get_attribute('href')
        page_url=self.driver.current_url

        nums=[userAgree,userThanks,followee,follower,ask,answer]
        info=[name,page_url,followee_url]
        num=map(lambda x:re.search(re.compile(r'\d+'),x).group(),nums)
        data=info+num
        print data

    def get_followee_url(self,):
        self.driver.find_element_by_xpath("//div[contains(@class, 'zm-profile-side-following')]/a[1]").click()

    def loadmore(self,):
        # self.driver.get('https://www.zhihu.com/people/yxy2829/followees')
        print self.driver.title
        while True:
            try:
                load=self.driver.find_element_by_xpath('//*[@id="zh-profile-follows-list"]/a[contains(@aria-role, "button")]')
                ActionChains(self.driver).move_to_element(load).perform()
            except:
                break

        all_people=self.driver.find_elements_by_class_name('author-link-line')
        for i in all_people:
            print i.text,i.find_element_by_tag_name('a').get_attribute('href')

    def quit(self,):
        self.driver.quit()

    def run(self,):
        self.login()
        self.get_info()
        self.get_followee_url()
        self.loadmore()
        self.quit()

def main():
    ua=UserAgent()
    dcap=dict(DesiredCapabilities.PHANTOMJS)
    dcap['phantomjs.page.settings.useragent']=ua.random
    zhihu=Zhihu(driver=webdriver.PhantomJS(desired_capabilities=dcap),account='account',passwd='passwd')
    zhihu.run()

if __name__=='__main__':
    main()
