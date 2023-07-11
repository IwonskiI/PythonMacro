from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import re
import time
import json

elements = {'red': '//*[@id="filterListWineType"]/li[1]/div/label',
            'white': '//*[@id="filterListWineType"]/li[2]/div/label',
            'sparkling': '//*[@id="filterListWineType"]/li[3]/div/label',
            'rose': '//*[@id="filterListWineType"]/li[4]/div/label',
            'fortified': '//*[@id="filterListWineType"]/li[5]/div/label',
            'etc': '//*[@id="filterListWineType"]/li[6]/div/label',
            'sort_list': '//*[@id="shOrder1"]',
            'sort_pop': '//*[@id="shOrder1"]/option[4]',
            'more_info': '//*[@id="wineListMoreBtn"]',
            'wine_list1': '//*[@id="wine_list"]/li[',
            'wine_list2': ']/div[2]/div[1]/h3/a',
            'back': '/html/body/section/div[3]/div[1]/a',
            'first_list': '/html/body/section/div[3]/div[2]/div[2]/div[3]/div[1]/div[1]/span',
            'second_list': '/html/body/section/div[3]/div[2]/div[2]/div[3]/div[2]/div[1]/span',
            'top': '/html/body/div[2]/p[2]',
            }
wine_elem = {'kor_name': '/html/body/section/div[3]/div[2]/div[2]/dl/dt',
             'eng_name': '/html/body/section/div[3]/div[2]/div[2]/dl/dd',
             'price': '/html/body/section/div[3]/div[2]/div[2]/p[1]/strong',
             'sweet': '/html/body/section/div[3]/div[2]/div[2]/div[2]/ul/li[1]/div',
             'acid': '/html/body/section/div[3]/div[2]/div[2]/div[2]/ul/li[2]/div',
             'body': '/html/body/section/div[3]/div[2]/div[2]/div[2]/ul/li[3]/div',
             'tannin': '/html/body/section/div[3]/div[2]/div[2]/div[2]/ul/li[4]/div',
             'aroma_cnt': '/html/body/section/div[3]/div[2]/div[2]/div[3]/div[1]/div[2]/ul',
             'aroma': '/html/body/section/div[3]/div[2]/div[2]/div[3]/div[1]/div[2]/ul/li[',
             'pairing_cnt': '/html/body/section/div[3]/div[2]/div[2]/div[3]/div[2]/div[2]/ul',
             'pairing': '/html/body/section/div[3]/div[2]/div[2]/div[3]/div[2]/div[2]/ul/li[',
             'ending': ']/p',
             'img_ending': ']/em/img',
             'rating1': '/html/body/section/div[3]/div[2]/div[2]/div[3]/div[',
             'rating2': ']/div[1]/dl[2]/dd/span',
             'table': '//*[@id="detail"]/div/div',
             'img': '/html/body/section/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]/img',
             'type': '/html/body/section/div[3]/div[2]/div[2]/div[1]/p/span[1]',
             }

total_list = []


def find_element(xpath):
    wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    return driver.find_element(By.XPATH, xpath)


def count_rating(element):
    cnt = 0
    rate = element.find_elements(By.TAG_NAME, 'a')
    for i in rate:
        if i.get_attribute("class") == "on":
            cnt += 1
    return cnt


def average(lst):
    sum = 0
    for i in lst:
        sum += int(i)
    return int(sum/2)


driver = webdriver.Chrome(ChromeDriverManager().install())
wait = WebDriverWait(driver, 5)
driver.maximize_window()
url = 'https://www.wine21.com/13_search/wine_list.html'
driver.get(url)
driver.implicitly_wait(5)
time.sleep(1)


# # 레드와인
# find_element(elements['red']).click()
# time.sleep(1)
# find_element(elements['sort_list']).click()
# time.sleep(1)
# find_element(elements['sort_pop']).click()
# time.sleep(10)
# wine_list = []

# for cnt in tqdm(range(40), desc='more_info'):
#     find_element(elements['more_info']).click()
#     time.sleep(10)

