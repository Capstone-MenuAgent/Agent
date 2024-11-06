from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.pydantic_v1 import Field
from langchain_community.utilities import SQLDatabase
from pydantic import BaseModel

from datetime import datetime
import os
from dotenv import load_dotenv

from database.sqlSetting import Engine
from database.restaurantService import loadRestaurantUrlById, loadMenu, loadRestaurantById
from weather import getWeatherFore

class RecommendModel(BaseModel):
    answer: str = Field(description="answer")
    id: str = Field(description="id")

class MenuAgent():
    def __init__(self) -> None:
        load_dotenv()
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        self.llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.8, api_key=OPENAI_API_KEY)
        
        engine = Engine().engine
        self.db = SQLDatabase(engine=engine, include_tables=['restaurants', 'menu'])

        self.parser = JsonOutputParser(pydantic_object=RecommendModel)
    
    def makeMenuChain(self):
        menuTemplate = """
            [System]
            너는 한국어로 대답해야 하며, 사용자의 질문, 사용자의 나이, 성별, 현재 날씨 및 시간에 맞춰 적합한 식사 메뉴를 추천해야 해.
            단, 데이터베이스에 있는 메뉴 중에서 하나만 추천해줘.

            [Data]
            사용자 나이 : {age}
            사용자 성별 : {gender},
            현재 날씨 : {weather},
            현재 시각 : {nowTime},
            데이터베이스 : {menuData}

            [Return]
            반드시 아래 양식에 맞춰서 JSON으로만 답변해줘. 추가 설명은 필요 없어.
            {{
                "menu": "현재 날씨와 사용자 질문을 고려한 메뉴 이름",
                "id": "메뉴 번호"
            }}
        """

        menuPrompt = ChatPromptTemplate.from_messages([
                ("system", menuTemplate),
                ("human", "{query}"),
            ])

        menuChain = menuPrompt | self.llm | self.parser
        return menuChain

    def MakeRecommnedTextChain(self):
        recommendTemplate = """
            [System]
            너는 한국어로 대답해야해.
            너는 현재 날씨에 맞춰 입력된 식당과 메뉴를 추천하는 한 문장을 출력해줘야해.
            이때, 한 문장으로 답해줘.

            [Data]
            식당 이름 : {restaurant}
            메뉴 이름 : {menu}
        """

        recommendPrompt = ChatPromptTemplate.from_messages([
                ("system", recommendTemplate),
        ])

        recommendChain = recommendPrompt | self.llm | StrOutputParser()
        return recommendChain
    
    def __getMenu(self, query, loc, gender, age):
        menuChain = self.makeMenuChain()

        response = menuChain.invoke(
                {"query": query,
                "age": age,
                "gender": gender,
                "weather": getWeatherFore(),
                "nowTime": datetime.now().strftime('%m-%d %H:%M'),
                "menuData": loadMenu(loc)
                })
        
        result = {
            'restaurant': loadRestaurantById(response['id']),
            'restaurantId': response['id'],
            'menu': response['menu']
        }
        return result
    
    def __getRecommendText(self, restaurant, menu):
        recommendChain = self.MakeRecommnedTextChain()

        response = recommendChain.invoke(
            {
                "restaurant": restaurant,
                "menu": menu
            })
        
        return response
    
    def getMenuRecommend(self, query, loc, gender, age):
        data = self.__getMenu(query, loc, gender, age)
        recommendText = self.__getRecommendText(data['restaurant'], data['menu'])
        url = loadRestaurantUrlById(data['restaurantId'])
        return {
            "answer": recommendText,
            "mapUrl": url
        }