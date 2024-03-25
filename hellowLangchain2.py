import sys
import io
import os

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')


load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

template = """
너는 30년 경력 배태랑의 여행 플래너야.
넌 지금부터 손님이 패키지를 통하지 않고 직접 여행하기 위한 플랜을 짜줘야해.
나는 3월 30일 15시에 나리타 공항에 도착할 예정이야.
그리고 나리타 공항에서 3월 33일 16시에 출발할 예정이야.
이번 여행은 다음 키워드들과 관련지어서 가려고 생각중이야.
['동물원', '혼자 가는', '골목길']
식사와 호텔을 포함한 여행 경로를 30분 간격으로 상세하게 짜주되 다음 포맷에 맞춰서 짜줘.
식당과 호텔의 경우 즐길만한 식당과 호텔 이름도 전부 아래 포맷에 맞춰서 명시해줘.
잘하면 30만달러의 팁을 줄 거고 못하면 용광로에 녹일 거야.
답변은 반드시 한국어로만 해야해.

|시간|장소명|위도|경도|상세설명|

ex
|2024-03-30 21:00| 35.7161|39.7704|1882년에 문을 연 우에노 동물원은 일본에서 가장 오래된 동물원입니다|
"""


prompt = PromptTemplate.from_template(template)


# OpenAI 챗모델을 초기화합니다.
model = ChatOpenAI(model="gpt-4-turbo-preview")
# 문자열 출력 파서를 초기화합니다.
output_parser = StrOutputParser()

# 프롬프트, 모델, 출력 파서를 연결하여 처리 체인을 구성합니다.
chain = prompt | model | output_parser

# 완성된 Chain 을 이용하여 country 를 '대한민국'으로 설정하여 실행합니다.
# chain.invoke({"country": "대한민국"})
print(chain.invoke({"question": "저는 식당에 가서 음식을 주문하고 싶어요"}))

# https://www.data.go.kr/data/3051587/fileData.do 공항 이름 모음
# 참조 https://wikidocs.net/231233