# find_element(elements['top']).click()
# time.sleep(3)


# for i in tqdm(range(1, 401), desc='red_wine'):
#     excepts = 3
#     flag = 0
#     wine_dict = {}
#     find_element(elements['wine_list1']+str(i)+elements['wine_list2']).click()
#     time.sleep(1)
#     wine_dict['kor_name'] = find_element(
#         wine_elem['kor_name']).text.replace('\"', "")
#     wine_dict['eng_name'] = find_element(
#         wine_elem['eng_name']).text.replace('\"', "")
#     wine_dict['imgsrc'] = find_element(wine_elem['img']).get_attribute('src')
#     wine_dict['r_type'] = find_element(wine_elem['type']).text
#     wine_dict['price'] = int(int(find_element(wine_elem['price']).text.replace(
#         "원", "").replace("가격정보없음", "0").replace(",", ""))/16)
#     wine_dict['sweet'] = count_rating(find_element(wine_elem['sweet']))
#     wine_dict['acid'] = count_rating(find_element(wine_elem['acid']))
#     wine_dict['body'] = count_rating(find_element(wine_elem['body']))
#     wine_dict['tannin'] = count_rating(find_element(wine_elem['tannin']))
#     try:
#         if find_element(elements['first_list']).text == '아로마':
#             aroma_size = find_element(wine_elem['aroma_cnt'])
#             aroma_cnt = len(aroma_size.find_elements(By.TAG_NAME, 'li'))
#             if aroma_cnt >= 5:
#                 aroma_cnt = 4
#             wine_dict['aroma'] = {}
#             for j in range(aroma_cnt):
#                 wine_dict['aroma'][find_element(wine_elem['aroma']+str(j+1) + wine_elem['img_ending']).get_attribute('src')] = find_element(
#                     wine_elem['aroma']+str(j+1) + wine_elem['ending']).text.replace('\'', '').split(',  ')
#         elif find_element(elements['first_list']).text == '음식매칭':
#             pairing_size = find_element(wine_elem['aroma_cnt'])
#             pairing_cnt = len(pairing_size.find_elements(By.TAG_NAME, 'li'))
#             if pairing_cnt >= 5:
#                 pairing_cnt = 4
#             wine_dict['pairing'] = {}
#             for j in range(pairing_cnt):
#                 wine_dict['pairing'][find_element(wine_elem['aroma']+str(j+1) + wine_elem['img_ending']).get_attribute('src')] = find_element(
#                     wine_elem['aroma']+str(j+1) + wine_elem['ending']).text.replace('\'', '').split(',  ')
#     except:
#         excepts = 1
#         flag = 1
#         pass
#     try:
#         pairing_size = find_element(wine_elem['pairing_cnt'])
#         pairing_cnt = len(pairing_size.find_elements(By.TAG_NAME, 'li'))
#         if pairing_cnt >= 5:
#             pairing_cnt = 4
#         wine_dict['pairing'] = {}
#         for j in range(pairing_cnt):
#             wine_dict['pairing'][find_element(wine_elem['pairing']+str(j+1) + wine_elem['img_ending']).get_attribute('src')] = find_element(
#                 wine_elem['pairing']+str(j+1) + wine_elem['ending']).text.replace('\'', '').split(',  ')
#     except:
#         excepts = 2
#         if flag == 1:
#             excepts = 1
#         pass
#     wine_dict['rating'] = find_element(
#         wine_elem['rating1']+str(excepts)+wine_elem['rating2']).text
#     table = find_element(wine_elem['table'])
#     table_comp = table.find_elements(By.TAG_NAME, 'dl')
#     for comp in table_comp:
#         if comp.find_element(By.TAG_NAME, 'dt').text == "음용온도":
#             temp = comp.find_element(By.TAG_NAME, 'dd').text.replace(" ℃", "")
#             temp = re.split('~|-|/', temp)
#             wine_dict['temp'] = average(temp)
#         elif comp.find_element(By.TAG_NAME, 'dt').text == "알코올":
#             wine_dict['alcohol'] = comp.find_element(By.TAG_NAME, 'dd').text
#     wine_dict['type'] = 'Red'
#     wine_list.append(wine_dict)
#     find_element(elements['back']).click()
#     time.sleep(1)

