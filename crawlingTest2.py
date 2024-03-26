from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

driver = webdriver.Chrome()
driver.get("https://flight.naver.com/")
sleep(10)
driver.find_element(By.CSS_SELECTOR, '.main_searchbox__3vrV3 .select_City__2NOOZ.start').click()

sleep(3)

dropdownButtons = driver.find_elements(By.CSS_SELECTOR, '.autocomplete_content__3RhAZ .autocomplete_Collapse__tP3pM')

fromAirportCords=[]

for dropdownButton in dropdownButtons:
    if(dropdownButton.text=="국내"):
        dropdownButton.click()
        sleep(3)
        airfortSpans = driver.find_elements(By.CSS_SELECTOR, '.autocomplete_Airport__3_dRP .autocomplete_code__i9Scs')
        for airfortSpan in airfortSpans:
            fromAirportCords.append(airfortSpan.text)
        
#국내의 출발가능 공항 코드 리스트
print(fromAirportCords)


driver.find_element(By.CSS_SELECTOR, '.searchBox_tablist__1uWMk').click()
sleep(3)
driver.find_element(By.CSS_SELECTOR, '.main_searchbox__3vrV3 .select_City__2NOOZ.end').click()
sleep(3)
dropdownButtons = driver.find_elements(By.CSS_SELECTOR, '.autocomplete_content__3RhAZ .autocomplete_Collapse__tP3pM')

toAirportCords=[]

for dropdownButton in dropdownButtons:
    if(dropdownButton.text!="국내"):
        dropdownButton.click()
        sleep(3)
airfortSpans = driver.find_elements(By.CSS_SELECTOR, '.autocomplete_Airport__3_dRP .autocomplete_code__i9Scs')
for airfortSpan in airfortSpans:
    toAirportCords.append(airfortSpan.text)

print(toAirportCords)
##네이버에서 지원하는 공항 목록 가져오기

##할 일.
## 1. 공항 목록 더 깔끔하게 객체처럼 정리하기. 도시, 국가, 코드 세개 들고 올 것.
## 2. 현재 선택할 수 있는 마지막 날짜 들고 올 것. 
## 3. 해당 두가지 데이터를 DB에 보관할 것(들고와서 검색하게 된다.)
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