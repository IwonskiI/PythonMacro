from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import keyboard
import pyperclip
import time

naver_info = {'nid': 'whdgnl1006', 'npw': 'gnldi1006'}
input_boxes = {'id': '/ html/body/table[2]/tbody/tr/td/table[1]/tbody/tr/td/table/tbody/tr[1]/td[2]/input',
               'pass': '/html/body/table[2]/tbody/tr/td/table[1]/tbody/tr/td/table/tbody/tr[2]/td[2]/input',
               'word': '/html/body/table[2]/tbody/tr/td/table[1]/tbody/tr/td/table/tbody/tr[4]/td[2]/input',
               'nid': '//*[@id="id"]',
               'npw': '//*[@id="pw"]',
               'nname': '//*[@id="orderForm"]/div/div[3]/div[1]/div[2]/div[1]/div/input[1]',
               'nphone1': '//*[@id="deliveryAddress.telNo1_2"]',
               'nphone2': '//*[@id="deliveryAddress.telNo1_3"]',
               'addr_search': '//*[@id="ipt_lb"]',
               'subaddrbox': '//*[@id="selected_address"]',
               'textbox': '//*[@id="orderForm"]/div/div[3]/div[1]/div[3]/div/div/div/input[1]',
               'pidbox': '//*[@id="orderForm"]/div/div[3]/div[1]/div[4]/div[1]/input[2]',
               'order_num': ']/td[5]/table/tbody/tr[1]/td/input',
               'price': ']/td[5]/table/tbody/tr[2]/td/input',
               'date': ']/td[6]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/textarea'
               }
buttons = {'login': '/html/body/table[2]/tbody/tr/td/table[1]/tbody/tr/td/table/tbody/tr[6]/td/div/a',
           'origin': '//*[@id="menu_top"]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/table[3]/tbody/tr/td/table[1]/tbody/tr[2]/td[2]/table/tbody/tr/td[2]/div[2]/div[2]/a[4]',
           'order_info1': '//*[@id="menu_top"]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/table[3]/tbody/tr/td/table[1]/tbody/tr[',
           'order_info2': ']/td[2]/table/tbody/tr/td[2]/div[2]/div[2]/a[1]',
           'order_info3': ']/td[2]/table/tbody/tr/td[2]/div[2]/div/a[1]',
           'order_info4': ']/td[2]/table/tbody/tr/td[2]/div[2]/div[3]/a[1]',
           'login_naver': '//*[@id="log.login"]',
           'new_address': '//*[@id="newAddressRadio"]/span',
           'search_address': '//*[@id="orderForm"]/div/div[3]/div[1]/div[2]/div[5]/div/button',
           'search_address2': '//*[@id="pop_content"]/form/div[1]/div/a',
           'address_result': '//*[@id="zip0"]',
           'addr_submit': '//*[@id="pop_footer"]/a[1]',
           'pid_change': '//*[@id="orderForm"]/div/div[3]/div[1]/div[4]/div[1]/div[1]/button',
           'pid_change1': '//*[@id="orderForm"]/div/div[3]/div[1]/div[4]/div[1]/div[1]/button',
           'buy_naver': '//*[@id="orderForm"]/div/div[7]/button',
           'popup': '//*[@id="order"]/div[5]/div/div[2]/div/button[2]',
           'submit': '//*[@id="getorder_menu"]/table[3]/tbody/tr/td[1]/a[1]',
           'pidcheck': '//*[@id="menu_top"]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/a',
           'pidconfirm1': '/html/body/div[2]/form/table[3]/tbody/tr[', 'pidconfirm2': ']/td[2]/a',
           'order_confirm': '/html/body/div[2]/form/div[1]/a[1]',
           'order_close': '/html/body/div[2]/form/div[1]/a[2]'
           }
