from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import sys
import io
import os
import urllib.request

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

from typing import List
from datetime import datetime

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup



app = FastAPI()

# CORS middleware settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:8080",],  # Allow access from all domains
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)



@app.get("/test")
async def read_root():
    return "justTest"

# # datetime
# class PlanRequestDto(BaseModel):
#     enterDate: str
#     enterAirplane: str
#     removeDate: str
#     removeAirplane: str
#     keywords: List[str] = Query(None) 

##http://127.0.0.1:8000/travelPlan/createPlan?enterDate=2024-04-23&enterAirplane=GMP&removeDate=2024-04-25&removeAirplane=KIX
@app.get("/travelPlan/createPlan")
async def createPlan(
    enterDate: str, 
    targetAirplane: str, 
    removeDate: str, 
    keywords: List[str] = Query(None)  # 쿼리 매개변수로 여러 값을 받기 위해 List 사용
):
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')


    load_dotenv()

    print(os.environ.get("OPENAI_API_KEY"))

    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )


    template = """너는 30년 경력 배태랑의 여행 플래너야.
    넌 지금부터 손님이 패키지를 통하지 않고 직접 여행하기 위한 플랜을 짜줘야해.
    손님은 {enterDate}에 공항코드 ({targetAirplane})에 도착할 예정이야.
    그리고 공항코드 ({targetAirplane})에서 {removeDate}에 출발할 예정이야.
    해당 공항코드에 해당하는 공항 이름을 확인해서, 해당 공항 이름부터 출발해서 해당 공항이름에 도착하는 플랜을 짜줘.
    공항 명과 공항 도착 날짜, 공항 출발날짜가 가장 우선되야되.
    다음 키워드들을 관련지어서 여행 플랜을 짜줘.
    [{keywords}]
    여행 경로를 짧은 시간 간격으로 상세하게 짜주되, 다음 포맷에 맞춰서 짜줘.
    위도와 경도가 같은 동일한 위치에서 여러 작업이 시행될 경우 한줄안에서 표현해줘.
    식당과 호텔의 경우 즐길만한 식당과 호텔명도 전부 아래 포맷에 맞춰서 명시해줘.
    잘하면 30만달러의 팁을 줄 거고 못하면 용광로에 녹일 거야.
    답변은 반드시 한국어로만 해야해.

    FORMAT:
    {format_instructions}
    """


    class TravelPlan(BaseModel):
        date: str = Field(description="해당 장소에 방문할 날짜")
        time: str = Field(description="해당 장소에 방문할 시간")
        placeName: str = Field(description="해당 장소 명")
        description: str = Field(description="해당 장소에 대한 설명")

    class TravelPlans(BaseModel):
        plans: TravelPlan = Field(description="시간, 위치, 설명으로 이루어진 하나의 여행 계획 단위")



    # 문자열 출력 파서를 초기화합니다.
    parser = JsonOutputParser(pydantic_object=TravelPlans)

    prompt = PromptTemplate.from_template(template=template,
                                        partial_variables={
            "format_instructions": parser.get_format_instructions()},)

    # OpenAI 챗모델을 초기화합니다.
    model = ChatOpenAI(model="gpt-4-turbo-preview")




    # 프롬프트, 모델, 출력 파서를 연결하여 처리 체인을 구성합니다.
    chain = prompt | model | parser

    # 완성된 Chain 을 이용하여 country 를 '대한민국'으로 설정하여 실행합니다.
    # chain.invoke({"country": "대한민국"})
    resultGpt = chain.invoke({"enterDate": enterDate, "targetAirplane": targetAirplane, "removeDate": removeDate, 
                        "keywords": keywords})
    
    resultData={}

    client_id =  os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")

    for plan in resultGpt['plans']:
        encText = urllib.parse.quote(plan['placeName'])
        url = "https://openapi.naver.com/v1/search/image.xml?query=" + encText # XML 결과
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            body = response_body.decode('utf-8')
            soup = BeautifulSoup(body, "xml")
            item=soup.find("item")
            imageUrl = ""
            if item:
                foundLink = item.find("link")
                imageUrl=foundLink.text
            plan['imageUrl'] = imageUrl

        else:
            plan['imageUrl'] = ""    


    resultData['data1'] = resultGpt['plans']
    resultData['resultCode'] = 'S-1'
    resultData['message'] = 'Success'
    
    return JSONResponse(content=resultData)