# total_list.extend(wine_list)

# with open("red.json", "w") as f:
#     json.dump(wine_list, f)

# find_element(elements['top']).click()
# time.sleep(3)

# # 화이트와인
# find_element(elements['white']).click()
# time.sleep(1)
# find_element(elements['red']).click()
# time.sleep(1)
# find_element(elements['sort_list']).click()
# time.sleep(1)
# find_element(elements['sort_pop']).click()
# time.sleep(10)
# wine_list = []


# for cnt in tqdm(range(30), desc='more_info'):
#     find_element(elements['more_info']).click()
#     time.sleep(10)

# find_element(elements['top']).click()
# time.sleep(3)


# for i in tqdm(range(1, 301), desc='white_wine'):
#     excepts = 3
#     flag = 0
#     wine_dict = {}
#     find_element(elements['wine_list1']+str(i)+elements['wine_list2']).click()
#     time.sleep(1)
#     wine_dict['kor_name'] = find_element(
#         wine_elem['kor_name']).text.replace('\"', "")
#     wine_dict['eng_name'] = find_element(
#         wine_elem['eng_name']).text.replace('\"', "")
#     wine_dict['imgsrc'] = find_element(wine_elem['img']).get_attribute('src')
#     wine_dict['r_type'] = find_element(wine_elem['type']).text
#     wine_dict['price'] = int(int(find_element(wine_elem['price']).text.replace(
#         "원", "").replace("가격정보없음", "0").replace(",", ""))/16)
#     wine_dict['sweet'] = count_rating(find_element(wine_elem['sweet']))
#     wine_dict['acid'] = count_rating(find_element(wine_elem['acid']))
#     wine_dict['body'] = count_rating(find_element(wine_elem['body']))
#     wine_dict['tannin'] = count_rating(find_element(wine_elem['tannin']))
#     try:
#         if find_element(elements['first_list']).text == '아로마':
#             aroma_size = find_element(wine_elem['aroma_cnt'])
#             aroma_cnt = len(aroma_size.find_elements(By.TAG_NAME, 'li'))
#             if aroma_cnt >= 5:
#                 aroma_cnt = 4
#             wine_dict['aroma'] = {}
#             for j in range(aroma_cnt):
#                 wine_dict['aroma'][find_element(wine_elem['aroma']+str(j+1) + wine_elem['img_ending']).get_attribute('src')] = find_element(
#                     wine_elem['aroma']+str(j+1) + wine_elem['ending']).text.replace('\'', '').split(',  ')
#         elif find_element(elements['first_list']).text == '음식매칭':
#             pairing_size = find_element(wine_elem['aroma_cnt'])
#             pairing_cnt = len(pairing_size.find_elements(By.TAG_NAME, 'li'))
#             if pairing_cnt >= 5:
#                 pairing_cnt = 4
#             wine_dict['pairing'] = {}
#             for j in range(pairing_cnt):
#                 wine_dict['pairing'][find_element(wine_elem['aroma']+str(j+1) + wine_elem['img_ending']).get_attribute('src')] = find_element(
#                     wine_elem['aroma']+str(j+1) + wine_elem['ending']).text.replace('\'', '').split(',  ')
#     except:
#         excepts = 1
#         flag = 1
#         pass
#     try:
#         pairing_size = find_element(wine_elem['pairing_cnt'])
#         pairing_cnt = len(pairing_size.find_elements(By.TAG_NAME, 'li'))
#         if pairing_cnt >= 5:
#             pairing_cnt = 4
#         wine_dict['pairing'] = {}
#         for j in range(pairing_cnt):
#             wine_dict['pairing'][find_element(wine_elem['pairing']+str(j+1) + wine_elem['img_ending']).get_attribute('src')] = find_element(
#                 wine_elem['pairing']+str(j+1) + wine_elem['ending']).text.replace('\'', '').split(',  ')
#     except:
#         excepts = 2
#         if flag == 1:
#             excepts = 1
#         pass
#     wine_dict['rating'] = find_element(
#         wine_elem['rating1']+str(excepts)+wine_elem['rating2']).text
#     table = find_element(wine_elem['table'])
#     table_comp = table.find_elements(By.TAG_NAME, 'dl')
#     for comp in table_comp:
#         if comp.find_element(By.TAG_NAME, 'dt').text == "음용온도":
#             temp = comp.find_element(By.TAG_NAME, 'dd').text.replace(" ℃", "")
#             temp = re.split('~|-|/', temp)
#             wine_dict['temp'] = average(temp)
#         elif comp.find_element(By.TAG_NAME, 'dt').text == "알코올":
#             wine_dict['alcohol'] = comp.find_element(By.TAG_NAME, 'dd').text
#     wine_dict['type'] = 'White'
#     wine_list.append(wine_dict)
#     find_element(elements['back']).click()
#     time.sleep(1)