select_boxes = {'ps_status': '//*[@id="getorder_menu"]/table[2]/tbody/tr/td[2]/table/tbody/tr/td/select[5]',
                'pay_comp': '//*[@id="getorder_menu"]/table[2]/tbody/tr/td[2]/table/tbody/tr/td/select[5]/option[9]',
                'del_comp': '//*[@id="getorder_menu"]/table[2]/tbody/tr/td[2]/table/tbody/tr/td/select[5]/option[17]',
                'pid_check1': '//*[@id="purchaserSocialSecurityAgreeFirstCheckbox"]/span',
                'pid_check2': '//*[@id="purchaserSocialSecurityAgreeSecondCheckbox"]/span',
                'confirm': '//*[@id="iiomaAgree"]/span',
                'order_status': ']/td[6]/table/tbody/tr[1]/td/select',
                'pay_complete': ']/td[6]/table/tbody/tr[1]/td/select/option[2]',
                'order_stop': ']/td[6]/table/tbody/tr[1]/td/select/option[3]',
                'order_complete': ']/td[6]/table/tbody/tr[1]/td/select/option[10]',
                'phone_select': '//*[@id="cellPhone"]/div/div',
                'phone_option': '/html/body/div[9]/div/ul/li[',
                'credit_select': '//*[@id="monthNaverPay"]',
                }
information = {'name': '/html/body/div[2]/form/table[3]/tbody/tr[2]/td[2]/input',
               'phone': '/html/body/div[2]/form/table[3]/tbody/tr[3]/td[2]/input[1]',
               'address': '/html/body/div[2]/form/table[3]/tbody/tr[4]/td[2]/table/tbody/tr[2]/td/input',
               'sub_address': '/html/body/div[2]/form/table[3]/tbody/tr[4]/td[2]/table/tbody/tr[3]/td/input',
               'text': '/html/body/div[2]/form/table[3]/tbody/tr[5]/td[2]',
               'pid1': '/html/body/div[2]/form/table[3]/tbody/tr[', 'pid2': ']/td[2]/input[1]',
               'order_num': '//*[@id="order"]/div[2]/div[2]/div[1]/a/strong',
               'price': '//*[@id="order"]/div[2]/div[3]/div/div[2]/div/p/em',
               'pidinfo': '//*[@id="menu_top"]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/span',
               'pname1': '/html/body/div[2]/form/table[3]/tbody/tr[', 'pname2': ']/td[2]/div[3]/table/tbody/tr[1]/td[2]',
               'pphone1': '/html/body/div[2]/form/table[3]/tbody/tr[', 'pphone2': ']/td[2]/div[3]/table/tbody/tr[2]/td[2]',
               'ppid1': '/html/body/div[2]/form/table[3]/tbody/tr[', 'ppid2': ']/td[2]/div[3]/table/tbody/tr[3]/td[2]',
               'msg': '//*[@id="custom_msg"]'
               }
css_selector = {
    'buy_naver': '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div.XqRGHcrncz > div:nth-child(1) > div:nth-child('}

##############################################

# 주문처리 날짜 계산함수


def date():
    year = datetime.today().year
    month = datetime.today().month
    if(month < 10):
        months = "0"+str(month)
    else:
        months = str(month)
    day = datetime.today().day
    if(day < 10):
        days = "0"+str(day)
    else:
        days = str(day)
    return(str(year)+"-"+months+"-"+days+" 주문완료")

# 휴대폰 첫번째 자리 처리 함수


def first_phone(num):
    if num == "010":
        return "1"
    elif num == "011":
        return "2"
    elif num == "016":
        return "3"
    elif num == "017":
        return "4"
    elif num == "018":
        return "5"
    elif num == "019":
        return "6"
    elif num == "02":
        return "7"
    elif num == "031":
        return "8"
    elif num == "032":
        return "9"
    elif num == "033":
        return "10"
    elif num == "041":
        return "11"
    elif num == "042":
        return "12"
    elif num == "043":
        return "13"
    elif num == "044":
        return "14"
    elif num == "051":
        return "15"
    elif num == "052":
        return "16"
    elif num == "053":
        return "17"
    elif num == "054":
        return "18"
    elif num == "055":
        return "19"
    elif num == "061":
        return "20"
    elif num == "062":
        return "21"
    elif num == "063":
        return "22"
    elif num == "064":
        return "23"
    elif num == "070":
        return "24"
    elif num == "080":
        return "25"
    elif num == "0130":
        return "26"
    elif num == "0303":
        return "27"
    elif num == "0502":
        return "28"
    elif num == "0503":
        return "29"
    elif num == "0504":
        return "30"
    elif num == "0505":
        return "31"
    elif num == "0506":
        return "32"
    elif num == "0507":
        return "33"
    elif num == "0508":
        return "34"
    elif num == "050":
        return "35"
    elif num == "012":
        return "36"
    elif num == "059":
        return "37"

