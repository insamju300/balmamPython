from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

driver = webdriver.Chrome()
driver.get("https://flight.naver.com/flights/international/SEL-TYO-20241001/TYO-SEL-20250131")
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


driver.close()

##공항 

# adult=1&child=5&infant=1&
# 성인, 소아, 유아


# fareType 
# Y: 일반석
# P: 프리미엄 일반석
# C: 비즈니스석
# F:일등석
