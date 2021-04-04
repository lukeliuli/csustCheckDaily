#长沙理工大学汽机学院
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import string,random,time,sys,os
from selenium.webdriver.support.ui import WebDriverWait

import os
#############################################################################
#打开网页并输入用户名和密码登录1
def openBrowser(browser,url1,logTimes):

    loginCounter = 0
    isOpenAndLog = False
    retryCounter = 0
    
    while loginCounter < logTimes and isOpenAndLog == False:
        print("opening Brower and logging\n")
        loginCounter = loginCounter+1
        try:
            browser.get(url1)
        except:
            browser.execute_script('window.stop()')
            print("Error:cannot loading url\n")
        
            
            
            
            

        #browser.execute_script('window.stop()')
       
        retryCounter = 0
        while retryCounter < 2 and isOpenAndLog == False:  # Trying finding username input 10 times
            try:
                print("username and password\n")
                username_input = browser.find_element_by_xpath("//input[@name='username']")
                password_input = browser.find_element_by_xpath("//input[@name='password']")
                username_input.send_keys("006683")  # 打卡账户
                password_input.send_keys("280511")  # 密码
                print("username and password2\n")
                browser.find_element_by_xpath("//button[@type='submit']").click()
                print("username and password3\n")
               
               
            except:
                retryCounter = retryCounter + 1
                print("Trying finding username input \n")
            finally:
                    if 'OA系统' in browser.page_source:
                        time.sleep(2)
                        isOpenAndLog = True
                
            
       
    return loginCounter, retryCounter, isOpenAndLog

######################################################################    
#登录成功后打开疫情打卡的页

def enterCovidCheck(browser, url2,enterTimes):

    isCovidChecked = False 
    retry = 0
    while retry < enterTimes and isCovidChecked == False:
        print("entering\n")
        retry = retry+1

        try:
            browser.get(url2)
        except:
            #browser.execute_script('window.stop()')
            time.sleep(2)

        if browser.title.find('系统异常') > -1:
            time.sleep(2)

        if browser.title.find('特殊时期信息收集') > -1:
            time.sleep(2)
            isCovidChecked = True
            
    return isCovidChecked, retry

######################################################################
#进入疫情打卡页后，填写相关内容


def addingAndFilling(browser, loopTimes):

    loop = 0
    rescode = 0
    isAddingAndFilling = False
    retry = 0

    while loop < loopTimes and isAddingAndFilling == False:
        print("adding and filling\n")
        loop = loop+1
        #增加打卡
        browser.find_element_by_xpath("//div[@data-action='add']").click()
        if "新建" in browser.page_source:
            retry = 0
            #基本信息页面出来很忙
            while '基本信息' not in browser.page_source:
                retry = retry+1
                time.sleep(2)
                if retry > 150:
                    print("waiting the filling pages\n")
                    break
            time.sleep(2)
            browser.execute_script('window.stop()')
            ####################
            ##在基本信息页面填写
            try:
                #值班
                sel2 = browser.find_element_by_xpath(
                    "//div[@data-caption='当日是否在校值班']")
                sel2.click()
                xpath = "//div[@class='jqx-listbox jqx-reset jqx-rc-all jqx-widget jqx-widget-content jqx-disableselect jqx-popup jqx-rc-t-expanded jqx-fill-state-focus']/div/div/div[2]/div/div[3]/span"
                browser.find_element_by_xpath(xpath).click()
                time.sleep(1)
                #省
                sel3 = browser.find_element_by_xpath(
                    "//div[contains(@data-caption, '当前所在地省份')]")
                sel3.click()
                ii = 0
                while ii < 19:
                    time.sleep(0.5)
                    sel3.send_keys(Keys.DOWN)
                    ii = ii+1
                sel3.send_keys(Keys.ENTER)
                time.sleep(1)
                #市
                sel4 = browser.find_element_by_xpath(
                    "//div[@data-caption='当前所在地城市']")
                sel4.click()
                ii = 0
                while ii < 2:
                    time.sleep(0.5)
                    sel4.send_keys(Keys.DOWN)
                    ii = ii+1
                sel4.send_keys(Keys.ENTER)
                time.sleep(1)
                #区
                sel5 = browser.find_element_by_xpath(
                    "//div[@data-caption='当前所在地区县']")
                sel5.click()
                ii = 0
                while ii < 4:
                    time.sleep(0.5)
                    sel5.send_keys(Keys.DOWN)
                    ii = ii+1
                sel5.send_keys(Keys.ENTER)
                time.sleep(1)
                #风险区
                sel6 = browser.find_element_by_xpath(
                    "//div[@data-caption='21天内是否到过中高风险区']")
                   #browser.execute_script("arguments[0].click();", sel6)
                browser.execute_script(
                    "arguments[0].scrollIntoView();", sel6)
                time.sleep(1)
                sel6.click()
                xpath = "//div[@class='jqx-listbox jqx-reset jqx-rc-all jqx-widget jqx-widget-content jqx-disableselect jqx-popup jqx-rc-t-expanded jqx-fill-state-focus']/div/div/div[2]/div/div[3]/span"
                browser.find_element_by_xpath(xpath).click()
                time.sleep(1)
               #提交
                browser.find_element_by_xpath(
                    "//div[@data-action='save']").click()
                browser.find_element_by_xpath("//a[text()='确认']").click()
                time.sleep(1)
            except:  # 在基本信息页面填写出现错误

                try:
                    browser.get(url2)
                except:
                    browser.execute_script('window.stop()')
                msgtxt = "打卡失败1！在基本信息页面填写错误"
                print(msgtxt)
                rescode = 1
        else:  # 等待"新建"不成功
            time.sleep(1)
            try:
                prompt = browser.find_element_by_xpath(
                    '//div[@class="bh-dialog-content"]/div')
                if prompt.text == "今日已填报！":
                    browser.find_element_by_xpath(
                        '//div[@class="bh-dialog-btnContainerBox"]/a').click()
                    msgtxt = "打卡成功！因为今日已填报"
                    print(msgtxt)
                    isAddingAndFilling = True
                    break

            except:
                #等待新建不成功，有不知道原因，再来一次   
                try:
                    browser.get(url2)
                except:
                    browser.execute_script('window.stop()')
                msgtxt = "打卡失败3！等待新建不成功，有不知道原因，再来一次进入疫情疫情打卡的页"
                print(msgtxt)
                rescode = 3
    
    return isAddingAndFilling, retry

 