# total_list.extend(wine_list)

# with open("white.json", "w") as f:
#     json.dump(wine_list, f)

# find_element(elements['top']).click()
# time.sleep(3)


# # 스파클링와인
# find_element(elements['sparkling']).click()
# time.sleep(1)
# find_element(elements['white']).click()
# time.sleep(1)
# find_element(elements['sort_list']).click()
# time.sleep(1)
# find_element(elements['sort_pop']).click()
# time.sleep(10)
# wine_list = []

# for cnt in tqdm(range(30), desc='more_info'):
#     find_element(elements['more_info']).click()
#     time.sleep(1)
#     print(cnt)

# find_element(elements['top']).click()
# time.sleep(3)

# for i in tqdm(range(1, 301), desc='sparkling_wine'):
#     excepts = 3
#     flag = 0
#     wine_dict = {}
#     find_element(elements['wine_list1']+str(i)+elements['wine_list2']).click()
#     time.sleep(1)
#     wine_dict['kor_name'] = find_element(
#         wine_elem['kor_name']).text.replace('\"', "")
#     wine_dict['eng_name'] = find_element(
#         wine_elem['eng_name']).text.replace('\"', "")
#     wine_dict['imgsrc'] = find_element(wine_elem['img']).get_attribute('src')
#     wine_dict['r_type'] = find_element(wine_elem['type']).text
#     wine_dict['price'] = int(int(find_element(wine_elem['price']).text.replace(
#         "원", "").replace("가격정보없음", "0").replace(",", ""))/16)
#     wine_dict['sweet'] = count_rating(find_element(wine_elem['sweet']))
#     wine_dict['acid'] = count_rating(find_element(wine_elem['acid']))
#     wine_dict['body'] = count_rating(find_element(wine_elem['body']))
#     wine_dict['tannin'] = count_rating(find_element(wine_elem['tannin']))
#     try:
#         if find_element(elements['first_list']).text == '아로마':
#             aroma_size = find_element(wine_elem['aroma_cnt'])
#             aroma_cnt = len(aroma_size.find_elements(By.TAG_NAME, 'li'))
#             if aroma_cnt >= 5:
#                 aroma_cnt = 4
#             wine_dict['aroma'] = {}
#             for j in range(aroma_cnt):
#                 wine_dict['aroma'][find_element(wine_elem['aroma']+str(j+1) + wine_elem['img_ending']).get_attribute('src')] = find_element(
#                     wine_elem['aroma']+str(j+1) + wine_elem['ending']).text.replace('\'', '').split(',  ')
#         elif find_element(elements['first_list']).text == '음식매칭':
#             pairing_size = find_element(wine_elem['aroma_cnt'])
#             pairing_cnt = len(pairing_size.find_elements(By.TAG_NAME, 'li'))
#             if pairing_cnt >= 5:
#                 pairing_cnt = 4
#             wine_dict['pairing'] = {}
#             for j in range(pairing_cnt):
#                 wine_dict['pairing'][find_element(wine_elem['aroma']+str(j+1) + wine_elem['img_ending']).get_attribute('src')] = find_element(
#                     wine_elem['aroma']+str(j+1) + wine_elem['ending']).text.replace('\'', '').split(',  ')
#     except:
#         excepts = 1
#         flag = 1
#         pass
#     try:
#         pairing_size = find_element(wine_elem['pairing_cnt'])
#         pairing_cnt = len(pairing_size.find_elements(By.TAG_NAME, 'li'))
#         if pairing_cnt >= 5:
#             pairing_cnt = 4
#         wine_dict['pairing'] = {}
#         for j in range(pairing_cnt):
#             wine_dict['pairing'][find_element(wine_elem['pairing']+str(j+1) + wine_elem['img_ending']).get_attribute('src')] = find_element(
#                 wine_elem['pairing']+str(j+1) + wine_elem['ending']).text.replace('\'', '').split(',  ')
#     except:
#         excepts = 2
#         if flag == 1:
#             excepts = 1
#         pass
#     wine_dict['rating'] = find_element(
#         wine_elem['rating1']+str(excepts)+wine_elem['rating2']).text
#     table = find_element(wine_elem['table'])
#     table_comp = table.find_elements(By.TAG_NAME, 'dl')
#     for comp in table_comp:
#         if comp.find_element(By.TAG_NAME, 'dt').text == "음용온도":
#             temp = comp.find_element(By.TAG_NAME, 'dd').text.replace(" ℃", "")
#             temp = re.split('~|-|/', temp)
#             wine_dict['temp'] = average(temp)
#         elif comp.find_element(By.TAG_NAME, 'dt').text == "알코올":
#             wine_dict['alcohol'] = comp.find_element(By.TAG_NAME, 'dd').text
#     wine_dict['type'] = 'Sparkling'
#     wine_list.append(wine_dict)
#     find_element(elements['back']).click()
#     time.sleep(1)

