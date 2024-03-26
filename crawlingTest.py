import requests
from bs4 import BeautifulSoup
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

url = 'https://flight.naver.com/'

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    print(soup)

else : 
    print(response.status_code)




#참조
#https://wikidocs.net/85739
#https://flight.naver.com/flights/international/SEL-TYO-20240327/TYO-SEL-20240527?adult=1&fareType=Y