# 요소 찾기 함수


def find_element(xpath):
    wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    return driver.find_element(By.XPATH, xpath)

# css selector 요소 찾기 함수


def find_element_css(css):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
    return driver.find_element(By.CSS_SELECTOR, css)

# 대기시간 조절 요소 찾기 함수


def find_element1(xpath, time):
    wait2 = WebDriverWait(driver, time)
    wait2.until(EC.presence_of_element_located((By.XPATH, xpath)))
    return driver.find_element("xpath", xpath)

##############################################

# 실행 시 출력 설명


def desc_S():
    print("ctrl+shift+1 => 주문처리 프로세스")
    print("ctrl+shift+2 => 통관부호 프로세스")
    print("ctrl+shift+u => 업데이트 내역 확인")
    print("ctrl+shift+q => 프로그램 종료")

# 첫번째 주문 처리 설명


def desc_o1():
    # print("<초기 시작 방법>")
    # print("1.마켓그룹 설정")
    # print("2.가장 첫번째 상품 원문 링크 클릭")
    # print("3.옵션 설정 및 수량 체크 이후 '실행 단축키'(Ctrl+Shift+1) 입력")
    # print("4.모든 정보 입력 완료까지 대기 이후 카드 설정 이후 결제진행")
    # print("5.결제 완료이후 창에서 '실행 단축키'(Ctrl+Shift+1) 입력해서 주문정보 전달")
    # print("--------- 초기 세팅 완료 ---------")
    # print("이후 진행 시 출력되는 인덱스를 확인하며 원문 링크 클릭후")
    # print("옵션 선택 및 수량 체크 이후 '실행 단축키' 입력")
    # print("이전 메뉴로 => ('ctrl+shift+q)")
    print("<스마트스토어 프로세스 실행 방법>")
    print("1. 마켓 그룹 설정")
    print("2. 원문링크 클릭 후 상품 주문 가능상태 확인")
    print("3. 상품에 문제가 없다면 상품 옵션 설정 이후 원문링크 실행 키(Ctrl+Shift+1) 입력")
    print("4. 상품에 문제가 있을경우 인덱스 증가/감소 키(Ctrl+Shift+3/4)로 상품 스킵")
    print("5. 프로세스 완료 후 저장할 경우 선택 수정 키(Ctrl+Shift+5) 입력")
    print("6. 선택 수정 완료 후 다른 프로세스 선택, 혹은 프로그램 종료를 위해 이전 단계로 돌아가려면 종료 키(Ctrl+Shift+q) 입력")
    print("")

# 두번째 이상 주문처리 설명


def desc_o2():
    global menu_cnt
    print("ctrl+shift+1 => 실행")
    print("ctrl+shift+2 => 인덱스 증가")
    print("ctrl+shift+3 => 인덱스 감소")
    print("ctrl+shift+4 => 선택 수정 및 인덱스 초기화")
    print("ctrl+shift+q => 프로그램 종료")
    print("현재 상품 인덱스 : ", str(menu_cnt - 1)+"번째 상품")
    print("")

##############################################

# 더망고 로그인 함수


def login():
    id_box = find_element(input_boxes['id'])
    id_box.send_keys("whdgnl1006")
    pass_box = find_element(input_boxes['pass'])
    pass_box.send_keys("dodfk100")
    find_element(input_boxes['word']).click()
    print("자동입력방지문자를 입력한 뒤 진행키(Ctrl+Shift+1)를 눌러주세요.")
    while True:
        try:
            if keyboard.is_pressed('ctrl+shift+1'):
                break
            else:
                pass
        except:
            pass
    login_btn = find_element(buttons['login'])
    login_btn.click()
    driver.implicitly_wait(1)
    print('Complete Login!')

# 네이버 로그인 함수


