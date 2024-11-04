from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.pydantic_v1 import Field
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain.chains import create_sql_query_chain
from pydantic import BaseModel

from datetime import datetime
import os
from dotenv import load_dotenv

from database.sqlSetting import Engine
from database.restaurantService import loadAllRestaurantAndMenu, loadRestaurantUrlById
from weather import getWeatherFore

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model='gpt-3.5-turbo', api_key=OPENAI_API_KEY)
engine = Engine().engine
db = SQLDatabase(engine=engine, include_tables=['restaurants', 'menu'])

class RecommendModel(BaseModel):
    answer: str = Field(description="answer")
    id: str = Field(description="id")

template = """
    [[System]
    사용하는 언어는 한국어로 해줘.
    너는 사용자의 식사 메뉴를 추천해줘야해.
    답변 시 식사 메뉴 후보는 1개만 정해서 알려줘.
    
    [Data]
    사용자 질문 : {query}
    사용자 나이 : {age},
    사용자 성별 : {gender},
    현재 날씨 : {weather},
    현재 시각 : {nowTime},
    음식점 데이터베이스 : {restaurantsData}

    [Return]
    {{
        "answer": "음식점과 메뉴를 추천하는 한 문장",
        "id": "음식점 ID"
    }}
"""

parser = JsonOutputParser(pydantic_object=RecommendModel)

prompt = PromptTemplate(
    template=template,
    input_variables=["query", "age", "gender", "weather", "nowTime", "restaurantsData"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | llm | parser

def menuRecomment(query, loc, age, gender):
    response = chain.invoke({
        "query": query,
        "age": age,
        "gender": gender,
        "weather": getWeatherFore(),  # Ensure this returns valid weather data.
        "nowTime": datetime.now().strftime('%m-%d %H:%M'),
        "restaurantsData": loadAllRestaurantAndMenu(loc)  # Ensure this returns valid restaurant data.
    })
    url = loadRestaurantUrlById(int(response['id']))
    result = {
        "answer": response['answer'],
        "mapUrl": url
    }
    return result