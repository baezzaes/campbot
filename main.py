from selenium import webdriver
from datetime import date
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import telegram
import requests
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

### 알림 제외 시간 ###
if int(time.strftime('%H')) > 0 and int(time.strftime('%H')) < 6:   # 새벽시간 알림 차단
    quit()

# Telegram Setting
chat = telegram.Bot(token = "1824090062:AAFqgbvUKtBA1xGrDrevpPjlM_uNd_IVBwI")
chat_id = "-1001512203758"
#chat_id = "1510104965"      # 테스트용
# text = "abcd"
# chat.sendMessage(chat_id = chat_id, text=text)
# quit()

# webdriver chrome 옵션
options = webdriver.ChromeOptions()
options.add_argument('headless')        # 웹 브라우저를 띄우지 않는 headless chrome 옵션
options.add_argument('disable-gpu')     # GPU 사용 안함
options.add_argument('lang=ko_KR')      # 언어 설정
options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 로그 숨김
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')

driver = webdriver.Chrome("./chromedriver", options=options)
driver.implicitly_wait(3)

t = ['월', '화', '수', '목', '금', '토', '일']

# 주말 체크
chkday = date.today()
# fridays = []
# sundays = []
fridays = ["2022-10-08"]
sundays = ["2022-10-10"]
weekNo = 0
# while True:
#     if chkday.weekday() == 4:
#         fridays.append(str(chkday))
#         sundays.append(str(chkday + timedelta(days=2)))
#         # 2022 현충일
#         if str(chkday) == "2022-06-03":
#             fridays.append(str("2022-06-04"))
#             sundays.append(str("2022-06-06"))
#         # 2022 광복절
#         elif str(chkday) == "2022-08-12":
#             fridays.append(str("2022-08-13"))
#             sundays.append(str("2022-08-15"))
#         # 2022 추석
#         elif str(chkday) == "2022-09-09":
#             fridays.append(str("2022-09-10"))
#             sundays.append(str("2022-09-12"))
#         # 2022 개천절
#         elif str(chkday) == "2022-09-30":
#             fridays.append(str("2022-10-01"))
#             sundays.append(str("2022-10-03"))
#         # 2022 한글날
#         elif str(chkday) == "2022-10-07":
#             fridays.append(str("2022-10-08"))
#             sundays.append(str("2022-10-10"))
#         weekNo+=1
#         if weekNo == 8:
#             break
#     chkday = chkday + timedelta(days=1)

#driver.get("https://m.booking.naver.com/booking/3/bizes/481805/items?startDate=2021-07-30&endDate=2021-08-01")

# try:
#     driver.find_element_by_class_name("summary_body")
# except Exception as error:
#     print(error)

# quit()


sites = []
sitelist = ""
string = ""


