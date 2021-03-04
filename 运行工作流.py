# -*- coding=utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
import time
import re

chrome_path = './chromedriver'
chrome_options = Options()  # 创建chrome设置
chrome_options.add_argument('--ignore-certificate-errors')  # 无视证书引发的错误
# chrome_options.add_argument('--headless')  # 无窗口模式
driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)  # 配置chrome设置


def find_ele(xpath):
    return driver.find_element_by_xpath(xpath)


def isElementPresent(value):
    try:
        driver.find_element_by_xpath(value)
    except NoSuchElementException as e:
        return False
    else:
        return True


print('正在打开页面...')
idp_url = r'http://10.24.68.238:8044/#/workbench/worker-flow'
driver.get(idp_url)
driver.maximize_window()
time.sleep(2)

# 登入
print('登录中...')
find_ele('//*[@id="app"]/div/form/div[2]/div[1]/div/div/input').send_keys('admin')  # 用户名
find_ele('//*[@id="app"]/div/form/div[2]/div[2]/div/div/input').send_keys('bigtimes2020')  # 密码
find_ele('//*[@id="app"]/div/form/button').click()  # 登录
print('登录成功！')

print('寻找测试用的项目...')
time.sleep(2)
if find_ele('//*[@id="app"]/div/div[1]/div[2]/div/div[1]/a[2]/span').text == 'For_TEST_Case':
    driver.get(idp_url)
    print('已处于测试项目中！')
else:
    find_ele('//*[@id="app"]/div/div[1]/div[2]/div/div[1]/a[2]/span').click()
    time.sleep(1.5)

    # 需要获取所有项目的数量/页数

    pages = find_ele('//*[@id="app"]/div/div[2]/div[2]/section/div/div/div[2]/div/div/div[2]/div/div/div['
                     '2]/div/span[1]').text
    pages_number = re.findall(r"共(.+?)条", pages)[0]
    # print(page_numbers)
    # print(type(page_numbers))

    ##################################################
    #                                                #
    #   没有做翻页的功能，目前仅支持项目在第一页的情况下使用   #
    #                                                #
    ##################################################

    # 遍历找项目
    for i in range(2, int(pages_number) + 1):  # range的右侧设置为项目总数+1
        case_name = find_ele('//*[@id="app"]/div/div[2]/div[2]/section/div/div/div[2]/div/div/div[2]/div/div/div['
                             '1]/div[%s]/div/div[1]/div[1]' % i).text
        # print('项目名称：', case_name)
        if case_name == 'For_TEST_Case':
            # print('已找到测试用项目！')
            find_ele('//*[@id="app"]/div/div[2]/div[2]/section/div/div/div[2]/div/div/div[2]/div/div/div[1]/div[%s]/div'
                     % i).click()
            print('已进入测试项目中！')
            del i
            break
        else:
            continue

# 运行工作流

# 改变一页内显示的节点数
print('正在拉取所有节点...')
# 改变页面高度位置——到最底下
time.sleep(1)
execute_js = "document.getElementsByClassName('outer-card')[0].scrollTop = 100000"
driver.execute_script(execute_js)

time.sleep(0.5)
find_ele('//*[@id="app"]/div/div[2]/div[2]/section/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/span[2]/div/div[1]/'
         'input').click()
time.sleep(2)
find_ele('/html/body/div[3]/div[1]/div[1]/ul/li[5]/span').click()

# 获取节点数量
print('正在获取节点数量...')
time.sleep(1)
pages = find_ele('//*[@id="app"]/div/div[2]/div[2]/section/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/'
                 'span[1]').text
pages_number = re.findall(r"共(.+?)条", pages)[0]
print('共%s个节点' % int(pages_number))

# 改变页面高度位置——回到最顶上
execute_js = "document.getElementsByClassName('outer-card')[0].scrollTop = 0"
driver.execute_script(execute_js)

# 依次运行所有节点
for i in range(2, (int(pages_number) + 2)):
    print('正在启动第%s个节点...' % (i - 1))
    time.sleep(1)
    """
    
    ##################
    #  svg xpath路径  #
    ##################
    '//*[@id="app"]/div/div[2]/div[2]/section/div/div/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[3]/div/div/svg[1]'
    '//*[@id="app"]/div/div[2]/div[2]/section/div/div/div[2]/div/div/div[2]/div/div/div[1]/div[3]/div/div[3]/div/div/svg[1]'
    
    改写方式
    svgelementXpath = "//div[12]/*[name()='svg']/*[name()='g']/*[name()='g'][2]/*[name()='g'][1]/*[name()='image']"

    ####################
    #  svg 改写后的路径  #
    ####################
    '//*[@id="app"]/div/div[2]/div[2]/section/div/div/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[3]/div/div/*[name()="svg"][1]'

    """
    svg_path = '//*[@id="app"]/div/div[2]/div[2]/section/div/div/div[2]/div/div/div[2]/div/div/div[1]/div[%s]/div' \
               '/div[3]/div/div/*[name()="svg"][1]' % i
    start_svg = driver.find_element_by_xpath(svg_path)
    action = ActionChains(driver)
    action.click(start_svg).perform()

    time.sleep(1)
    find_ele('//*[@id="app"]/div/div[2]/div[2]/section/div/div/div[3]/div/div/div[2]/div/form/div[10]'
             '/button[2]').click()
    time.sleep(1)

print('所有节点均已启动！')
# driver.close()
