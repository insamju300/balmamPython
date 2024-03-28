from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import json


    
driver = webdriver.Chrome()


driver.get("https://flight.naver.com/flights/international/SEL-KIX-20240426/KIX-SEL-20240428")
driver.maximize_window()
##로딩 프로그레스바가 나타날때까지 기다리고, 다시 로딩 프로그레스바가 사라질때까지 기다린다.
WebDriverWait(driver, 30).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.loadingProgress_loadingProgress__1LRJo'))
)
WebDriverWait(driver, 50).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loadingProgress_loadingProgress__1LRJo")))
# driver.implicitly_wait(50)
flightConatiners = driver.find_elements(By.CSS_SELECTOR, '.concurrent_ConcurrentItemContainer__2lQVG')
flightInfoList = []

for index, flightConatiner in enumerate(flightConatiners):
    
    routes = flightConatiner.find_elements(By.CSS_SELECTOR, ".route_Route__2UInh")
    departureRouteAirforts = routes[0].find_elements(By.CSS_SELECTOR, ".route_airport__3VT7M")
    departureFromTime=departureRouteAirforts[0].find_element(By.CSS_SELECTOR, ".route_time__-2Z1T").text
    departureFromAirport=departureRouteAirforts[0].find_element(By.CSS_SELECTOR, ".route_code__3WUFO").text
    departureToTime=departureRouteAirforts[1].find_element(By.CSS_SELECTOR, ".route_time__-2Z1T").text
    departureToAirport=departureRouteAirforts[1].find_element(By.CSS_SELECTOR, ".route_code__3WUFO").text
    departureToAirport=departureRouteAirforts[1].find_element(By.CSS_SELECTOR, ".route_code__3WUFO").text
    departureRouteInfo = routes[0].find_element(By.CSS_SELECTOR, ".route_info__1RhUH").text
    
    returnRouteAirforts = routes[1].find_elements(By.CSS_SELECTOR, ".route_airport__3VT7M")
    returnFromTime=returnRouteAirforts[0].find_element(By.CSS_SELECTOR, ".route_time__-2Z1T").text
    returnFromAirport=returnRouteAirforts[0].find_element(By.CSS_SELECTOR, ".route_code__3WUFO").text
    returnToTime=returnRouteAirforts[1].find_element(By.CSS_SELECTOR, ".route_time__-2Z1T").text
    returnToAirport=returnRouteAirforts[1].find_element(By.CSS_SELECTOR, ".route_code__3WUFO").text 
    returnRouteInfo = routes[1].find_element(By.CSS_SELECTOR, ".route_info__1RhUH").text
    
    airlines = flightConatiner.find_elements(By.CSS_SELECTOR, ".item_ItemHeader__3G-Hu")
    
    paymentMethod = flightConatiner.find_element(By.CSS_SELECTOR,".item_type__2KJOZ").text
    
    payCheck = flightConatiner.find_elements(By.CSS_SELECTOR,".item_promoted__2eSDk")
    if(len(payCheck)==0):
        payCheck = flightConatiner.find_elements(By.CSS_SELECTOR,".item_usual__dZqAN")
    pay=payCheck[0].text
     
#    item_usual__dZqAN
    
    departureAirline=""
    returnAirLine=""
    
    if(len(airlines)==1):
        departureAirline = airlines[0].find_element(By.CSS_SELECTOR, ".airline_name__Tm2wJ").text
        returnAirLine = airlines[0].find_element(By.CSS_SELECTOR, ".airline_name__Tm2wJ").text
    else:
        departureAirline = airlines[0].find_element(By.CSS_SELECTOR, ".airline_name__Tm2wJ").text
        returnAirLine = airlines[1].find_element(By.CSS_SELECTOR, ".airline_name__Tm2wJ").text
    
    flightInfo = {}
    flightInfo['index'] = index
    flightInfo['departureAirline'] = departureAirline
    flightInfo['departureFromTime'] = departureFromTime
    flightInfo['departureFromAirport'] = departureFromAirport
    flightInfo['departureToTime'] = departureToTime
    flightInfo['departureToAirport'] = departureToAirport
    flightInfo['departureRouteInfo'] = departureRouteInfo
    flightInfo['returnAirLine'] = returnAirLine
    flightInfo['returnFromTime'] = returnFromTime
    flightInfo['returnFromAirport'] = returnFromAirport
    flightInfo['returnToTime'] = returnFromAirport
    flightInfo['returnToAirport'] = returnFromAirport
    flightInfo['returnRouteInfo'] = returnFromAirport
    flightInfo['paymentMethod'] = paymentMethod
    flightInfo['returnFromAirport'] = returnFromAirport
    print(flightInfo)
    flightInfoList.append(flightInfo)
    
resultData={}
resultData["flightInfoList"] = flightInfoList
resultData['resultCode'] = 'S-1'
resultData['message'] = 'Success'
jsonString = json.dumps(resultData, ensure_ascii=False, indent=4)   
print(jsonString)
    

    

    
    


# driver.back()

# for flatConatiner in flatConatiners:
#     flatConatiner.click()
#     sleep(0.5)
#     flatConatiner.click()
#     sleep(0.5)
    
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.item_anchor__2CGzx'))
    # )
    # flatConatiner.find_element(By.CSS_SELECTOR, ".item_anchor__2CGzx").click()
    # driver.implicitly_wait(10)
    # urls.append(driver.current_url)
    # driver.back()
    


# airportCords=[]

# for dropdownButton in dropdownButtons:
#     if(dropdownButton.text=="국내"):
#         dropdownButton.click()

# WebDriverWait(driver, 10).until(
#     EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.autocomplete_Airport__3_dRP'))
# )    