#### 캠핏 예약 ####
dicCamp = {'625d36bc0b5a84001eea82b8':'어썸', '61cc191740d609001e3b576f':'씨사이드힐', '60c720c5d5987e001ed2d293':'파인힐', '60b0c91a00b65c001fc71485':'아라뜰', '629461309128d2001ec4869b':'서종힐링', '60b990527978ea001ecbc3b6':'에코유'}
#dicCamp = {'610cda0155fc69001e1b1ca6':'리버힐'}
for k in dicCamp.keys():
    for i in range(0,len(fridays)):

        s_timestamp = time.mktime(datetime.strptime(fridays[i], '%Y-%m-%d').timetuple())
        e_timestamp = time.mktime(datetime.strptime(sundays[i], '%Y-%m-%d').timetuple())
        # 밀리세컨드
        s_timestamp = int(s_timestamp) * 1000
        e_timestamp = int(e_timestamp) * 1000

        # headerDict = {}
        # headerDict.setdefault('user-agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')

        # paramDict = {}
        # paramDict.setdefault('startTimestamp', int(s_timestamp))
        # paramDict.setdefault('endTimestamp', int(e_timestamp))

        #requestData = requests.get('https://api.camfit.co.kr/v1/camps/zones/'+k, params=paramDict)
        #requestData = requests.get('https://api.camfit.co.kr/v1/camps/zones/'+k+"?startTimestamp="+str(int(s_timestamp))+"&endTimestamp="+str(int(e_timestamp)), headers=headerDict)
        #### rest api 실패 보안문제 ####
        #print('https://api.camfit.co.kr/v1/camps/zones/'+k+"?startTimestamp="+str(int(s_timestamp))+"&endTimestamp="+str(int(e_timestamp)))

        #print(requestData.status_code)

        driver.get("https://api.camfit.co.kr/v1/camps/zones/"+k+"?id="+k+"&adult=2&teen=0&child=2&startTimestamp="+str(s_timestamp)+"&endTimestamp="+str(e_timestamp)+"&limit=100&skip=0")
        print("https://api.camfit.co.kr/v1/camps/zones/"+k+"?id="+k+"&adult=2&teen=0&child=2&startTimestamp="+str(s_timestamp)+"&endTimestamp="+str(e_timestamp)+"&limit=100&skip=0")
        responseData = driver.find_element_by_xpath('//*').text
        jsonData = json.loads(responseData)

        for j in range(0, len(jsonData)):
            #print(jsonData[j]["numOfAvailableSites"])
            if(jsonData[j]["numOfAvailableSites"] != 0):
                if dicCamp[k] == "리버힐" and jsonData[j]["name"].find("프리미엄") > -1:    #리버힐 제외 SITE
                    continue
                elif dicCamp[k] == "씨사이드힐" and jsonData[j]["name"].find("커플") > -1:  #씨사이드힐 제외 SITE
                    continue
                elif dicCamp[k] == "아라뜰":
                    if jsonData[j]["name"].find("B구역") > -1:     # 아라뜰 선호 SITE
                        sites.append(jsonData[j]["name"])
                    else:
                        continue
                elif dicCamp[k] == "서종힐링":      # 서종힐링 선호 SITE
                    if jsonData[j]["name"].find("A1") > -1 or jsonData[j]["name"].find("A2") > -1 or jsonData[j]["name"].find("A3") > -1 or jsonData[j]["name"].find("A4") > -1 or jsonData[j]["name"].find("A5") > -1 or jsonData[j]["name"].find("A6") > -1 or jsonData[j]["name"].find("A7") > -1 or jsonData[j]["name"].find("A8") > -1 or jsonData[j]["name"].find("A16") > -1 or jsonData[j]["name"].find("B7") > -1:
                        sites.append(jsonData[j]["name"])
                    else:
                        continue
                elif dicCamp[k] == '에코유':        # 에코유 선호 SITE
                    if jsonData[j]["name"].find("G") > -1 or jsonData[j]["name"].find("H") > -1:
                        sites.append(jsonData[j]["name"])
                    else:
                        continue

                else:
                    sites.append(jsonData[j]["name"])

        if len(sites) == 0:
            sitelist = ""
            result = "X"
        elif len(sites) >= 1: #and len(sites) <=10:
            sitelist = str(sites)
            result = "O"

        print(dicCamp[k] + " / " + fridays[i] + " ~ " + sundays[i] + " : " + result + (" - " if len(sites) > 0 else "") + sitelist)

        if result == "O":
            string += dicCamp[k] + " / " + fridays[i] + " ~ " + sundays[i] + "\n " + sitelist + "\n" + "https://camfit.co.kr/search/result?camp="+dicCamp[k]+"&checkInTimestamp="+str(s_timestamp)+"&checkoutTimestamp="+str(e_timestamp)+"\n"

        sites = []
        sitelist = ""

        time.sleep(1)

    if string != "":
        #if int(time.strftime('%H')) == 0 or int(time.strftime('%H')) >= 6:   # 새벽시간 알림 차단
        chat.sendMessage(chat_id = chat_id, text=string)
        string = ""

#quit()

#### 네이버예약 ####
dicCamp = {'59772':'아버지의숲', '481805':'돌고래', '14972':'마리원', '278756':'대부도비치'}
#dicCamp = {'160759':'마장호수휴', '557521':'캠핑느루', '160905':'리프레쉬', '299264':'해여림빌리지', '394663':'답게', '529626':'아롱별', '164989':'물왕숲','627922':'솔잎향', '607387':'을왕리솔트', '1142':'캄파슬로우'}

