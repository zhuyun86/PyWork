from selenium import webdriver
import time
 
if __name__ == '__main__':
    browser = webdriver.Chrome(r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe')
    url = r'http://spf.szfcweb.com/szfcweb/(S(qsdnn055bmgiuquegmrfli55))/DataSerach/SaleInfoProListIndex.aspx'
    browser.get(url)

    lbl = browser.find_element_by_id('ctl00_MainContent_txt_Pro')

    browser.find_element_by_id('ctl00_MainContent_txt_Pro').send_keys(r'万象汇')
    browser.find_element_by_name('ctl00$MainContent$ddl_RD_CODE').send_keys(r'吴江')
    # browser.find_element_by_id('ctl00_MainContent_txt_Com').send_keys(r'华润')
    
    btn = browser.find_element_by_id('ctl00_MainContent_bt_select')
    print(btn.get_attribute('type')) 
    btn.click()

    table = browser.find_element_by_id('ctl00_MainContent_OraclePager1')
    tds = table.find_elements_by_tag_name('td')
    for t in tds:
        print(t.text,t.get_attribute('onmouseover'))
    # tds[0].click()

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