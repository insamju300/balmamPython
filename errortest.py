# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# # INFO:     127.0.0.1:50134 - "GET /travelPlan/getTicketingUrl?departureAirportCode=CJU&returnAirportCode=OKA&departureDay=20240426&returnDay=20240429&index=1 HTTP/1.1" 500 Internal Server Error
# # ERROR:    Exception in ASGI application
# # 과제... 

# def getTicketingUrl(departureAirportCode, returnAirportCode, departureDay, returnDay, index):
#     driver = webdriver.Chrome()
#     url_template = "https://flight.naver.com/flights/international/{departureAirportCode}-{returnAirportCode}-{departureDay}/{returnAirportCode}-{departureAirportCode}-{returnDay}"
#     final_url = url_template.format(departureAirportCode=departureAirportCode, returnAirportCode=returnAirportCode, departureDay=departureDay, returnDay=returnDay)
#     driver.get(final_url)
#     driver.maximize_window()
#     ##로딩 프로그레스바가 나타날때까지 기다리고, 다시 로딩 프로그레스바가 사라질때까지 기다린다.
#     WebDriverWait(driver, 30).until(
#         EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.loadingProgress_loadingProgress__1LRJo'))
#     )
#     WebDriverWait(driver, 50).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loadingProgress_loadingProgress__1LRJo")))


#     flatConatiners = driver.find_elements(By.CSS_SELECTOR, '.concurrent_select_schedule__3O1pT')

#     flatConatiners[int(index)].click()
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, '.item_detail__2jkvn>div:first-child'))
#     )
#     driver.find_element(By.CSS_SELECTOR, ".item_detail__2jkvn>div:first-child").click()
#     print(driver.current_url)         
    
        
#     resultData={}
#     resultData["url"] = driver.current_url
#     resultData['resultCode'] = 'S-1'
#     resultData['message'] = 'Success'
    
#     driver.close()