def nlogin():
    driver.execute_script(
        'window.open("https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com");')
    driver.switch_to.window(driver.window_handles[1])
    pyperclip.copy(naver_info['nid'])
    find_element(input_boxes['nid']).send_keys(Keys.CONTROL, 'v')
    pyperclip.copy(naver_info['npw'])
    find_element(input_boxes['npw']).send_keys(Keys.CONTROL, 'v')
    find_element(buttons['login_naver']).click()
    driver.implicitly_wait(1)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

##############################################

# 주문처리 프로세스 함수


def order_process():
    global pid_index, menu_cnt
    find_element(select_boxes['ps_status']).click()
    # find_element(select_boxes['del_comp']).click()
    find_element(select_boxes['pay_comp']).click()
    desc_o1()
    while True:
        desc_o2()
        while True:
            if keyboard.is_pressed('ctrl+shift+1'):
                time.sleep(1)
                try:
                    driver.switch_to.window(driver.window_handles[1])
                    if find_element_css(css_selector['buy_naver']+"1)").get_attribute("class") == "OgETmrvExa sys_chk_buy N=a:pcs.buy":
                        find_element_css(
                            css_selector['buy_naver']+"1) > a").click()
                    elif find_element_css(css_selector['buy_naver']+"2)").get_attribute("class") == "OgETmrvExa sys_chk_buy N=a:pcs.buy":
                        find_element_css(
                            css_selector['buy_naver']+"2) > a").click()
                    else:
                        print("오류입니다. 현재 상품은 매크로를 이용하실 수 없습니다. 제작자에게 문의 바랍니다.")
                        return
                    order()
                    break
                except:
                    print("다시 시도해주세요.")
                    print("")
                    time.sleep(0.5)
                    break
            elif keyboard.is_pressed('ctrl+shift+2'):
                time.sleep(1)
                menu_cnt += 1
                break
            elif keyboard.is_pressed('ctrl+shift+3'):
                time.sleep(1)
                menu_cnt -= 1
                break
            elif keyboard.is_pressed('ctrl+shift+4'):
                menu_cnt = 2
                driver.switch_to.window(driver.window_handles[0])
                find_element(buttons['submit']).click()
                time.sleep(0.3)
                driver.switch_to.alert.accept()
                break
            elif keyboard.is_pressed('ctrl+shift+q'):
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[0])
                menu_cnt = 2
                print("네이버 프로세스를 종료하고 이전단계로 이동합니다.")
                print("")
                return

# 주문 프로세스


def order():
    global menu_cnt
    order_flag = False
    driver.switch_to.window(driver.window_handles[0])
    try:
        if order_flag == False:
            orderinfo = buttons['order_info1'] + \
                str(menu_cnt) + buttons['order_info2']
            ordertext = orderinfo + '/span'
            if find_element(ordertext).text == "주문정보":
                order_flag = True
                find_element(orderinfo).click()
    except:
        pass
    try:
        if order_flag == False:
            orderinfo = buttons['order_info1'] + \
                str(menu_cnt) + buttons['order_info3']
            ordertext = orderinfo + '/span'
            if find_element(ordertext).text == "주문정보":
                order_flag = True
                find_element(orderinfo).click()
    except:
        pass
    try:
        if order_flag == False:
            orderinfo = buttons['order_info1'] + \
                str(menu_cnt) + buttons['order_info4']
            ordertext = orderinfo + '/span'
            if find_element(ordertext).text == "주문정보":
                order_flag = True
                find_element(orderinfo).click()
    except:
        pass
    if order_flag == False:
        print("오류가 발생했습니다. 다시 시도하여주세요.")
        return
    driver.switch_to.window(driver.window_handles[2])
    driver.set_window_size(width/10*3, height)
    driver.set_window_position(width/10*7, 0)
    driver.switch_to.window(driver.window_handles[1])
    driver.set_window_size(width/10*7, height)
    driver.set_window_position(0, 0)
    driver.implicitly_wait(1)
    find_element(buttons['new_address']).click()
    driver.switch_to.window(driver.window_handles[2])
    pyperclip.copy(find_element(information['name']).get_attribute("value"))
    driver.switch_to.window(driver.window_handles[1])
    find_element(input_boxes['nname']).send_keys(Keys.CONTROL, 'v')
    phone()
    address()
    complete()
    menu_cnt += 1

