# -*- coding: utf-8 -*-

from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
import time
from random import choice
import re
import os

# 这里需要先下载chromedriver 直接新建webdriver.Chrome()对象会报错
chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
browser =  webdriver.Chrome(chromedriver)
# browser = webdriver.Chrome() # 打开谷歌浏览器
wait = ui.WebDriverWait(browser,10) #检测元素是否存在

browser.get("http://s.weibo.com/")

page = 0

## 登录函数，需要输入自己的微博账号登录
def login(username,password):
    wait.until(lambda browser: browser.find_element_by_xpath("//a[@node-type='loginBtn']"))
    browser.find_element_by_xpath("//a[@node-type='loginBtn']").click()

    wait.until(lambda browser: browser.find_element_by_xpath("//input[@name='username']"))
    user = browser.find_element_by_xpath("//input[@name='username']")
    user.clear()
    user.send_keys(username)
    psw = browser.find_element_by_xpath("//input[@name='password']")
    psw.clear()
    psw.send_keys(password)
    browser.find_element_by_xpath("//a[@node-type='submitBtn']").click()

## 登陆完成，若出现用户名，则开始进行搜索
def search(searchWord):
    wait.until(lambda browser: browser.find_element_by_class_name("gn_name"))

    inputBtn = browser.find_element_by_class_name("searchInp_form")
    inputBtn.clear()
    inputBtn.send_keys(searchWord.strip().decode("gbk"))
    browser.find_element_by_class_name('searchBtn').click()

def save2txt(lines,name):
    if not os.path.exists('data'):
        os.mkdir("data")
    filename = "data/"+name+".txt"
    f = open(filename, 'a')
    try:
        f.writelines(lines.encode('utf8'))
    finally:
        f.close()

## 获取每页的博文   
def gettext():
    content =[]
    # 处理需要输入验证码的时候
    try:
        browser.find_element_by_xpath("//input[@node-type='yzm_input']")
        flag = True
    except:
        flag = False
    if flag:
        print "Now pause at "+ str(page) +"page"
        raw_input("Press Enter to continue...")
        print "Continue..."

    wait.until(lambda browser: browser.find_element_by_class_name("W_pages"))
    texts = browser.find_elements_by_xpath("//p[@class='comment_txt']")
    # print len(texts)
    for n in texts: # 处理表情图片
        try:
            highpoints = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
		highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        mytext =  highpoints.sub(u'', n.text)
        # print mytext.encode('gbk','ignore') # 输出抓取的每一条
        content.append(mytext)
    return '\n'.join(content)

def nextPage():
    if browser.find_elements_by_xpath("//div[@class='W_pages']") != None:
        pg = browser.find_element_by_xpath("//div[@class='W_pages']/a[last()]") #获取下一页btn
        # print pg
        y = pg.location['y']+100 # 获取下一页btn元素y轴位置
        # print y
        browser.execute_script('window.scrollTo(0, {0})'.format(y))  #滑动至该元素位置，不然你会发现无法点击
        # 这里不能直接点击，需要先执行鼠标移入动作再点击      
        ActionChains(browser).move_to_element(pg).click(pg).perform()

def main():
    t0 = time.time()
    username = "your email"
    password = "your password"
    keyword = u"周杰伦直播lol".encode("gbk")

    login(username,password)
    search(keyword)
    for i in range(0,50): #控制抓取页数
        page = i+1
        text = gettext()
        save2txt(text, keyword) #存为txt
        time.sleep(choice([1,2,3,4,5])) # 防止被ban
        nextPage()
    # browser.quit()
    print "Finished in %.2fs" %(time.time()-t0)

main()