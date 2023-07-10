###################### 엑셀 import ############################
import pandas as pd
import os
###############################################################

###################### 셀레니움 import #########################
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import chromedriver_autoinstaller
import subprocess
import pyautogui
import pyperclip
import time
###############################################################

user_info = []
spreadlink = ""
sheet_name = ""
elements = {'idbox': '//*[@id="loginId"]',
            'pwbox': '//*[@id="password"]',
            'loginbtn': '//*[@id="formLogin"]/div/div[3]/button',
            'syear': '//*[@id="cal-start-year"]',
            'smonth': '//*[@id="cal-start-month"]',
            'sday': '//*[@id="cal-start-day"]',
            'eyear': '//*[@id="cal-end-year"]',
            'emonth': '//*[@id="cal-end-month"]',
            'eday': '//*[@id="cal-end-day"]',
            'option': '/option[',
            'searchbtn': '//*[@id="do-search-period"]',
            'base1': '//*[@id="Contents"]/div[2]/div[2]/table/tbody[',
            'base2': ']/tr[',
            'td': ']/td[',
            'itemname': ']/div/div/a/span[2]',
            'strong': ']/strong',
            'logout': '//*[@id="menu_list_header"]/li[1]/a',
            'login/mypage': '//*[@id="menu_list_header"]/li[2]/a',
            'orderlookup': '//*[@id="Contents"]/div[2]/div[1]/ul/li[1]/ul[1]/li[1]/a',
            'paging': '//*[@id="Contents"]/div[2]/div[2]/div[3]',
            }

# 요소 찾기 함수


def find_element(xpath):
    wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    return driver.find_element(By.XPATH, xpath)

# 요소 child 개수 함수


def find_elements(parents, tag):
    return parents.find_elements(By.TAG_NAME, tag)


# 아이디 비밀번호 읽어오기 함수
def read_info():
    global f_name, sheet_name
    cnt = 0
    with open("login_info.txt", "r", encoding='UTF8') as f:
        for line in f:
            cnt += 1
            if cnt == 2:
                f_name = line.strip().replace("- 스프레드시트 이름 : ", "")
            if cnt >= 11:
                if cnt % 2 != 0:
                    user_info.append(line.strip().replace("ID : ", ""))
                else:
                    user_info.append(line.strip().replace("PW : ", ""))


# 데이터프레임 열기
read_info()
columns = ['주문일자', '주문아이디', '상품명', '수량', '주문금액', '상태']
df = pd.DataFrame(columns=columns)


# 검색 날짜 입력받기
sdate = input("검색할 시작 날짜를 입력해주세요(ex: 22-04-12) : ")
edate = input("검색할 종료 날짜를 입력해주세요(ex: 22-04-12) : ")
slst = sdate.split("-")
elst = edate.split("-")
syear = str(int(slst[0])-11)
smonth = slst[1]
sday = slst[2]
eyear = str(int(elst[0])-11)
emonth = elst[1]
eday = elst[2]