@app.get("/travelPlan/crawlingFlightList")
async def crawlingFlightList(departureAirportCode, returnAirportCode, departureDay, returnDay):
    driver = webdriver.Chrome()
    url_template = "https://flight.naver.com/flights/international/{departureAirportCode}-{returnAirportCode}-{departureDay}/{returnAirportCode}-{departureAirportCode}-{returnDay}"
    final_url = url_template.format(departureAirportCode=departureAirportCode, returnAirportCode=returnAirportCode, departureDay=departureDay, returnDay=returnDay)
    driver.get(final_url)
    driver.maximize_window()
    ##로딩 프로그레스바가 나타날때까지 기다리고, 다시 로딩 프로그레스바가 사라질때까지 기다린다.
    try:
    
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.loadingProgress_loadingProgress__1LRJo'))
        )
        WebDriverWait(driver, 50).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loadingProgress_loadingProgress__1LRJo")))
    except Exception:
        pass

    try:

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
            flightInfo['returnToTime'] = returnToTime
            flightInfo['returnToAirport'] = returnToAirport
            flightInfo['returnRouteInfo'] = returnRouteInfo
            flightInfo['paymentMethod'] = paymentMethod
            flightInfo['pay'] = pay
            flightInfoList.append(flightInfo)

        driver.close()
      
        if flightInfoList is None or len(flightInfoList) == 0:
            resultData = {
                'resultCode': 'F-1',
                'message': '해당 날짜의 항공편이 존재하지 않습니다'
            }
            return JSONResponse(content=resultData)
        
            
        resultData={}
        resultData["flightInfoList"] = flightInfoList
        resultData['resultCode'] = 'S-1'
        resultData['message'] = 'Success'
        

        return JSONResponse(content=resultData)
    except Exception:
        resultData={}
        resultData['resultCode'] = 'F-1'
        resultData['message'] = '해당 날짜의 항공편이 존재하지 않습니다'
        driver.close()
        return JSONResponse(content=resultData)


@app.get("/travelPlan/getTicketingUrl")
async def getTicketingUrl(departureAirportCode, returnAirportCode, departureDay, returnDay, index):
    driver = webdriver.Chrome()
    url_template = "https://flight.naver.com/flights/international/{departureAirportCode}-{returnAirportCode}-{departureDay}/{returnAirportCode}-{departureAirportCode}-{returnDay}"
    final_url = url_template.format(departureAirportCode=departureAirportCode, returnAirportCode=returnAirportCode, departureDay=departureDay, returnDay=returnDay)
    driver.get(final_url)
    driver.maximize_window()
    ##로딩 프로그레스바가 나타날때까지 기다리고, 다시 로딩 프로그레스바가 사라질때까지 기다린다.
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.loadingProgress_loadingProgress__1LRJo'))
    )
    WebDriverWait(driver, 50).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loadingProgress_loadingProgress__1LRJo")))


    flatConatiners = driver.find_elements(By.CSS_SELECTOR, '.concurrent_select_schedule__3O1pT')

    flatConatiners[int(index)].click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.item_detail__2jkvn>div:first-child'))
    )
    driver.find_element(By.CSS_SELECTOR, ".item_detail__2jkvn>div:first-child").click()
    print(driver.current_url)         
    
        
    resultData={}
    resultData["url"] = driver.current_url
    resultData['resultCode'] = 'S-1'
    resultData['message'] = 'Success'
    
    driver.close()
    return JSONResponse(content=resultData)