# 전화번호 처리 함수


def phone():
    driver.switch_to.window(driver.window_handles[2])
    phone = find_element(information['phone']).get_attribute("value")
    phone = phone.replace("-", "")
    if len(phone) == 12:
        phone0 = phone[:4]
        phone1 = phone[4:-4]
    else:
        phone0 = phone[:3]
        phone1 = phone[3:-4]
    phone2 = phone[-4:]
    driver.switch_to.window(driver.window_handles[1])
    find_element(select_boxes['phone_select']).click()
    find_element(select_boxes['phone_option']+first_phone(phone0)+"]").click()
    pyperclip.copy(phone1)
    find_element(input_boxes['nphone1']).send_keys(Keys.CONTROL, 'v')
    pyperclip.copy(phone2)
    find_element(input_boxes['nphone2']).send_keys(Keys.CONTROL, 'v')

# 주소/요청사항/통관부호 처리함수


def address():
    global pid_index
    driver.switch_to.window(driver.window_handles[2])
    addr = find_element(information['address']).get_attribute("value")
    pyperclip.copy(addr)
    driver.switch_to.window(driver.window_handles[1])
    find_element(buttons['search_address']).click()
    driver.switch_to.window(driver.window_handles[3])
    driver.implicitly_wait(1)
    find_element(input_boxes['addr_search']).send_keys(Keys.CONTROL, 'v')
    find_element(buttons['search_address2']).click()
    print("주소를 선택한 이후 진행 단축키 (ctrl+shift+1)를 눌러주세요.")
    print("프로그램을 중지하려면 중단키(ctrl+shift+q)를 입력하세요.")
    print("")
    while True:
        try:
            if keyboard.is_pressed('ctrl+shift+1'):
                break
            elif keyboard.is_pressed('ctrl+shift+q'):
                driver.switch_to.window(driver.window_handles[3])
                driver.close()
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(1)
                return
        except:
            pass
    driver.switch_to.window(driver.window_handles[2])
    subaddr = find_element(information['sub_address']).get_attribute("value")
    if subaddr == "":
        subaddrs = addr.split(') ')
        if len(subaddrs) == 1:
            pass
        else:
            subaddr = subaddrs[-1]
    pyperclip.copy(subaddr)
    driver.switch_to.window(driver.window_handles[3])
    find_element(input_boxes['subaddrbox']).send_keys(Keys.CONTROL, 'v')
    find_element(buttons['addr_submit']).click()
    driver.switch_to.window(driver.window_handles[2])
    texts = find_element(information['text']).text
    if texts[:4] == "통관부호":
        texts = ""
        pid_index = 5
    idx_text = texts.find("(주문번호 : ")
    if idx_text != -1:
        texts = texts[:idx_text]
    idx_text2 = texts.find("[고객배송메모]")
    if idx_text2 != -1:
        texts = texts[8:]
    idx_text3 = texts.find("직접 입력")
    if idx_text3 != -1:
        texts = texts[5:]
    pyperclip.copy(texts)
    driver.switch_to.window(driver.window_handles[1])
    find_element(input_boxes['textbox']).send_keys(Keys.CONTROL, 'v')
    driver.switch_to.window(driver.window_handles[2])
    pidbox = information['pid1'] + str(pid_index) + information['pid2']
    pyperclip.copy(find_element(pidbox).get_attribute("value"))
    driver.switch_to.window(driver.window_handles[1])
    find_element(buttons['pid_change']).click()
    try:
        find_element('//*[@id="icuc"]')
        find_element(input_boxes['pidbox']).clear()
        find_element(input_boxes['pidbox']).send_keys(Keys.CONTROL, 'v')
        find_element(select_boxes['pid_check1']).click()
        find_element(select_boxes['pid_check2']).click()
    except:
        pass
    pid_index = 6
    find_element(select_boxes['credit_select']).click()
    find_element(select_boxes['credit_select']).click()
    try:
        find_element1(select_boxes['confirm'], 0.5).click()
    except:
        pass
    if menu_cnt != 2:
        find_element(buttons['buy_naver']).click()