# total_list.extend(wine_list)

# with open("sparkling.json", "w") as f:
#     json.dump(wine_list, f)


# find_element(elements['top']).click()
# time.sleep(3)

# # 로제와인
# find_element(elements['rose']).click()
# time.sleep(1)
# find_element(elements['sparkling']).click()
# time.sleep(1)
# find_element(elements['sort_list']).click()
# time.sleep(1)
# find_element(elements['sort_pop']).click()
# time.sleep(10)
# wine_list = []

# for cnt in tqdm(range(10), desc='more_info'):
#     find_element(elements['more_info']).click()
#     time.sleep(10)

# find_element(elements['top']).click()
# time.sleep(3)

# for i in tqdm(range(1, 101), desc='rose_wine'):
#     excepts = 3
#     flag = 0
#     wine_dict = {}
#     find_element(elements['wine_list1']+str(i)+elements['wine_list2']).click()
#     time.sleep(1)
#     wine_dict['kor_name'] = find_element(
#         wine_elem['kor_name']).text.replace('\"', "")
#     wine_dict['eng_name'] = find_element(
#         wine_elem['eng_name']).text.replace('\"', "")
#     wine_dict['imgsrc'] = find_element(wine_elem['img']).get_attribute('src')
#     wine_dict['r_type'] = find_element(wine_elem['type']).text
#     wine_dict['price'] = int(int(find_element(wine_elem['price']).text.replace(
#         "원", "").replace("가격정보없음", "0").replace(",", ""))/16)
#     wine_dict['sweet'] = count_rating(find_element(wine_elem['sweet']))
#     wine_dict['acid'] = count_rating(find_element(wine_elem['acid']))
#     wine_dict['body'] = count_rating(find_element(wine_elem['body']))
#     wine_dict['tannin'] = count_rating(find_element(wine_elem['tannin']))
#     try:
#         if find_element(elements['first_list']).text == '아로마':
#             aroma_size = find_element(wine_elem['aroma_cnt'])
#             aroma_cnt = len(aroma_size.find_elements(By.TAG_NAME, 'li'))
#             if aroma_cnt >= 5:
#                 aroma_cnt = 4
#             wine_dict['aroma'] = {}
#             for j in range(aroma_cnt):
#                 wine_dict['aroma'][find_element(wine_elem['aroma']+str(j+1) + wine_elem['img_ending']).get_attribute('src')] = find_element(
#                     wine_elem['aroma']+str(j+1) + wine_elem['ending']).text.replace('\'', '').split(',  ')
#         elif find_element(elements['first_list']).text == '음식매칭':
#             pairing_size = find_element(wine_elem['aroma_cnt'])
#             pairing_cnt = len(pairing_size.find_elements(By.TAG_NAME, 'li'))
#             if pairing_cnt >= 5:
#                 pairing_cnt = 4
#             wine_dict['pairing'] = {}
#             for j in range(pairing_cnt):
#                 wine_dict['pairing'][find_element(wine_elem['aroma']+str(j+1) + wine_elem['img_ending']).get_attribute('src')] = find_element(
#                     wine_elem['aroma']+str(j+1) + wine_elem['ending']).text.replace('\'', '').split(',  ')
#     except:
#         excepts = 1
#         flag = 1
#         pass
#     try:
#         pairing_size = find_element(wine_elem['pairing_cnt'])
#         pairing_cnt = len(pairing_size.find_elements(By.TAG_NAME, 'li'))
#         if pairing_cnt >= 5:
#             pairing_cnt = 4
#         wine_dict['pairing'] = {}
#         for j in range(pairing_cnt):
#             wine_dict['pairing'][find_element(wine_elem['pairing']+str(j+1) + wine_elem['img_ending']).get_attribute('src')] = find_element(
#                 wine_elem['pairing']+str(j+1) + wine_elem['ending']).text.replace('\'', '').split(',  ')
#     except:
#         excepts = 2
#         if flag == 1:
#             excepts = 1
#         pass
#     wine_dict['rating'] = find_element(
#         wine_elem['rating1']+str(excepts)+wine_elem['rating2']).text
#     table = find_element(wine_elem['table'])
#     table_comp = table.find_elements(By.TAG_NAME, 'dl')
#     for comp in table_comp:
#         if comp.find_element(By.TAG_NAME, 'dt').text == "음용온도":
#             temp = comp.find_element(By.TAG_NAME, 'dd').text.replace(" ℃", "")
#             temp = re.split('~|-|/', temp)
#             wine_dict['temp'] = average(temp)
#         elif comp.find_element(By.TAG_NAME, 'dt').text == "알코올":
#             wine_dict['alcohol'] = comp.find_element(By.TAG_NAME, 'dd').text
#     wine_dict['type'] = 'Rose'
#     wine_list.append(wine_dict)
#     find_element(elements['back']).click()
#     time.sleep(1)