# 셀레니움 실행
error = []
blank = []
error_index = 0
subprocess.Popen(
    r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')  # 디버거 크롬 구동
option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
try:
    driver = webdriver.Chrome(
        f'./{chrome_ver}/chromedriver.exe', options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(
        f'./{chrome_ver}/chromedriver.exe', options=option)
wait = WebDriverWait(driver, 5)
driver.implicitly_wait(1)
driver.maximize_window()
size = driver.get_window_size()
width = size.get("width")
height = size.get("height")
driver.get("https://www.oliveyoung.co.kr/")
driver.implicitly_wait(1)
for i in range(int(len(user_info)/2)):
    find_element(elements['login/mypage']).click()
    driver.implicitly_wait(2)
    pyperclip.copy(user_info[2*i])
    find_element(elements['idbox']).clear()
    find_element(elements['idbox']).send_keys(Keys.CONTROL, 'v')
    pyperclip.copy(user_info[2*i + 1])
    find_element(elements['pwbox']).send_keys(Keys.CONTROL, 'v')
    time.sleep(1)
    find_element(elements['pwbox']).send_keys(Keys.ENTER)
    driver.implicitly_wait(2)
    time.sleep(1)
    pyautogui.press('enter')
    find_element(elements['login/mypage']).click()
    driver.implicitly_wait(2)
    find_element(elements['orderlookup']).click()
    driver.implicitly_wait(2)
    find_element(elements['syear']).click()
    time.sleep(0.3)
    find_element(elements['syear']+elements['option']+syear+']').click()
    find_element(elements['smonth']).click()
    time.sleep(0.3)
    find_element(elements['smonth']+elements['option']+smonth+']').click()
    find_element(elements['smonth']).click()
    time.sleep(0.3)
    find_element(elements['sday']+elements['option']+sday+']').click()
    find_element(elements['sday']).click()
    time.sleep(0.3)
    find_element(elements['eyear']+elements['option']+eyear+']').click()
    find_element(elements['eyear']).click()
    time.sleep(0.3)
    find_element(elements['emonth']+elements['option']+emonth+']').click()
    find_element(elements['emonth']).click()
    time.sleep(0.3)
    find_element(elements['eday']+elements['option']+eday+']').click()
    time.sleep(0.3)
    find_element(elements['eday']).click()
    time.sleep(0.3)
    find_element(elements['searchbtn']).click()
    driver.implicitly_wait(5)
    time.sleep(1)

    first_page = True
    page_end = False
    single_page = False
    stt = 1
    error_code = 0
    page_cnt = 0
    while not page_end:
        try:
            error_code = 1
            if first_page == False:  # 다음페이지로 넘어와서 이전페이지 버튼이 있을경우 시작을 2부터
                stt = 2
            page_p = find_element(elements['paging'])
            p_lst = find_elements(page_p, "a")

            if first_page:
                if len(p_lst) == 0:
                    page_cnt = 1
                    single_page = True
                    page_end = True
                elif len(p_lst) < 10:
                    page_cnt = len(p_lst)
                    page_end = True
                else:
                    page_cnt = len(p_lst)
            else:
                if len(p_lst) == 1:
                    page_cnt = 2
                    single_page = True
                    page_end = True
                elif len(p_lst) < 11:
                    page_cnt = len(p_lst)
                    page_end = True
                else:
                    page_cnt = len(p_lst)

            # 크롤링 코드
            for page in range(stt, page_cnt+1):
                error_code = 2
                parent = find_element(
                    elements['base1'].strip().replace("/tbody[", ""))
                f_lst = find_elements(parent, "tbody")
                cnt1 = len(f_lst)
                for j in range(1, cnt1+1):
                    error_code = 3
                    sub_parent = find_element(elements['base1'] + str(j) + ']')
                    s_lst = find_elements(sub_parent, "tr")
                    cnt2 = len(s_lst)
                    for k in range(1, cnt2+1):
                        error_code = 4
                        row_cnt = 2
                        if k != 1:
                            row_cnt = 1
                        order_date = find_element(
                            elements['base1']+str(j)+elements['base2']+'1'+elements['td']+'1]/ul/li[1]').text
                        if order_date[0] != '2':
                            order_date = find_element(
                                elements['base1']+str(j)+elements['base2']+'1'+elements['td']+'1]/ul/li[2]').text
                        order_id = user_info[2*i]
                        item_name = find_element(
                            elements['base1']+str(j)+elements['base2']+str(k)+elements['td']+str(row_cnt)+elements['itemname']).text
                        item_cnt = find_element(
                            elements['base1']+str(j)+elements['base2']+str(k)+elements['td']+str(row_cnt+1)+']').text
                        item_price = find_element(
                            elements['base1']+str(j)+elements['base2']+str(k)+elements['td']+str(row_cnt+2)+elements['strong']).text
                        item_state = find_element(
                            elements['base1']+str(j)+elements['base2']+str(k)+elements['td']+str(row_cnt+3)+elements['strong']).text
                        error_code = 5
                        info = {'주문일자': [str(order_date)], '주문아이디': [str(order_id)], '상품명': [str(item_name)], '수량': [
                            str(item_cnt)], '주문금액': [str(item_price)], '상태': [str(item_state)]}
                        infodf = pd.DataFrame(info)
                        df = pd.concat([df, infodf], axis=0, ignore_index=True)
                        error_code = 6
                if not single_page:
                    find_element(elements['paging'] +
                                 '/a['+str(page)+']').click()
                if (page_end == True) and (page == page_cnt) and (not single_page):
                    error_code = 2
                    parent = find_element(
                        elements['base1'].strip().replace("/tbody[", ""))
                    f_lst = find_elements(parent, "tbody")
                    cnt1 = len(f_lst)
                    for j in range(1, cnt1+1):
                        error_code = 3
                        sub_parent = find_element(
                            elements['base1'] + str(j) + ']')
                        s_lst = find_elements(sub_parent, "tr")
                        cnt2 = len(s_lst)
                        for k in range(1, cnt2+1):
                            error_code = 4
                            row_cnt = 2
                            if k != 1:
                                row_cnt = 1
                            order_date = find_element(
                                elements['base1']+str(j)+elements['base2']+'1'+elements['td']+'1]/ul/li[1]').text
                            if order_date[0] != '2':
                                order_date = find_element(
                                    elements['base1']+str(j)+elements['base2']+'1'+elements['td']+'1]/ul/li[2]').text
                            order_id = user_info[2*i]
                            item_name = find_element(
                                elements['base1']+str(j)+elements['base2']+str(k)+elements['td']+str(row_cnt)+elements['itemname']).text
                            item_cnt = find_element(
                                elements['base1']+str(j)+elements['base2']+str(k)+elements['td']+str(row_cnt+1)+']').text
                            item_price = find_element(
                                elements['base1']+str(j)+elements['base2']+str(k)+elements['td']+str(row_cnt+2)+elements['strong']).text
                            item_state = find_element(
                                elements['base1']+str(j)+elements['base2']+str(k)+elements['td']+str(row_cnt+3)+elements['strong']).text
                            error_code = 5
                            info = {'주문일자': [str(order_date)], '주문아이디': [str(order_id)], '상품명': [str(item_name)], '수량': [
                                str(item_cnt)], '주문금액': [str(item_price)], '상태': [str(item_state)]}
                            infodf = pd.DataFrame(info)
                            df = pd.concat([df, infodf], axis=0,
                                           ignore_index=True)
                            error_code = 6
            first_page = False

        except:
            print("에러코드 : "+str(error_code))
            break
    find_element(elements['logout']).click()
    driver.implicitly_wait(2)

driver.close()
if not os.path.exists(f_name+".csv"):
    df.to_csv(f_name+".csv", index=False, mode='w', encoding='utf-8-sig')
else:
    df.to_csv(f_name+".csv", index=False, mode='a',
              encoding='utf-8-sig', header=False)