# 결제 완료시 처리 프로세스


def complete():
    global menu_cnt
    print("결제 완료 창일때, 진행키(ctrl+shift+1) 입력")
    print("이전 단계로 나가려면 종료키(ctrl+shift+q) 입력")
    while True:
        try:
            if keyboard.is_pressed('ctrl+shift+1'):
                break
            elif keyboard.is_pressed('ctrl+shift+q'):
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[2])
                driver.close()
                driver.switch_to.window(driver.window_handles[1])
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                driver.maximize_window()
                menu_cnt -= 1
                return
        except:
            pass
    try:
        find_element1(buttons['popup'], 1).click()
    except:
        pass
    driver.switch_to.window(driver.window_handles[2])
    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    driver.maximize_window()
    order = buttons['order_info1'] + str(menu_cnt)
    order_num_box = order + input_boxes['order_num']
    price_box = order + input_boxes['price']
    status = order + select_boxes['order_status']
    status_comp = order + select_boxes['order_complete']
    textbox = order + input_boxes['date']
    order_num = find_element(information['order_num']).text
    price = find_element(information['price']).text
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    find_element(order_num_box).send_keys(order_num)
    find_element(price_box).send_keys(price)
    find_element(status).click()
    find_element(status_comp).click()
    find_element(textbox).clear()
    find_element(textbox).send_keys(date())

# 전화번호 처리 함수


def phone_bar(phone):
    num1 = phone[:3]
    num2 = phone[3:-4]
    num3 = phone[-4:]
    return num1+"-"+num2+"-"+num3

##############################################

# 통관부호 처리 함수


def pid_func(driver, i):
    global pid_idx
    driver.switch_to.window(driver.window_handles[1])
    texts = find_element(information['text']).text
    if texts[:4] == "통관부호":
        texts = ""
        pid_idx = 5
    find_element(information['name']).clear()
    names = find_element(
        information['pname1']+str(pid_idx)+information['pname2']).text.lstrip(": &nbsp")
    find_element(information['name']).send_keys(names)
    find_element(information['phone']).clear()
    phones = find_element(information['pphone1']+str(pid_idx) +
                          information['pphone2']).text.lstrip(": &nbsp").replace("-", "")
    find_element(information['phone']).send_keys(phone_bar(phones))
    pidbox = information['pid1'] + str(pid_idx) + information['pid2']
    find_element(pidbox).clear()
    pids = find_element(
        information['ppid1']+str(pid_idx)+information['ppid2']).text.lstrip(": &nbsp")
    find_element(pidbox).send_keys(pids)
    find_element(buttons['pidconfirm1']+str(pid_idx) +
                 buttons['pidconfirm2']).click()
    time.sleep(0.3)
    if find_element(information['msg']).text == "→ "+names+"("+pids+" / "+phones+") 정보로 개인통관부호가 검증되었습니다.\n→ 통관부호 검증 후 배송정보수정을 하셔야 배송정보에 반영됩니다.":
        print("complete!")
        find_element(buttons['order_confirm']).click()
        time.sleep(0.2)
        driver.switch_to.alert.accept()
        # find_element(buttons['order_close']).click()
        driver.switch_to.window(driver.window_handles[0])
        find_element(buttons['order_info1'] + str(i) +
                     select_boxes['order_status']).click()
        time.sleep(0.5)
        find_element(buttons['order_info1'] + str(i) +
                     select_boxes['pay_complete']).click()
    else:
        print("failed..")
        # find_element(buttons['order_close']).click()
        driver.switch_to.window(driver.window_handles[0])
        find_element(buttons['order_info1'] + str(i) +
                     select_boxes['order_status']).click()
        find_element(buttons['order_info1'] + str(i) +
                     select_boxes['order_stop']).click()
        find_element(buttons['order_info1'] + str(i) +
                     input_boxes['date']).clear()
        find_element(buttons['order_info1'] + str(i) +
                     input_boxes['date']).send_keys("통관부호")

# 첫번째 정보 클릭 후 alert창 없애기


