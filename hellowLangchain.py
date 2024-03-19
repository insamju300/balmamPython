# -*- coding: utf-8 -*-
from dotenv import load_dotenv
import os
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate.from_template(template)

# # 객체 생성
# llm = ChatOpenAI(temperature=0,               # 창의성 (0.0 ~ 2.0) 
#                  max_tokens=2048,             # 최대 토큰수
#                  model_name='gpt-3.5-turbo',  # 모델명
#                 )

# # 질의내용
# question = '대한민국의 수도는 뭐야?'

# # 질의
# print(f'[답변]: {llm.predict(question)}')