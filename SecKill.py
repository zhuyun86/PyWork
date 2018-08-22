from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
 
if __name__ == '__main__':
    browser = webdriver.Chrome()
    url = 'https://www.jd.com'
    # url = r'http://spf.szfcweb.com/szfcweb/(S(qsdnn055bmgiuquegmrfli55))/DataSerach/SaleInfoProListIndex.aspx'
    browser.get(url)

    login_btn = browser.find_element_by_class_name('link-login')
    login_btn.click()

    browser.find_element_by_link_text('账户登录').click()

    browser.find_element_by_id('loginname').send_keys('rogbiv')
    browser.find_element_by_id('nloginpwd').send_keys('zap.1219')
    time.sleep(1)
    # browser.find_element_by_class_name('authcode-btn').click()
    # browser.find_element_by_id('loginsubmit').click()
    
    try:
        wait = WebDriverWait(browser, 60)
        wait.until(EC.presence_of_element_located((By.LINK_TEXT,'秒杀')))
    except BaseException as e:
        print('*'*5, e)

    browser.find_element_by_link_text('秒杀').click()
    
    browser.switch_to_window(browser.window_handles[1])

    lt = browser.find_elements_by_class_name('timeline_item_link_skew_time')
    print('time:',len(lt))
    for item in lt:
        print(item.text)
        time.sleep(0.1)
        # ele = EC.element_to_be_clickable((By.LINK_TEXT, item.text))
        # if not ele:
        #     continue
        try:
            item.click()
        except BaseException as e:
            print(e)
        # if item.text == '16:00':
        #     item.click()
        #     break
        browser.execute_script('window.scrollTo(0,99999)')
        time.sleep(1)

        lt = browser.find_elements_by_class_name('seckill_mod_goods ')
        for item in lt:
            title = item.find_element_by_class_name('seckill_mod_goods_title')
            price = item.find_element_by_class_name('seckill_mod_goods_price_now')
            if re.search('酒', title.text):
                print(price.text, title.text)
                item.click()

    # time.sleep(3)
    # browser.switch_to_window(browser.window_handles[2])
    # browser.find_element_by_id('btn-onkeybuy').click()
    # time.sleep(1)
    # browser.find_element_by_id('order-submit').click()
    
    # browser.find_element_by_id('ctl00_MainContent_txt_Pro').send_keys(r'万象汇')
    # browser.find_element_by_name('ctl00$MainContent$ddl_RD_CODE').send_keys(r'吴江')
    # # browser.find_element_by_id('ctl00_MainContent_txt_Com').send_keys(r'华润')
    
    # btn = browser.find_element_by_id('ctl00_MainContent_bt_select')
    # print(btn.get_attribute('type'))
    # btn.click()

    # browser.execute_script('window.open()')
    # print(browser.window_handles)
    # browser.switch_to_window(browser.window_handles[1])
    # browser.get('http://www.baidu.com')
    # browser.switch_to_window(browser.window_handles[0])
    # browser.execute_script('window.close()')

    # table = browser.find_element_by_id('ctl00_MainContent_OraclePager1')
    # tds = table.find_elements_by_tag_name('td')
    # for t in tds:
    #     print(t.text,t.get_attribute('onmouseover'))
    # # tds[0].click()

    # table = browser.find_element_by_id('ctl00_MainContent_OraclePager1')
    # tds = table.find_elements_by_tag_name('td')
    # print('*'*20,tds)
    # for t in tds:
    #     print(t.text) 
    # print(tds[0].get_attribute('href'))
    # tds[0].click()


    # browser.implicitly_wait(10)
    # time.sleep(5)
    # browser.back()
    # print(btn.tag_name)

    # print(browser.page_source)
    # print(browser.current_url)
    # print(browser.get_cookies())