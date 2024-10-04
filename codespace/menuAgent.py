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
    나이, 성별, 날씨를 고려해서 음식점 이름, 추천 메뉴, 주소를 알려줘.
    추천 메뉴는 음식점에서 한 가지만 정해서 알려줘.
    음식점 이름, 추천 메뉴는 " "로 묶어서 알려줘.
    답변은 세 줄 작성해줘.
    첫 줄은 하늘 상태와 기온에 대해 작성해줘.
    두 번째 줄은 "음식점 이름"의 "추천 메뉴"를 작성해줘.
    세 번째 줄은 주소 데이터만 작성해줘.
    아래는 예시야.
    하늘은 "하늘 상태" 기온은 "온도"입니다.
    "음식점 이름"의 "추천 메뉴"를 추천해드릴게요.
    "주소"
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