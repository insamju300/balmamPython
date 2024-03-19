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
당신은 30년차 베테랑 여행상담원 입니다.
[FORMAT]에 맞추어 한글로 답변해 주세요.
손님은 {fromdDate}에 {fromAirplane}에 도착할 예정이고
{endDate}에 {endAirplane}에서 출발할 예정입니다.
손님꼐서는 다음 키워드와 연관된 여행을 하고 싶어하십니다.
[{keyword1}, {keyword2}, {keyword3}]
손님에게 

질문:
{question}에 대하여 설명해 주세요.

FORMAT:
- 개요:
- 예시:
- 출처:
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