for k in dicCamp.keys():
    for i in range(0,len(fridays)):
        driver.get("https://m.booking.naver.com/booking/3/bizes/"+ k +"/items?startDate=" + fridays[i] + "&endDate=" + sundays[i])

        try:
            find = driver.find_element_by_class_name("result_txt")
            #find = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "result_txt")))
            #print(find)
            result = "X"
        except Exception as error:
            #print(error)
            result = "O"
            finds = driver.find_elements_by_css_selector(".summary_body .desc_title")
            for j in finds:
                if j.text == "카라반 CARAVAN" or j.text == "캠프렛 CAMPLET" or j.text == "차박&루프탑&파쇄석 존" or j.text.find("룸텐트") > -1:       # 물왕숲 제외 SITE
                    continue
                elif k == '278756' and (j.text.find("캠핑 B") > -1 or j.text.find("캠핑 C") > -1 or j.text.find("캠핑 D") > -1):     # 대부도비치 제외 SITE
                    continue
                elif k == '299264' and (j.text.find("Hill") > -1 or j.text.find("Pond") > -1):     # 해여림빌리지 제외 SITE
                    continue
                elif k == '14972' and (j.text.find("숲 14") > -1 or j.text.find("숲 15") > -1 or j.text.find("숲 16") > -1):    # 마리원 제외 SITE
                    continue
                elif k == '481805' and j.text.find("소나무") > -1:        # 돌고래 제외 SITE
                    continue
                elif j.text.find("펜션") > -1 or j.text.find("방가로") > -1 or j.text.find("커플") > -1 or j.text.find("하우스") > -1 or j.text.find("캠프닉") > -1 or j.text.find("단골전용") > -1 or j.text.find("글램핑") > -1 or j.text.find("오두막") > -1 or j.text.find("방갈로") > -1:
                    continue
                else:
                    if k == '607387':      # 을왕리솔트 선호 SITE
                        if j.text.find("B-1 ") > -1 or j.text.find("B-2") > -1 or j.text.find("B-3") > -1 or j.text.find("B-4") > -1:
                            sites.append(j.text)
                        else:
                            continue

                    else:
                        sites.append(j.text)

            if len(sites) == 0:
                sitelist = ""
                result = "X"
            elif len(sites) >= 1 and len(sites) <=10:
                sitelist = str(sites)
            elif len(sites) > 10:
                sitelist = "예약가능 사이트수 : " + str(len(sites)) + "건"

        print(dicCamp[k] + " / " + fridays[i] + " ~ " + sundays[i] + " : " + result + (" - " if len(sites) > 0 else "") + sitelist)
        if result == "O":
            string += dicCamp[k] + " / " + fridays[i] + " ~ " + sundays[i] + "\n " + sitelist + "\n" + "https://m.booking.naver.com/booking/3/bizes/"+ k +"/items?startDate=" + fridays[i] + "&endDate=" + sundays[i] +"\n"

        sites = []
        sitelist = ""
    # if string != "":
    #     if int(time.strftime('%H')) == 0 or int(time.strftime('%H')) >= 6:   # 새벽시간 알림 차단
    #         chat.sendMessage(chat_id = chat_id, text=string)
        string = ""


