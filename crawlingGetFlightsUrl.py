from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

    
driver = webdriver.Chrome()

driver.get("https://flight.naver.com/flights/international/SEL-KIX-20240426/KIX-SEL-20240428")
driver.maximize_window()
WebDriverWait(driver, 30).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.loadingProgress_loadingProgress__1LRJo'))
)
WebDriverWait(driver, 50).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loadingProgress_loadingProgress__1LRJo")))


flatConatiners = driver.find_elements(By.CSS_SELECTOR, '.concurrent_select_schedule__3O1pT')
index = 105

flatConatiners[index].click()
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '.item_detail__2jkvn .item_anchor__2CGzx'))
)
driver.find_element(By.CSS_SELECTOR, ".item_detail__2jkvn .item_anchor__2CGzx").click()
print(driver.current_url)