# total_list.extend(wine_list)

# with open("rose.json", "w") as f:
#     json.dump(wine_list, f)


# find_element(elements['top']).click()
# time.sleep(3)


# 주정강화와인
find_element(elements['fortified']).click()
time.sleep(1)
# find_element(elements['rose']).click()
# time.sleep(1)
find_element(elements['sort_list']).click()
time.sleep(1)
find_element(elements['sort_pop']).click()
time.sleep(10)
wine_list = []

for cnt in tqdm(range(2), desc='more_info'):
    find_element(elements['more_info']).click()
    time.sleep(10)

find_element(elements['top']).click()
time.sleep(3)

for i in tqdm(range(1, 21), desc='fortified_wine'):
    excepts = 3
    flag = 0
    wine_dict = {}
    find_element(elements['wine_list1']+str(i)+elements['wine_list2']).click()
    time.sleep(1)
    wine_dict['kor_name'] = find_element(
        wine_elem['kor_name']).text.replace('\"', "")
    wine_dict['eng_name'] = find_element(
        wine_elem['eng_name']).text.replace('\"', "")
    wine_dict['imgsrc'] = find_element(wine_elem['img']).get_attribute('src')
    wine_dict['r_type'] = find_element(wine_elem['type']).text
    wine_dict['price'] = int(int(find_element(wine_elem['price']).text.replace(
        "원", "").replace("가격정보없음", "0").replace(",", ""))/16)
    wine_dict['sweet'] = count_rating(find_element(wine_elem['sweet']))
    wine_dict['acid'] = count_rating(find_element(wine_elem['acid']))
    wine_dict['body'] = count_rating(find_element(wine_elem['body']))
    wine_dict['tannin'] = count_rating(find_element(wine_elem['tannin']))
    try:
        if find_element(elements['first_list']).text == '아로마':
            aroma_size = find_element(wine_elem['aroma_cnt'])
            aroma_cnt = len(aroma_size.find_elements(By.TAG_NAME, 'li'))
            if aroma_cnt >= 5:
                aroma_cnt = 4
            wine_dict['aroma'] = {}
            for j in range(aroma_cnt):
                wine_dict['aroma'][find_element(wine_elem['aroma']+str(j+1) + wine_elem['img_ending']).get_attribute('src')] = find_element(
                    wine_elem['aroma']+str(j+1) + wine_elem['ending']).text.replace('\'', '').split(',  ')
        elif find_element(elements['first_list']).text == '음식매칭':
            pairing_size = find_element(wine_elem['aroma_cnt'])
            pairing_cnt = len(pairing_size.find_elements(By.TAG_NAME, 'li'))
            if pairing_cnt >= 5:
                pairing_cnt = 4
            wine_dict['pairing'] = {}
            for j in range(pairing_cnt):
                wine_dict['pairing'][find_element(wine_elem['aroma']+str(j+1) + wine_elem['img_ending']).get_attribute('src')] = find_element(
                    wine_elem['aroma']+str(j+1) + wine_elem['ending']).text.replace('\'', '').split(',  ')
    except:
        excepts = 1
        flag = 1
        pass
    try:
        pairing_size = find_element(wine_elem['pairing_cnt'])
        pairing_cnt = len(pairing_size.find_elements(By.TAG_NAME, 'li'))
        if pairing_cnt >= 5:
            pairing_cnt = 4
        wine_dict['pairing'] = {}
        for j in range(pairing_cnt):
            wine_dict['pairing'][find_element(wine_elem['pairing']+str(j+1) + wine_elem['img_ending']).get_attribute('src')] = find_element(
                wine_elem['pairing']+str(j+1) + wine_elem['ending']).text.replace('\'', '').split(',  ')
    except:
        excepts = 2
        if flag == 1:
            excepts = 1
        pass
    wine_dict['rating'] = find_element(
        wine_elem['rating1']+str(excepts)+wine_elem['rating2']).text
    table = find_element(wine_elem['table'])
    table_comp = table.find_elements(By.TAG_NAME, 'dl')
    for comp in table_comp:
        if comp.find_element(By.TAG_NAME, 'dt').text == "음용온도":
            temp = comp.find_element(By.TAG_NAME, 'dd').text.replace(" ℃", "")
            temp = re.split('~|-|/', temp)
            wine_dict['temp'] = average(temp)
        elif comp.find_element(By.TAG_NAME, 'dt').text == "알코올":
            wine_dict['alcohol'] = comp.find_element(By.TAG_NAME, 'dd').text
    wine_dict['type'] = 'Fortified'
    wine_list.append(wine_dict)
    find_element(elements['back']).click()
    time.sleep(1)