# airportContainers = driver.find_elements(By.CSS_SELECTOR, '.autocomplete_Airport__3_dRP')
        
# for airportContainer in airportContainers:
#     cityAndCountry =  airportContainer.find_element(By.CSS_SELECTOR, ".autocomplete_location__TDL6g").text.split(",")
#     city = cityAndCountry[0]
#     country = cityAndCountry[1]
#     code = airportContainer.find_element(By.CSS_SELECTOR, ".autocomplete_code__i9Scs").text
#     airport = NaverAirport(city, country, code, 1)
#     airportCords.append(airport)
            


# driver.find_element(By.CSS_SELECTOR, '.searchBox_tablist__1uWMk').click()
# driver.find_element(By.CSS_SELECTOR, '.main_searchbox__3vrV3 .select_City__2NOOZ.end').click()
# WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.autocomplete_content__3RhAZ .autocomplete_Collapse__tP3pM')))
# dropdownButtons = driver.find_elements(By.CSS_SELECTOR, '.autocomplete_content__3RhAZ .autocomplete_Collapse__tP3pM')


# for dropdownButton in dropdownButtons:
#     if(dropdownButton.text!="국내"):
#         dropdownButton.click()

# WebDriverWait(driver, 10).until(
#     EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.autocomplete_Airport__3_dRP'))
# )
# airportContainers = driver.find_elements(By.CSS_SELECTOR, '.autocomplete_Airport__3_dRP')
        
# for airportContainer in airportContainers:
#     cityAndCountry =  airportContainer.find_element(By.CSS_SELECTOR, ".autocomplete_location__TDL6g").text.split(",")
#     city = cityAndCountry[0]
#     country = cityAndCountry[1]
#     code = airportContainer.find_element(By.CSS_SELECTOR, ".autocomplete_code__i9Scs").text
#     airport = NaverAirport(city, country, code, 0)
#     airportCords.append(airport)


# if airportCords:
#     try :
#         #데이터베이스에 연결
#         con = pymysql.connect(host= 'localhost', port = 3306, user = 'root', passwd = '', db = 'Balmam', charset = 'utf8')
#         cursor = con.cursor()
        
#         ## 1. 현재 버전중 가장 높은 값을 가져온다. 없으면 0
#         selectSql = "SELECT IFNULL(MAX(`VERSION`),0) FROM NaverAirport"
#         cursor.execute(selectSql)
#         result = cursor.fetchone()
#         version = result[0] + 1

        
        
#         ## 2. 버전값을 하나 올린 후 for문 돌려가며 객체를 저장한다.
#         insertSql = "INSERT INTO NaverAirport(city, country, code, version, isDeparture) VALUES(%s, %s, %s, %s, %s)"
#         insertList = []
        
#         for airportCord in airportCords:
#             insertList.append((airportCord.city, airportCord.country, airportCord.code, str(version), str(airportCord.isDeparture)))
            

#         cursor.executemany(insertSql, insertList)
#         con.commit()
#     except :
#         print("예외 발생", sys.exc_info())
#     finally :
#         if con != None :
#             con.close()
        


## 2. insert 작업을 한다.


   
   
# for airportCord in airportCords:
#     print(airportCord)

####날짜 관련 처리

## 네이버에서 날짜는 현재 날짜의 다음날 부터 1년후 오늘 까지에서 선택할 수 있다. 동일하게 처리할 것.


# driver.find_element(By.CSS_SELECTOR, '.searchBox_tablist__1uWMk').click()
# driver.find_element(By.CSS_SELECTOR, '.tabContent_option__2y4c6.select_Date__1aF7Y:last-child').click()




# WebDriverWait(driver, 10).until(
#     EC.presence_of_all_elements_located((By.CLASS_NAME, 'month'))
# )    


# months = driver.find_elements(By.CLASS_NAME, 'month')
# lastMonth = months[-1]

# yearAndMonth=lastMonth.find_element(By.CSS_SELECTOR, '.sc-iqcoie.dCaTmH').text.split(".")
# year=int(yearAndMonth[0])
# month=int(yearAndMonth[1])
# print(year)
# print(month)

# days=lastMonth.find_elements(By.CSS_SELECTOR, '.day:not(.invalid)')
# print(len(days))
# lastDay = days[-1]
# print(lastDay.get_attribute("outerHTML"))



    



#네이버에서 지원하는 공항 목록 가져오기

##할 일.
## 1. 공항 목록 더 깔끔하게 객체처럼 정리하기. 도시, 국가, 코드 세개 들고 올 것. ㅇ
## 2. 현재 선택할 수 있는 마지막 날짜 들고 올 것.  -> 크롤링 불가. 네이버는 현재날짜 다음날부터 1년까지 선택가능이므로 동일한 사양으로 할 것.
## 3. 해당 두가지 데이터를 DB에 보관할 것(들고와서 검색하게 된다.) 크롤링 버전이라는 db를 추가하고 최신 갱신일을 넣은 후에, 해당 version id city country code is_departure을 db에보관한다.
##    버전에는 ok 코드를 추가한다.
## 4. main.py에 출발공항, 도착공항, 출발일, 도착일을 파라미터로 받으면, 스크롤 다운하며 긁어온 모든 데이터를 객체화해서 JSON으로 바꿔서 반환해주는 url을 추가한다.
## 5. 검색어와 index를 인자로 받아서, 클릭하면 성인 모든 결제수단 링크를 반환하는 url을 만든다.
## 6. 해당 기능을 랭체인과 연결 하여 java코드 작성
## 7. 1~3까지의 작업을 스케쥴링 처리할 수 있게 할 것.


driver.close()

##공항 

# assert "Python" in driver.title
# elem = driver.find_element(By.NAME, "q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()