### 땡큐캠핑예약 ###
dicCamp = {'1890':'블리스'}
#dicCamp = {'1578':'인제캠핑타운', '3638':'캠프인디오', '2208':'캠핑브릿지', '1800':'에버힐'}
for k in dicCamp.keys():
    # url = "https://m.thankqcamping.com/resv/view.hbb?cseq="+k
    # driver.get(url)
    # driver.find_element_by_css_selector("button[type=button]").click()
    # time.sleep(1)
    # driver.switch_to.window(driver.window_handles[1])

    for i in range(0,len(fridays)):
        try:
            url = "https://r.camperstory.com/resMain.hbb?campseq="+k+"&res_dt="+fridays[i].replace("-","")+"&res_edt="+sundays[i].replace("-","")+"&ser_res_days=2"
            #url = "https://r.camperstory.com/resMain.hbb?#"+fridays[i].replace("-","")+"^"+sundays[i].replace("-","")+"^2"
            #driver.get(url)
            driver.get(url)

            # 공지사항 팝업 레이어 뜨는경우, 닫기
            pop = driver.find_element_by_class_name("dim_layer")
            if pop.get_attribute("style") != "":
                driver.find_element_by_class_name("btn_layerClose").click()

            time.sleep(1)

            siteNames = driver.find_elements_by_css_selector(".site_info > .name")
            siteStatus = driver.find_elements_by_css_selector(".site_info > .res_num")
            for j in range(0, len(siteNames)):
                if siteStatus[j].text.find("예약완료") > -1 or siteStatus[j].text.find("예약불가") > -1:
                    continue
                else:
                    if k == '1761':             # 나린오토캠핑 선호 SITE
                        if siteNames[j].text == "해지개프리미엄데크":
                            sites.append(siteNames[j].text + " " + siteStatus[j].text.replace("예약가능", ""))
                    #elif k == '1578' and siteNames[j].text.find("오토구역") > -1:           # 인제캠핑타운 제외 SITE
                    #    continue
                    elif k == '1890':           # 블리스 선호 SITE
                        if siteNames[j].text.find("MV사이트") > -1:
                           sites.append(siteNames[j].text + " " + siteStatus[j].text.replace("예약가능", ""))
                    elif k == '2067':           # 에코유 선호 SITE
                        if siteNames[j].text.find("G사이트") > -1 or siteNames[j].text.find("H사이트") > -1:
                           sites.append(siteNames[j].text + " " + siteStatus[j].text.replace("예약가능", ""))
                    elif k == '2526':           # 양평수목원 제외 SITE
                        if siteNames[j].text.find("데크") > -1 or siteNames[j].text.find("카라반") > -1:
                            continue
                        else:
                            sites.append(siteNames[j].text + " " + siteStatus[j].text.replace("예약가능", ""))
                    elif siteNames[j].text.find("펜션") > -1 or siteNames[j].text.find("캠핑카") > -1 or siteNames[j].text.find("방가로") > -1 or siteNames[j].text.find("커플") > -1 or siteNames[j].text.find("하우스") > -1 or siteNames[j].text.find("캠프닉") > -1 or siteNames[j].text.find("글램핑") > -1 or siteNames[j].text.find("카라반") > -1 or siteNames[j].text.find("세미존") > -1:
                        continue
                    else:
                        sites.append(siteNames[j].text + " " + siteStatus[j].text.replace("예약가능", ""))

            if len(sites) == 0:
                sitelist = ""
                result = "X"
            #elif len(sites) >= 1 and len(sites) <=5:
            else:
                sitelist = str(sites)
                result = "O"
            #elif len(sites) > 5:
                #sitelist = "예약가능 사이트수 : " + str(len(sites)) + "건"

            print(dicCamp[k] + " / " + fridays[i] + " ~ " + sundays[i] + " : " + result + (" - " if len(sites) > 0 else "") + sitelist)
            if result == "O":
                string += dicCamp[k] + " / " + fridays[i] + " ~ " + sundays[i] + "\n " + sitelist + "\n" + "https://r.camperstory.com/resMain.hbb?campseq="+k+"&res_dt="+fridays[i].replace("-","")+"&res_edt="+sundays[i].replace("-","")+"&ser_res_days=2\n"

            sites = []
            sitelist = ""
        except Exception as error:
            print(error)
            break

    #if string != "":
        #if int(time.strftime('%H')) == 0 or int(time.strftime('%H')) >= 6:   # 새벽시간 알림 차단
            #chat.sendMessage(chat_id = chat_id, text=string)
        #string = ""



#### 장호비치 ####
# string = "장호비치\n"
# url = "https://forest.maketicket.co.kr/ticket/GD41"
# ableCnt = 0
# driver.get(url)
# driver.switch_to.window(driver.window_handles[0])

# # 이번달
# rMonth = driver.find_element_by_css_selector("caption").text
# rDate = datetime.strptime(rMonth+".01", "%Y. %m.%d")
# days = driver.find_elements_by_css_selector("td[id^=calendar]>strong")
# finds = driver.find_elements_by_css_selector(".s3 span")
# for i in range(0, len(days)):
#     if finds[i].text != "0":
#         rDate = rDate.replace(day = int(days[i].text))
#         day = rDate.weekday()
#         print(rDate.strftime("%m-%d") + "(" + t[day] + ") : 오토캠핑 " + finds[i].text + "개")
#         if t[day] in ['금', '토']:
#             ableCnt+=1
#             string += rDate.strftime("%m-%d") + "(" + t[day] + ") : 오토캠핑 " + finds[i].text + "개\n"

# # 다음달
# driver.find_element_by_css_selector(".nextmonth").click()
# time.sleep(1)
# rMonth = driver.find_element_by_css_selector("caption").text
# rDate = datetime.strptime(rMonth+".01", "%Y. %m.%d")
# days = driver.find_elements_by_css_selector("td[id^=calendar]>strong")
# finds = driver.find_elements_by_css_selector(".s3 span")
# for i in range(0, len(days)):
#     if finds[i].text != "0":
#         rDate = rDate.replace(day = int(days[i].text))
#         day = rDate.weekday()
#         print(rDate.strftime("%m-%d") + "(" + t[day] + ") : 오토캠핑 " + finds[i].text + "개")
#         if t[day] in ['금', '토']:
#             ableCnt+=1
#             string += rDate.strftime("%m-%d") + "(" + t[day] + ") : 오토캠핑 " + finds[i].text + "개\n"

# string += url
# if ableCnt > 0:
#     if int(time.strftime('%H')) == 0 or int(time.strftime('%H')) >= 6:   # 새벽시간 알림 차단
#         chat.sendMessage(chat_id = chat_id, text=string)