def pid_click(i):
    try:
        orderinfo = '//*[@id="menu_top"]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/table[3]/tbody/tr/td/table[1]/tbody/tr[{}]/td[2]/table/tbody/tr/td[2]/div[2]/div[2]/a[1]'.format(
            i)
        find_element(orderinfo).click()
        driver.switch_to.window(driver.window_handles[1])
        driver.switch_to.alert.accept()
    except:
        try:
            orderinfo = '//*[@id="menu_top"]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/table[3]/tbody/tr/td/table[1]/tbody/tr[{}]/td[2]/table/tbody/tr/td[2]/div[2]/div/a[1]'.format(
                i)
            find_element(orderinfo).click()
            driver.switch_to.window(driver.window_handles[1])
            driver.switch_to.alert.accept()
        except:
            orderinfo = '//*[@id="menu_top"]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/table[3]/tbody/tr/td/table[1]/tbody/tr[{}]/td[2]/table/tbody/tr/td[2]/div[2]/div[3]/a[1]'.format(
                i)
            find_element(orderinfo).click()
            driver.switch_to.window(driver.window_handles[1])
            driver.switch_to.alert.accept()

# 두번째 이상 정보 클릭 및 통관부호 입력


def pid_click2(i):
    try:
        orderinfo = '//*[@id="menu_top"]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/table[3]/tbody/tr/td/table[1]/tbody/tr[{}]/td[2]/table/tbody/tr/td[2]/div[2]/div[2]/a[1]'.format(
            i)
        driver.switch_to.window(driver.window_handles[0])
        find_element(orderinfo).click()
        driver.switch_to.window(driver.window_handles[1])
        driver.switch_to.alert.accept()
        print(driver.window_handles)
        pid_func(driver, i)
        driver.switch_to.window(driver.window_handles[0])
    except:
        try:
            orderinfo = '//*[@id="menu_top"]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/table[3]/tbody/tr/td/table[1]/tbody/tr[{}]/td[2]/table/tbody/tr/td[2]/div[2]/div/a[1]'.format(
                i)
            driver.switch_to.window(driver.window_handles[0])
            find_element(orderinfo).click()
            driver.switch_to.window(driver.window_handles[1])
            driver.switch_to.alert.accept()
            print(driver.window_handles)
            pid_func(driver, i)
            driver.switch_to.window(driver.window_handles[0])
        except:
            orderinfo = '//*[@id="menu_top"]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/table[3]/tbody/tr/td/table[1]/tbody/tr[{}]/td[2]/table/tbody/tr/td[2]/div[2]/div[3]/a[1]'.format(
                i)
            driver.switch_to.window(driver.window_handles[0])
            find_element(orderinfo).click()
            driver.switch_to.window(driver.window_handles[1])
            driver.switch_to.alert.accept()
            print(driver.window_handles)
            pid_func(driver, i)
            driver.switch_to.window(driver.window_handles[0])

# 통관부호 프로세스


def pid_process():
    global pid_idx
    product_idx = 3  # 상품 번호
    try:
        # 처리 횟수 구하기 - 시작 인덱스는 2, 첫번째 상품은 수동 처리이므로 2번째 상품(인덱스 3)부터 처리하기 위한 과정
        pidcnt = int(find_element1(information['pidinfo'], 1).text.lstrip(
            '문자메세지를 통해 통관번호를 입력받은 주문건이 ').rstrip('건 확인됩니다.'))+2
    except:
        print("처리할 통관번호 오류 건이 없습니다!")
        time.sleep(1)
        return
    print("처리할 건이 "+(pidcnt-2)+"건 있습니다!")
    find_element(buttons['pidcheck']).click()
    driver.switch_to.window(driver.window_handles[0])
    driver.close()
    print("ctrl+shift+1 입력 후 확인창이 사라지면 ctrl+shift+2 입력")
    print("ctrl+shift+q 입력 시 이전단계로 이동")
    while True:
        try:
            if keyboard.is_pressed('ctrl+shift+1'):
                driver.switch_to.window(driver.window_handles[0])
                try:
                    add_ship = '//*[@id="menu_top"]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/table[3]/tbody/tr/td/table[1]/tbody/tr[{}]/td[2]/table/tbody/tr/td[2]/b'.format(
                        2)
                    find_element(add_ship)
                    pid_click(2)
                    product_idx += 1
                except:
                    pid_click(2)
            if keyboard.is_pressed('ctrl+shift+2'):
                driver.switch_to.window(driver.window_handles[1])
                pid_func(driver, 2)
                for i in range(product_idx, pidcnt):
                    try:
                        add_ship = '//*[@id="menu_top"]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/table[3]/tbody/tr/td/table[1]/tbody/tr[{}]/td[2]/table/tbody/tr/td[2]/b'.format(
                            i)
                        find_element(add_ship)
                        pid_click(2)
                        product_idx += 1
                    except:
                        pid_click2(i)
                break
            elif keyboard.is_pressed('ctrl+shift+q'):
                return
        except:
            pass
    driver.switch_to.window(driver.window_handles[1])
    find_element(buttons['order_close']).click()
    driver.switch_to.window(driver.window_handles[0])
    find_element(buttons['submit']).click()
    time.sleep(0.3)
    driver.switch_to.alert.accept()

