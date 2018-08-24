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
    browser.maximize_window()
    browser.implicitly_wait(10)

    login_btn = browser.find_element(By.CLASS_NAME, 'link-login')
    login_btn.click()

    # browser.find_element_by_link_text('账户登录').click()
    browser.find_element(By.XPATH, ".//*[@clstag='pageclick|keycount|login_pc_201804112|10']").click()

    browser.find_element_by_id('loginname').send_keys('rogbiv')
    browser.find_element_by_id('nloginpwd').send_keys('zap.1219')
    
    browser.implicitly_wait(10)

    wait = WebDriverWait(browser, 60)
    # wait.until(EC.visibility_of_element_located((By.LINK_TEXT,'秒杀')))
    wait.until(EC.visibility_of_element_located((By.XPATH, ".//*[@href='//miaosha.jd.com/']")))

    # browser.find_element_by_link_text('秒杀').click()
    # browser.find_element_by_xpath(".//*[@href='//miaosha.jd.com/']").click()
    browser.find_element(By.XPATH, ".//*[@href='//miaosha.jd.com/']").click()
    
    browser.switch_to_window(browser.window_handles[1])

    lt = browser.find_elements_by_class_name('timeline_item_link_skew_time')
    print('timespan:', len(lt))
    for item in lt:
        print(item.text)
        browser.implicitly_wait(2)
        try:
            item.click()
        except BaseException as e:
            print(e)
        # if item.text == '16:00':
        #     item.click()
        #     break

        time.sleep(1)
        lt = browser.find_elements_by_class_name('seckill_mod_goods')
        for item in lt:
            title = item.find_element(By.CLASS_NAME, 'seckill_mod_goods_title')
            price = item.find_element(By.CLASS_NAME, 'seckill_mod_goods_price_now')
            href = item.find_element(By.CLASS_NAME, 'seckill_mod_goods_info_i').get_attribute('href')
            if re.search('玩具', title.text):
                print(price.text, title.text, href)
                # item.click()

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