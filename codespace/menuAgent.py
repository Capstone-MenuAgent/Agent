from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import os
from dotenv import load_dotenv

from getWeather import getWeatherFore

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

template = """
    사용하는 언어는 한국어로 해줘.
    너는 사용자의 식사 메뉴를 추천해줘야해.
    답변 시 식사 메뉴 후보는 1개만 정해서 알려줘.

    사용자 나이 : {age},
    사용자 성별 : {gender},
    현재 날씨   : {weather}

    답변 양식은 아래와 같아.
    [AI] : 
"""

prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", "{question}"),
    ])
model = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.1, api_key=OPENAI_API_KEY)

# prototype : check code
menuBotChain = prompt | model | StrOutputParser()

def menuRecomment(question):
    return menuBotChain.invoke(
            {"question": question,
            "age": 25,
            "gender": "남성",
            "weather": getWeatherFore()
            })