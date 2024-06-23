from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import os
from dotenv import load_dotenv

from weather import getWeatherFore
from restaurant import getRestaurant

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

template = """
    [System]
    사용하는 언어는 한국어로 해줘.
    너는 사용자의 식사 메뉴를 추천해줘야해.
    답변 시 식사 메뉴 후보는 1개만 정해서 알려줘.

    [Data]
    사용자 나이 : {age},
    사용자 성별 : {gender},
    현재 날씨   : {weather},
    주변 음식점 : {restaurants}

    [Response]
    가능하면 의미가 전달되는 선에서 문장을 짧게 해줘.
    음식점 이름과 추천 메뉴를 알려줘.
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

def menuRecomment(question, age, gender, loc):
    return menuBotChain.invoke(
            {"question": question,
            "age": age,
            "gender": gender,
            "weather": getWeatherFore(),
            "restaurants": getRestaurant(loc)
            })