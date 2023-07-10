from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
input_boxes = {'std_id': '//*[@id="stdno"]',
               'id': '//*[@id="userId"]',
               'pass': '//*[@id="pssrd"]'}
buttons = {'login': '//*[@id="btn_login"]',
           'end': '//*[@id="header"]/div[1]/div/div/div/ul/li[4]/a',
           'tab': '//*[@id="tabs2"]',
           'test': '//*[@id="lectPackReqGrid_0"]/td[11]/a'}


def find_element(xpath):
    wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    return driver.find_element(By.XPATH, xpath)


def login(boxes):
    std_id_box = find_element(boxes['std_id'])
    std_id_box.send_keys('std_no')
    id_box = find_element(boxes['id'])
    id_box.send_keys('id')
    pass_box = find_element(boxes['pass'])
    pass_box.send_keys('password')
    login_btn = find_element(buttons['login'])
    login_btn.click()
    driver.implicitly_wait(time_to_wait=10)
    print('Complete Login!')


def find_subject(num, code):
    for i in range(num):
        codenum = '//*[@id="grid01"]/tr[{}]/td[3]'.format(i+1)
        if find_element(codenum).text == code:
            return i+1
    return 0

# code = 신청 교과목 코드
# sub_num = 수꾸 담긴 과목 수
# find_subject(x,y) : x = 수꾸 전체 과목 수(반복횟수) , y = 신청교과목 코드
# major / mj_name = 신청 교과목 이름
# total_possible / total = 신청과목 제한인원
# limit_std / past_std = 신청과목 수강인원
# past = 현재 수강신청 완료된 과목 수


start = time.time()
code = 'sub_no'
# input('교과목코드 입력(분반x/수강꾸러미에 있어야함) : ').upper()
driver = webdriver.Chrome(ChromeDriverManager().install())
wait = WebDriverWait(driver, 10)
url = 'https://sugang.knu.ac.kr/'
driver.get(url)
alert = Alert(driver)
driver.implicitly_wait(time_to_wait=10)
driver.maximize_window()
login(input_boxes)
find_element(buttons['tab']).click()
time.sleep(0.3)
sub_num = '//*[@id="grid01cnt"]'
sub_num = int(find_element(sub_num).text.rstrip("건"))
print("교과목 인덱스 설정")
if find_subject(sub_num, code) != 0:
    row = find_subject(sub_num, code)
    print("해당 교과목을 찾았습니다.")
else:
    print("해당 교과목을 찾을 수 없습니다.")
    driver.close()
major = '//*[@id="grid01"]/tr[{}]/td[4]'.format(row)
total_possible = '//*[@id="grid01"]/tr[{}]/td[11]'.format(row)
limit_std = '//*[@id="grid01"]/tr[{}]/td[12]'.format(row)

mj_name = find_element(major).text
total = find_element(total_possible).text
past = find_element('//*[@id="grid03cnt"]').text.rstrip("건")
past_std = find_element(limit_std).text
print(past+"건 신청 완료")
while 1:
    if time.time() - start >= 1000:
        driver.refresh()
        driver.implicitly_wait(time_to_wait=10)
        time.sleep(0.2)
        find_element(buttons['tab']).click()
        print("Refresh")
        start = time.time()
        time.sleep(0.3)
    staleElement = True
    while(staleElement):
        try:
            std = find_element(limit_std).text
            staleElement = False
        except StaleElementReferenceException:
            staleElement = True
        except ElementClickInterceptedException:
            staleElement = True
    print('target :', mj_name, std, '/', total,
          (int(time.time() - start)), 'sec...\t', end='\r')
    if int(std) < int(total):
        row = find_subject(sub_num, code)
        buttons['submit'] = '//*[@id="grid01"]/tr[{}]/td[2]/a'.format(row)
        print('Empty 1')
        submit = find_element(buttons['submit'])
        submit.click()
        time.sleep(0.1)
        alert.accept()
        time.sleep(1)
        alert.accept()
        time.sleep(0.3)
        now = find_element('//*[@id="grid03cnt"]').text.rstrip("건")
        find_element(buttons['tab']).click()
        if int(past) != int(now):
            end = find_element(buttons['end'])
            end.click()
            driver.implicitly_wait(time_to_wait=10)
            break
    elif int(std) != int(past_std):
        print("\n교과목 인덱스 재설정\n")
        if find_subject(sub_num, code) != 0:
            row = find_subject(sub_num, code)
        else:
            print("해당 교과목을 찾을 수 없습니다.")
            driver.close()
        major = '//*[@id="grid01"]/tr[{}]/td[4]'.format(row)
        total_possible = '//*[@id="grid01"]/tr[{}]/td[11]'.format(row)
        limit_std = '//*[@id="grid01"]/tr[{}]/td[12]'.format(row)
        buttons['submit'] = '//*[@id="grid01"]/tr[1]/td[2]/a'.format(row)
        find_element(buttons['tab']).click()
    else:
        staleElement = True
        while(staleElement):
            try:
                find_element(buttons['tab']).click()
                staleElement = False
            except StaleElementReferenceException:
                staleElement = True
            except ElementClickInterceptedException:
                staleElement = True
driver.close()
print('complete')
