from selenium import webdriver
from datetime import date
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import telegram

# Telegram Setting
chat = telegram.Bot(token = "1824090062:AAF1UsFJ0-RShZS8Ulys6sOtRgqG10X7SNM")
chat_id = "-1001512203758"
#chat_id = "1510104965"
# text = "abcd"
# chat.sendMessage(chat_id = chat_id, text=text)
# quit()

# webdriver chrome 옵션
options = webdriver.ChromeOptions()
options.add_argument('headless')        # 웹 브라우저를 띄우지 않는 headless chrome 옵션
options.add_argument('disable-gpu')     # GPU 사용 안함
options.add_argument('lang=ko_KR')      # 언어 설정
options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 로그 숨김

driver = webdriver.Chrome("./chromedriver", options=options)
driver.implicitly_wait(3)

t = ['월', '화', '수', '목', '금', '토', '일']

# 주말 체크
chkday = date.today()
fridays = []
sundays = []
weekNo = 0
while True:
    if chkday.weekday() == 4:
        fridays.append(str(chkday))
        sundays.append(str(chkday + timedelta(days=2)))
        # 2021 추석연휴
        if str(chkday) == "2021-09-17":
            fridays.append(str("2021-09-18"))
            sundays.append(str("2021-09-20"))
        # 2021 개천절 대체공휴일
        elif str(chkday) == "2021-10-01":
            fridays.append(str("2021-10-02"))
            sundays.append(str("2021-10-04"))
        # 2021 한글날 대체공휴일
        elif str(chkday) == "2021-10-08":
            fridays.append(str("2021-10-09"))
            sundays.append(str("2021-10-11"))
        weekNo+=1
        if weekNo == 12:
            break
    chkday = chkday + timedelta(days=1)

#driver.get("https://m.booking.naver.com/booking/3/bizes/481805/items?startDate=2021-07-30&endDate=2021-08-01")

# try:
#     driver.find_element_by_class_name("summary_body")
# except Exception as error:
#     print(error)

# quit()


sites = []
sitelist = ""
string = ""

#### 네이버예약 ####
dicCamp = {'59772':'아버지의숲', '481805':'돌고래', '14972':'마리원', '163771':'아라뜰', '278756':'대부도비치',   '1142':'캄파슬로우', '100853':'두리캠핑', '83676':'서종힐링', '394663':'답게', '160905':'리프레쉬'}
#dicCamp = {'164989':'물왕숲', '160759':'마장호수휴', '557521':'캠핑느루'}

for k in dicCamp.keys():
    for i in range(0,len(fridays)):
        driver.get("https://m.booking.naver.com/booking/3/bizes/"+ k +"/items?startDate=" + fridays[i] + "&endDate=" + sundays[i])

        try:
            find = driver.find_element_by_class_name("result_txt")
            #print(find)
            result = "X"
        except Exception as error:
            #print(error)
            result = "O"
            finds = driver.find_elements_by_css_selector(".summary_body .desc_title")
            for j in finds:
                if j.text == "카라반 CARAVAN" or j.text == "캠프렛 CAMPLET" or j.text == "차박&루프탑&파쇄석 존":       # 물왕숲 제외 SITE
                    continue
                elif k == '278756' and (j.text.find("캠핑 B") > -1 or j.text.find("캠핑 C") > -1 or j.text.find("캠핑 D") > -1):     # 대부도비치 제외 SITE
                    continue
                elif k == '299264' and (j.text.find("Hill") > -1 or j.text.find("Pond") > -1):     # 해여림빌리지 제외 SITE
                    continue
                elif k == '14972' and (j.text.find("숲 14") > -1 or j.text.find("숲 15") > -1 or j.text.find("숲 16") > -1):    # 마리원 제외 SITE
                    continue
                elif k == '481805' and j.text.find("소나무") > -1:        # 돌고래 제외 SITE
                    continue
                elif j.text.find("펜션") > -1 or j.text.find("방가로") > -1 or j.text.find("커플") > -1 or j.text.find("하우스") > -1 or j.text.find("캠프닉") > -1 or j.text.find("단골전용") > -1 or j.text.find("글램핑") > -1:
                    continue
                else:
                    if k == '163771':       # 아라뜰 선호 SITE
                        if j.text.find("B7") > -1 or j.text.find("B8") > -1 or j.text.find("B9") > -1 or j.text.find("A23") > -1 or j.text.find("A17") > -1:
                            sites.append(j.text.replace("(2박 우선예약)", ""))
                        else:
                            continue

                    elif k == '83676':      # 서종힐링 선호 SITE
                        if j.text.find("A2") > -1 or j.text.find("A3") > -1 or j.text.find("A4") > -1 or j.text.find("A6") > -1 or j.text.find("A7") > -1 or j.text.find("A8") > -1:
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
    if string != "":
        if int(time.strftime('%H')) == 0 or int(time.strftime('%H')) >= 6:   # 새벽시간 알림 차단
            chat.sendMessage(chat_id = chat_id, text=string)
        string = ""


