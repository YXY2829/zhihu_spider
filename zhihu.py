#coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent
import time
import re
import peewee
from peewee import *

class People_info(peewee.Model):
    name = peewee.CharField(20)
    page_url = peewee.CharField(128)
    followee_url = peewee.CharField(128)
    userAgree = peewee.IntegerField(8)
    userThanks = peewee.IntegerField(8)
    followee = peewee.IntegerField(8)
    follower = peewee.IntegerField(8)
    ask = peewee.IntegerField(8)
    answer = peewee.IntegerField(8)

    class Meta:
        database = MySQLDatabase('zhihu',user='root',passwd='rootroot')


class Followee(peewee.Model):
    name = peewee.CharField(20)
    page_url = peewee.CharField(128)

    class Meta:
        database = MySQLDatabase('zhihu',user='root',passwd='rootroot')


class Zhihu(object):
    def __init__(self,driver,account,passwd):
        self.url = 'https://www.zhihu.com'
        self.driver = driver
        self.account = account
        self.passwd = passwd

    def login(self,):
        self.driver.get(self.url)
        self.driver.find_element_by_link_text(u'登录').click()
        account = self.driver.find_element_by_name('account')
        account.send_keys(self.account)
        passwd = self.driver.find_element_by_name('password')
        passwd.send_keys(self.passwd)
        time.sleep(20)
        passwd.send_keys(Keys.ENTER)
        print self.driver.title


    def get_info(self,):
        time.sleep(1)
        self.driver.get('https://www.zhihu.com/people/yxy2829/followees')
        print self.driver.title
        name = self.driver.title[:-11]
        userAgree = self.driver.find_element_by_class_name('zm-profile-header-user-agree').text
        userThanks = self.driver.find_element_by_class_name('zm-profile-header-user-thanks').text
        followee = self.driver.find_element_by_xpath("//div[contains(@class, 'zm-profile-side-following')]/a[1]").text
        follower = self.driver.find_element_by_xpath("//div[contains(@class, 'zm-profile-side-following')]/a[2]").text
        ask = self.driver.find_element_by_xpath('//div[contains(@class,"profile-navbar")]/a[2]').text
        answer = self.driver.find_element_by_xpath('//div[contains(@class,"profile-navbar")]/a[3]').text
        # title=self.driver.find_element_by_xpath('//div[contains(@class,"profile-navbar")]/a[4]').text
        # collection=self.driver.find_element_by_xpath('//div[contains(@class,"profile-navbar")]/a[5]').text
        # publicEditor=self.driver.find_element_by_xpath('//div[contains(@class,"profile-navbar")]/a[6]').text
        followee_url = self.driver.find_element_by_xpath("//div[contains(@class, 'zm-profile-side-following')]/a[1]").get_attribute('href')
        page_url = self.driver.current_url

        nums = [userAgree, userThanks, followee, follower, ask, answer]
        info = [name, page_url, followee_url]
        num = map(lambda x: re.search(re.compile(r'\d+'), x).group(), nums)
        data = info + num
        print data
        return data

    def loadmore(self,):
        # self.driver.find_element_by_xpath("//div[contains(@class, 'zm-profile-side-following')]/a[1]").click()
        # self.driver.get('https://www.zhihu.com/people/yxy2829/followees')
        time.sleep(1)
        print self.driver.title
        while True:
            try:
                load=self.driver.find_element_by_xpath('//*[@id="zh-profile-follows-list"]/a[contains(@aria-role, "button")]')
                ActionChains(self.driver).move_to_element(load).perform()
                print '-----loading------'
            except:
                break

    def add_followee(self):
        all_people = self.driver.find_elements_by_class_name('author-link-line')
        for i in all_people:
            print i.text,i.find_element_by_tag_name('a').get_attribute('href')
            followee=Followee(name=i.text,page_url=i.find_element_by_tag_name('a').get_attribute('href'))
            followee.save()

    def quit(self,):
        self.driver.quit()

    def run(self,):
        self.login()
        People_info.create_table()
        Followee.create_table()
        info=self.get_info()
        people=People_info(name=info[0], page_url=info[1], followee_url=info[2],userAgree=info[3], userThanks=info[4], followee=info[5], follower=info[6], ask=info[7], answer=info[8])
        people.save()
        self.loadmore()
        self.add_followee()
        self.quit()

def main():
    ua = UserAgent()
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap['phantomjs.page.settings.useragent'] = ua.random
    zhihu = Zhihu(driver = webdriver.PhantomJS(desired_capabilities = dcap), account = 'account', passwd = 'passwd')
    # zhihu=Zhihu(driver=webdriver.Chrome(), account = 'account', passwd = 'passwd')
    zhihu.run()

if __name__ == '__main__':
    main()