##############################################

# 업데이트 내역


def update():
    print("###################업데이트 내역###################")
    print("v1.0.0 - 매크로 제작")
    print("v1.1.0 - 네이버 로그인 기능 추가")
    print("v1.1.1 - 크롬드라이버 온라인 업데이트 기능 추가")
    print("v1.1.2 - 결제 완료 프로세스 추가")
    print("v1.1.3 - 더망고 익스텐션 기능 추가")
    print("v2.0.0 - 통관부호 프로세스 추가")
    print("v2.1.0 - 통관부호 프로세스 베타 테스트")
    print("v2.2.0 - 통관부포 프로세스 베타 테스트 오류 수정-1")
    print("v2.2.1 - 통관부포 프로세스 베타 테스트 오류 수정-1")
    print("v2.2.2 - 통관부호 프로세스 기능 - 알림창 수정")
    print("v2.3.0 - 통관부호 프로세스 기능 수정 - 미완료")
    print("v2.4.0 - 통관부호 프로세스 기능 수정 - 완료")
    print("v2.5.0 - 주문처리 프로세스_인덱스 초기화 기능 추가 / 주문처리 프로세스_배송요청사항 수정 기능 추가")
    print("v2.6.0 - 로그인 기능 변경")
    print("v3.0.0 - 화면 비율 변경 및 쿠팡 옵션 상황 적용")
    print("v3.0.1 - 인덱스 자동증가 오류 수정")
    print("##################################################")
    print("")
    # print("통관부호 프로세스_합배송 처리기능 추가 / 주문처리 프로세스_국내상품 통관부호 스킵기능 추가")

##############################################


print("더망고 매크로 V3.0.1 - by . wonski")
start = time.time()
options = webdriver.ChromeOptions()
options.add_extension('./extention/themango.crx')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 5)
driver.maximize_window()
size = driver.get_window_size()
width = size.get("width")
height = size.get("height")
driver.get("https://tmg547.cafe24.com/mall/admin/admin_login.php")
driver.implicitly_wait(1)
login()
driver.implicitly_wait(1)
driver.execute_script('window.open("/mall/admin/admin_getorder.php");')
driver.switch_to.window(driver.window_handles[0])
driver.close()
driver.switch_to.window(driver.window_handles[0])
nlogin()
desc_S()
while True:
    try:
        if keyboard.is_pressed('ctrl+shift+1'):
            menu_cnt = 2
            pid_index = 6
            order_process()
            desc_S()
        elif keyboard.is_pressed('ctrl+shift+2'):
            pid_idx = 6
            pid_process()
            desc_S()
        elif keyboard.is_pressed('ctrl+shift+u'):
            update()
            time.sleep(1)
            desc_S()
        elif keyboard.is_pressed('ctrl+shift+q'):
            print("프로그램을 종료합니다.")
            print("")
            time.sleep(1)
            break
        elif keyboard.is_pressed('ctrl+shift+/'):
            print("debug mode")
    except:
        pass
driver.quit()