### 땡큐캠핑예약 ###
dicCamp = {'1578':'인제캠핑타운', '2067':'에코유', '1890':'블리스', '1761':'나린오토캠핑'}
#dicCamp = {'2208':'캠핑브릿지'}
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
                    elif k == '1578' and siteNames[j].text.find("오토구역") > -1:           # 인제캠핑타운 제외 SITE                        
                        continue
                    elif k == '1890':           # 블리스 선호 SITE
                        if siteNames[j].text.find("MV사이트") > -1:
                           sites.append(siteNames[j].text + " " + siteStatus[j].text.replace("예약가능", ""))
                    elif k == '2067':           # 에코유 선호 SITE
                        if siteNames[j].text.find("G사이트") > -1 or siteNames[j].text.find("H사이트") > -1:
                           sites.append(siteNames[j].text + " " + siteStatus[j].text.replace("예약가능", ""))
                    elif siteNames[j].text.find("펜션") > -1 or siteNames[j].text.find("캠핑카") > -1 or siteNames[j].text.find("방가로") > -1 or siteNames[j].text.find("커플") > -1 or siteNames[j].text.find("하우스") > -1 or siteNames[j].text.find("캠프닉") > -1 or siteNames[j].text.find("글램핑") > -1:
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

    if string != "":
        if int(time.strftime('%H')) == 0 or int(time.strftime('%H')) >= 6:   # 새벽시간 알림 차단
            chat.sendMessage(chat_id = chat_id, text=string)
        string = ""



#### 장호비치 ####
string = "장호비치\n"
url = "https://forest.maketicket.co.kr/ticket/GD41"
ableCnt = 0
driver.get(url)
driver.switch_to.window(driver.window_handles[0])

# 이번달
rMonth = driver.find_element_by_css_selector("caption").text
rDate = datetime.strptime(rMonth+".01", "%Y. %m.%d")
days = driver.find_elements_by_css_selector("td[id^=calendar]>strong")
finds = driver.find_elements_by_css_selector(".s3 span")
for i in range(0, len(days)):
    if finds[i].text != "0":
        ableCnt+=1
        rDate = rDate.replace(day = int(days[i].text))
        day = rDate.weekday()
        print(rDate.strftime("%m-%d") + "(" + t[day] + ") : 오토캠핑 " + finds[i].text + "개")
        string += rDate.strftime("%m-%d") + "(" + t[day] + ") : 오토캠핑 " + finds[i].text + "개\n"

# 다음달
driver.find_element_by_css_selector(".nextmonth").click()
time.sleep(1)
rMonth = driver.find_element_by_css_selector("caption").text
rDate = datetime.strptime(rMonth+".01", "%Y. %m.%d")
days = driver.find_elements_by_css_selector("td[id^=calendar]>strong")
finds = driver.find_elements_by_css_selector(".s3 span")
for i in range(0, len(days)):
    if finds[i].text != "0":
        ableCnt+=1
        rDate = rDate.replace(day = int(days[i].text))
        day = rDate.weekday()
        print(rDate.strftime("%m-%d") + "(" + t[day] + ") : 오토캠핑 " + finds[i].text + "개")
        string += rDate.strftime("%m-%d") + "(" + t[day] + ") : 오토캠핑 " + finds[i].text + "개\n"

string += url
if ableCnt > 0:
    if int(time.strftime('%H')) == 0 or int(time.strftime('%H')) >= 6:   # 새벽시간 알림 차단
        chat.sendMessage(chat_id = chat_id, text=string)



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




driver.quit()