################## 스프레드시트 import #########################
import gspread
from oauth2client.service_account import ServiceAccountCredentials
###############################################################

###################### 셀레니움 import #########################
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import sys
###############################################################

# 요소 찾기 함수


def find_element(xpath):
    wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    return driver.find_element(By.XPATH, xpath)


# 스프레드시트 열기
scope = ['https://spreadsheets.google.com/feeds']
json_file_name = './olivemacro-c80840dd37d3.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    json_file_name, scope)
gc = gspread.authorize(credentials)
# 실제 링크
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/12PEeXJ8D6LqWsXjqmvR7LIQZ-xKylzPRcK1Ngbb9VFs/edit#gid=0'

# 디버깅용 링크
# spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1Y_gxBV79HctWv4s6Kg3FscBV2ITHhAbtiIFI7Kwalw8/edit?copiedFromTrash#gid=0'
doc = gc.open_by_url(spreadsheet_url)
sheet_name = input('시트이름을 입력해주세요:')
try:
    worksheet = doc.worksheet(sheet_name)
    links = worksheet.col_values(3)
    price = worksheet.col_values(2)
except:
    print("입력하신 시트를 찾을 수 없습니다. 입력하신 시트 이름을 확인해주세요.")

# 셀레니움 실행
error = []
blank = []
update = []
error_index = 0
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("headless")
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 2)
driver.maximize_window()
size = driver.get_window_size()
width = size.get("width")
height = size.get("height")
driver.get(spreadsheet_url)
driver.implicitly_wait(1)
print("-현재 진행 상황")
try:
    for idx, link in enumerate(links):
        error_index = idx
        sys.stdout.write("\r{} % ( {} / {} )".format(
            str(round((idx/len(links))*100, 1)), str(idx), str(len(links))))
        if link == 'URL':
            pass
        elif link == "":
            blank.append(idx+1)
            cell = 'B' + str(idx+1) + ':C' + str(idx+1)
            worksheet.format(cell, {
                "backgroundColor": {
                    "red": 1.0,
                    "green": 1.0,
                    "blue": 0.0
                }
            })
        else:
            driver.execute_script('window.open("' + link + '");')
            driver.switch_to.window(driver.window_handles[1])
            driver.implicitly_wait(1)
            value = ""
            try:
                value = find_element(
                    '//*[@id="Contents"]/div[2]/div[2]/div/div[1]/span[2]/strong').text
            except:
                try:
                    value = find_element(
                        '//*[@id="Contents"]/div[2]/div[2]/div/div[1]/span/strong').text
                except:
                    error.append(idx+1)
                    cell = 'B' + str(idx+1) + ':C' + str(idx+1)
                    worksheet.format(cell, {
                        "backgroundColor": {
                            "red": 1.0,
                            "green": 0.0,
                            "blue": 0.0
                        },
                        "textFormat": {
                            "foregroundColor": {
                                "red": 1.0,
                                "green": 1.0,
                                "blue": 1.0
                            }
                        }
                    })
            cell = 'B' + str(idx+1)
            if value != "":
                if len(price) >= idx+1:
                    if value != price[idx]:
                        update.append(idx+1)
                        worksheet.update_acell(cell, value)
                        cell = 'B' + str(idx+1) + ':C' + str(idx+1)
                        worksheet.format(cell, {
                            "backgroundColor": {
                                "red": 0.0,
                                "green": 1.0,
                                "blue": 0.0
                            },
                            "textFormat": {
                                "foregroundColor": {
                                    "red": 0.0,
                                    "green": 0.0,
                                    "blue": 0.0
                                }
                            }
                        })
                    else:
                        worksheet.update_acell(cell, value)
                        cell = 'B' + str(idx+1) + ':C' + str(idx+1)
                        worksheet.format(cell, {
                            "backgroundColor": {
                                "red": 1.0,
                                "green": 1.0,
                                "blue": 1.0
                            },
                            "textFormat": {
                                "foregroundColor": {
                                    "red": 0.0,
                                    "green": 0.0,
                                    "blue": 0.0
                                }
                            }
                        })
                else:
                    worksheet.update_acell(cell, value)
                    cell = 'B' + str(idx+1) + ':C' + str(idx+1)
                    worksheet.format(cell, {
                        "backgroundColor": {
                            "red": 1.0,
                            "green": 1.0,
                            "blue": 1.0
                        },
                        "textFormat": {
                            "foregroundColor": {
                                "red": 0.0,
                                "green": 0.0,
                                "blue": 0.0
                            }
                        }
                    })
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    print("")
    print("")
    print("가격 정보 업데이트를 완료했습니다.")
    print("- 링크 없는 상품 인덱스 - 노랑")
    print(blank)
    print("")
    print("- 링크 오류 상품 인덱스 - 빨강")
    print(error)
    print("")
    print("- 가격 변동 상품 인덱스 - 초록")
    print(update)

    driver.quit()
except:
    print(str(error_index+1) + "번 상품에서 오류가 발생했습니다. 오류가 발생한 링크와 함께 개발자에게 문의해주세요.")
    driver.quit()

print("")
print("시트 결과를 출력합니다.")
sheet_index = 0
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 2)
driver.maximize_window()
size = driver.get_window_size()
width = size.get("width")
height = size.get("height")
driver.get(spreadsheet_url)
sheets = find_element(
    '/html/body/div[5]/div/div[4]/table/tbody/tr[2]/td[3]/div/div[3]/div').text.split('\n ')
for idx, sheet in enumerate(sheets):
    if sheet == sheet_name:
        sheet_index = idx+1
try:
    find_element('/html/body/div[5]/div/div[4]/table/tbody/tr[2]/td[3]/div/div[3]/div/div['+str(
        sheet_index)+']/div/div/div[1]/span').click()
except:
    print("입력하신 시트를 찾을 수 없습니다. 입력하신 시트 이름을 확인해주세요.")