if __name__=='__main__':
#    logfile=os.getcwd()+'\\'+time.strftime("%Y-%m-%d", time.localtime())+'.log'
  
    for num in range(1, 10):#运行9次
        
        path1=os.getcwd()

        flog = open(path1 + '\\rvls.txt', 'a+')
        nowday = time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime())
        flog.write(nowday)
        
        url1 = "http://ehall.csust.edu.cn/"
        url2="http://ehall.csust.edu.cn/qljfwapp/sys/lwReportEpidemic/index.do"
        
        chrome_options=webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')   # 浏览器不提供可视化页面
        chrome_options.add_argument('--disable-gpu')    # 谷歌文档提到需要加上这个属性来规避bug
        driver_url=path1+'\\chromedriver.exe'
        browser = webdriver.Chrome(executable_path=driver_url,options=chrome_options)  
        browser.implicitly_wait(20)
        browser.set_page_load_timeout(20)
        browser.set_script_timeout(20)
        
        ########################################################################
        #进入ehall，并输入用户名密码登录
        loginCounters, retryCounter,  isOpenAndLog= openBrowser(browser, url1, 50)

            
        if isOpenAndLog == False:
            print("Fail:OpenAndLog\n")
            flog.write("Fail:OpenAndLog\n")
            browser.quit()
            #sys.exit(1)

        ######################################################################    
        #登录成功后打开疫情打卡的页             
        isCovidChecked, retry = enterCovidCheck(browser, url2, 200)
        if isCovidChecked == False:
            print("Fail:enterCovidCheck\n")
            flog.write("Fail:enterCovidCheck\n")
            browser.quit()
            #sys.exit(1)
        
        ######################################################################
        #进入疫情打卡的页后，进行填写
        isAddingAndFilling, retry = addingAndFilling(browser, 4)
        
        if isAddingAndFilling == False:
            print("Fail:addingAndFilling\n")
            browser.quit()
            flog.write("Fail:addingAndFilling\n")
        

        if isAddingAndFilling == True:
            print("打卡成功\n")
            browser.quit()
            flog.write("打卡成功\n")
        
            
        flog.close()
        browser.quit()
        time.sleep(2)
        browser.quit()
        #sys.exit(1)
        

    

    
       
