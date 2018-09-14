from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import re


class CSecKill():
    def __init__(self):
        self.browser = webdriver.Chrome()

    def Login(self, url, username, password):
        self.browser.switch_to_window(self.browser.window_handles[0])
        self.browser.get(url)
        self.browser.maximize_window()
        self.browser.implicitly_wait(10)

        login_btn = self.browser.find_element(By.CLASS_NAME, 'link-login')
        login_btn.click()
        self.browser.implicitly_wait(10)
        self.browser.find_element(
            By.XPATH,
            ".//*[@clstag='pageclick|keycount|login_pc_201804112|10']").click(
            )
        self.browser.find_element_by_id('loginname').send_keys(username)
        self.browser.find_element_by_id('nloginpwd').send_keys(password)
        print(username, password)
        self.browser.implicitly_wait(10)

    def SearchGoods(self, goods_name, urls):
        if len(self.browser.window_handles) < 2:
            self.browser.execute_script('window.open()')
        self.browser.switch_to_window(self.browser.window_handles[1])
        self.browser.get('https://miaosha.jd.com/')

        lt = self.browser.find_elements_by_class_name(
            'timeline_item_link_skew_time')
        print('timespan:', len(lt))
        for item_time in lt:
            print(item_time.text)
            self.browser.implicitly_wait(2)
            try:
                item_time.click()
            except BaseException as e:
                print(e)
            # if item_time.text == '16:00':
            #     item_time.click()
            #     break

            time.sleep(1)
            lt = self.browser.find_elements_by_class_name('seckill_mod_goods')
            for item in lt:
                title = item.find_element(By.CLASS_NAME,
                                          'seckill_mod_goods_title')
                price = item.find_element(By.CLASS_NAME,
                                          'seckill_mod_goods_price_now')
                href = item.find_element(
                    By.CLASS_NAME,
                    'seckill_mod_goods_info_i').get_attribute('href')
                if re.search(goods_name, title.text):
                    urls.append((item_time.text, price.text, title.text, href))
                    # item.click()

    def KillGoods(self, url, start_time):
        while len(self.browser.window_handles) < 3:
            self.browser.execute_script('window.open()')
        self.browser.switch_to_window(self.browser.window_handles[2])
        self.browser.get(url)

        now_time = datetime.now()
        now_y = now_time.year
        now_m = now_time.month
        now_d = now_time.day
        parts = re.findall(r'(\D*?)(\d+):(\d+)', start_time)
        if len(parts[0]) != 3:
            return

        kill_time = datetime(now_y, now_m, (now_d + 1
                                            if parts[0][0] else now_d),
                             int(parts[0][1]), int(parts[0][2]))

        # if now_time < kill_time:
        price_old = 0
        while now_time < kill_time:
            now_time = datetime.now()
            delta_time = kill_time - now_time
            print(delta_time)

            self.browser.refresh()
            p_price = self.browser.find_element_by_class_name('p-price')
            price_new = float(re.findall(r'\d+.\d+', p_price.text)[0])
            print(price_new)
            if not price_old:
                price_old = price_new
            if price_new < price_old:
                break
            price_old = price_new
        
        self.browser.implicitly_wait(1)
        btn_onkeybuy = self.browser.find_element_by_id('btn-onkeybuy')
        btn_onkeybuy.click()

        self.browser.implicitly_wait(1)
        btn_submit = self.browser.find_element_by_id('order-submit')
        btn_submit.click()


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
    browser.find_element(
        By.XPATH,
        ".//*[@clstag='pageclick|keycount|login_pc_201804112|10']").click()

    browser.find_element_by_id('loginname').send_keys('rogbiv')
    browser.find_element_by_id('nloginpwd').send_keys('zap.1219')

    browser.implicitly_wait(10)

    wait = WebDriverWait(browser, 60)
    # wait.until(EC.visibility_of_element_located((By.LINK_TEXT,'秒杀')))
    wait.until(
        EC.visibility_of_element_located((By.XPATH,
                                          ".//*[@href='//miaosha.jd.com/']")))

    # browser.find_element_by_link_text('秒杀').click()
    # browser.find_element_by_xpath(".//*[@href='//miaosha.jd.com/']").click()
    browser.find_element(By.XPATH, ".//*[@href='//miaosha.jd.com/']").click()

    browser.switch_to_window(browser.window_handles[1])

    urls = []
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
            price = item.find_element(By.CLASS_NAME,
                                      'seckill_mod_goods_price_now')
            href = item.find_element(
                By.CLASS_NAME,
                'seckill_mod_goods_info_i').get_attribute('href')
            if re.search('玩具', title.text):
                print(price.text, title.text, href)
                urls.append(href)
                # item.click()

    for u in urls:
        browser.execute_script('window.open()')
        browser.switch_to_window(browser.window_handles[-1])
        browser.get(u)