total_list.extend(wine_list)

with open("fortified.json", "w") as f:
    json.dump(wine_list, f)


find_element(elements['top']).click()
time.sleep(3)


# 기타와인
find_element(elements['etc']).click()
time.sleep(1)
find_element(elements['fortified']).click()
time.sleep(1)
find_element(elements['sort_list']).click()
time.sleep(1)
find_element(elements['sort_pop']).click()
time.sleep(10)
wine_list = []

for cnt in tqdm(range(2), desc='more_info'):
    find_element(elements['more_info']).click()
    time.sleep(10)

find_element(elements['top']).click()
time.sleep(3)

for i in tqdm(range(1, 21), desc='etc_wine'):
    excepts = 3
    flag = 0
    wine_dict = {}
    find_element(elements['wine_list1']+str(i)+elements['wine_list2']).click()
    time.sleep(1)
    wine_dict['kor_name'] = find_element(
        wine_elem['kor_name']).text.replace('\"', "")
    wine_dict['eng_name'] = find_element(
        wine_elem['eng_name']).text.replace('\"', "")
    wine_dict['imgsrc'] = find_element(wine_elem['img']).get_attribute('src')
    wine_dict['r_type'] = find_element(wine_elem['type']).text
    wine_dict['price'] = int(int(find_element(wine_elem['price']).text.replace(
        "원", "").replace("가격정보없음", "0").replace(",", ""))/16)
    wine_dict['sweet'] = count_rating(find_element(wine_elem['sweet']))
    wine_dict['acid'] = count_rating(find_element(wine_elem['acid']))
    wine_dict['body'] = count_rating(find_element(wine_elem['body']))
    wine_dict['tannin'] = count_rating(find_element(wine_elem['tannin']))
    try:
        if find_element(elements['first_list']).text == '아로마':
            aroma_size = find_element(wine_elem['aroma_cnt'])
            aroma_cnt = len(aroma_size.find_elements(By.TAG_NAME, 'li'))
            if aroma_cnt >= 5:
                aroma_cnt = 4
            wine_dict['aroma'] = {}
            for j in range(aroma_cnt):
                wine_dict['aroma'][find_element(wine_elem['aroma']+str(j+1) + wine_elem['img_ending']).get_attribute('src')] = find_element(
                    wine_elem['aroma']+str(j+1) + wine_elem['ending']).text.replace('\'', '').split(',  ')
        elif find_element(elements['first_list']).text == '음식매칭':
            pairing_size = find_element(wine_elem['aroma_cnt'])
            pairing_cnt = len(pairing_size.find_elements(By.TAG_NAME, 'li'))
            if pairing_cnt >= 5:
                pairing_cnt = 4
            wine_dict['pairing'] = {}
            for j in range(pairing_cnt):
                wine_dict['pairing'][find_element(wine_elem['aroma']+str(j+1) + wine_elem['img_ending']).get_attribute('src')] = find_element(
                    wine_elem['aroma']+str(j+1) + wine_elem['ending']).text.replace('\'', '').split(',  ')
    except:
        excepts = 1
        flag = 1
        pass
    try:
        pairing_size = find_element(wine_elem['pairing_cnt'])
        pairing_cnt = len(pairing_size.find_elements(By.TAG_NAME, 'li'))
        if pairing_cnt >= 5:
            pairing_cnt = 4
        wine_dict['pairing'] = {}
        for j in range(pairing_cnt):
            wine_dict['pairing'][find_element(wine_elem['pairing']+str(j+1) + wine_elem['img_ending']).get_attribute('src')] = find_element(
                wine_elem['pairing']+str(j+1) + wine_elem['ending']).text.replace('\'', '').split(',  ')
    except:
        excepts = 2
        if flag == 1:
            excepts = 1
        pass
    wine_dict['rating'] = find_element(
        wine_elem['rating1']+str(excepts)+wine_elem['rating2']).text
    table = find_element(wine_elem['table'])
    table_comp = table.find_elements(By.TAG_NAME, 'dl')
    for comp in table_comp:
        if comp.find_element(By.TAG_NAME, 'dt').text == "음용온도":
            temp = comp.find_element(By.TAG_NAME, 'dd').text.replace(" ℃", "")
            temp = re.split('~|-|/', temp)
            wine_dict['temp'] = average(temp)
        elif comp.find_element(By.TAG_NAME, 'dt').text == "알코올":
            wine_dict['alcohol'] = comp.find_element(By.TAG_NAME, 'dd').text
    wine_dict['type'] = 'Etc.'
    wine_list.append(wine_dict)
    find_element(elements['back']).click()
    time.sleep(1)
total_list.extend(wine_list)

with open("etc.json", "w") as f:
    json.dump(wine_list, f)


with open("wine_data.json", "w") as f:
    json.dump(total_list, f)
