from selenium import webdriver
import datetime
from datetime import date
import time
import telegram

# Telegram Setting
chat = telegram.Bot(token = "1824090062:AAGCxw7oRV_RpC9kWrt8DN4fblurkzpnRn4")
chat_id = "-1001512203758"
# text = "Hi"
# chat.sendMessage(chat_id = chat_id, text=text)
# quit()

# webdriver chrome 옵션
options = webdriver.ChromeOptions()
options.add_argument('headless')        # 웹 브라우저를 띄우지 않는 headless chrome 옵션
options.add_argument('disable-gpu')     # GPU 사용 안함
options.add_argument('lang=ko_KR')      # 언어 설정

# 상수

dicCamp = {'481805':'돌고래', '14972':'마리원', '163771':'아라뜰', '164989':'물왕숲', '278756':'대부도비치', '59772':'아버지의숲', '160759':'마장호수휴'}

# 주말 체크
chkday = date.today()
fridays = []
sundays = []
weekNo = 0
while True:
    if chkday.weekday() == 4:
        fridays.append(str(chkday))
        sundays.append(str(chkday + datetime.timedelta(days=2)))
        weekNo+=1
        if weekNo == 12:
            break
    chkday = chkday + datetime.timedelta(days=1)


driver = webdriver.Chrome("./chromedriver", options=options)
#driver.get("https://m.booking.naver.com/booking/3/bizes/481805/items?startDate=2021-07-30&endDate=2021-08-01")
driver.implicitly_wait(3)
# try:
#     driver.find_element_by_class_name("summary_body")
# except Exception as error:
#     print(error)

# quit()

string = ""
for k in dicCamp.keys():
    for i in range(0,len(fridays) - 1):
        driver.get("https://m.booking.naver.com/booking/3/bizes/"+ k +"/items?startDate=" + fridays[i] + "&endDate=" + sundays[i])

        try:
            find = driver.find_element_by_class_name("result_txt")
            #print(find)
            result = "X"
        except Exception as error:
            #print(error)
            result = "O"

        print(dicCamp[k] + " / " + fridays[i] + " ~ " + sundays[i] + " : " + result)
        if result == "O":
            string += dicCamp[k] + " / " + fridays[i] + " ~ " + sundays[i] + " / " + "https://m.booking.naver.com/booking/3/bizes/"+ k +"/items?startDate=" + fridays[i] + "&endDate=" + sundays[i] +"\n"

    if string != "":
        chat.sendMessage(chat_id = chat_id, text=string)
        string = ""

