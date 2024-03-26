from typing import Union
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

import sys
import io
import os

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

from typing import List
from datetime import datetime



app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    
@app.get("/travelPlan/createPlan")
async def createPlan(
    enterDate: str, 
    enterAirplane: str, 
    removeDate: str, 
    removeAirplane: str, 
    keywords: List[str] = Query(None)  # 쿼리 매개변수로 여러 값을 받기 위해 List 사용
):
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')


    load_dotenv()

    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )


    template = """너는 30년 경력 배태랑의 여행 플래너야.
    넌 지금부터 손님이 패키지를 통하지 않고 직접 여행하기 위한 플랜을 짜줘야해.
    손님은 {enterDate}에 {enterAirplane}에 도착할 예정이야.
    그리고 {removeAirplane}에서 {removeDate}에 출발할 예정이야.
    다음 키워드들을 관련지어서 여행 플랜을 짜줘.
    [{keywords}]
    여행 경로를 30분 간격으로 상세하게 짜주되, 다음 포맷에 맞춰서 짜줘.
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
        lat: str = Field(description="해당 장소의 위도")
        lng: str = Field(description="해당 장소의 경도")
        description: str = Field(description="해당 장소에 대한 설명")

    class TravelPlans(BaseModel):
        plan: TravelPlan = Field(description="시간, 위치, 설명으로 이루어진 하나의 여행 계획 단위")



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
    resultData = chain.invoke({"enterDate": enterDate, "enterAirplane": enterAirplane, "removeDate": removeDate, 
                        "removeAirplane": removeAirplane, "keywords": keywords})

    resultData['resultCode'] = 'S-1'
    resultData['message'] = 'Success'
    
    return resultData