#### 캠프운악 ####
campName = "캠프운악"
string = ""
driver.get("https://www.campunak.co.kr/login.aspx")
driver.find_element_by_id("ContentMain_txtUserID").send_keys("baezzaes@naver.com")
driver.find_element_by_id("ContentMain_txtUserPW").send_keys("bjs0321")
driver.find_element_by_id("ContentMain_btnMemberLogin").click()
for i in range(0,len(fridays)):
    url = "https://www.campunak.co.kr/Reservation2/Reservation_Site.aspx?sdate=" + fridays[i] + "&edate=" + sundays[i]
    #url = "https://www.campunak.co.kr/Reservation2/Reservation_Site.aspx?sdate=2021-08-13&edate=2021-08-14"
    ableCnt = 0
    driver.get(url)
    driver.find_element_by_id("ContentMain_btnSearch").click()
    time.sleep(1)
    try:
        findSites = driver.find_elements_by_css_selector(".site_choice .payamount")
        findAbles = driver.find_elements_by_css_selector(".site_choice .none")
        for j in range(0, len(findSites)):
            if findAbles[j].text == "선택가능":
                sites.append(findSites[j].text)
                #print(findSites[i].text)
                result = "O"
        if len(sites) == 0:
            sitelist = ""
            result = "X"
        elif len(sites) >= 1 and len(sites) <=10:
            sitelist = str(sites)
        elif len(sites) > 10:
            sitelist = "예약가능 사이트수 : " + str(len(sites)) + "건"

        print(campName + " / " + fridays[i] + " ~ " + sundays[i] + " : " + result + (" - " if len(sites) > 0 else "") + sitelist)
        if result == "O":
            string += campName + " / " + fridays[i] + " ~ " + sundays[i] + "\n " + sitelist + "\n" + "https://www.campunak.co.kr/Reservation2/Reservation_Site.aspx?sdate=" + fridays[i] + "&eDate=" + sundays[i] +"\n"

        sites = []
        sitelist = ""
    except Exception as error:
        print(error)
        break

if string != "":
    if int(time.strftime('%H')) == 0 or int(time.strftime('%H')) >= 6:   # 새벽시간 알림 차단
        chat.sendMessage(chat_id = chat_id, text=string)
    string = ""




### 연천재인폭포오토캠핑장 ###
# campName = "연천재인폭포오토캠핑장"
# string = ""
# ableCnt = 0
# rYear = date.today().year
# rMonth = date.today().month
# for k in range(0, 3):
#     if rMonth == 13:
#         rYear = rYear + 1
#         rMonth = 1
#     for j in range(20, 25):
#         if j == 20:
#             siteArea = "오토캠핑 A1 ~ A20"
#         elif j == 21:
#             siteArea = "오토캠핑 A21 ~ A40"
#         elif j == 22:
#             siteArea = "오토캠핑 A41 ~ A60"
#         elif j == 23:
#             siteArea = "오토캠핑 A61 ~ A78"
#         elif j == 24:
#             siteArea = "오토캠핑 A89 ~ A100"
#         tmpString = ""
#         ableCnt = 0
#         url = "http://www.namastte.kr/popup.php?m="+str(rMonth)+"&Y="+str(rYear)+"&s=step01&searchRoomTy="+str(j)+"&t=resve&innb=5b7d0fe8da05f5b7d0fe8da0a1"
#         driver.get(url)
#         #finds = driver.find_elements_by_css_selector(".icon_standby")
#         finds = driver.find_elements_by_css_selector(".icon_possible")
#         rDate = datetime.strptime(str(rYear) + ". " + str(rMonth).zfill(2)+".01", "%Y. %m.%d")
#         for i in range(1, len(finds)):
#             day = finds[i].find_element_by_xpath('..').get_attribute("data-date")
#             rDate = rDate.replace(day = int(day))
#             weekday = rDate.weekday()
#             if t[weekday] == '토':
#                 ableCnt+=1
#                 print(rDate.strftime("%m-%d") + "(" + t[weekday] + ") : " + finds[i].text)
#                 tmpString += rDate.strftime("%m-%d") + "(" + t[weekday] + ") : " + finds[i].text + "\n"
#         if ableCnt > 0:
#             if ableCnt >= 10:
#                 string += str(rMonth) + "월 " + siteArea + " 예약가능 10건 이상\n" + url + "\n"
#             else:
#                 string += tmpString + url + "\n"

#     rMonth = rMonth + 1

# if string != "":
#     string = campName + "\n" + string
#     if int(time.strftime('%H')) == 0 or int(time.strftime('%H')) >= 6:   # 새벽시간 알림 차단
#         chat.sendMessage(chat_id = chat_id, text=string)

driver.quit()
