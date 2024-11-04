from sqlalchemy.orm import Session

from database.sqlSetting import Engine
from database.tables import RestaurantTable, MenuTable


engine = Engine().engine
conn = engine.connect()

def loadRestaurantUrlById(id):
    session = Session(bind=engine)
    query = session.query(
        RestaurantTable.url
    ).filter(RestaurantTable.id == id)
    queryData = query.first()[0]
    session.close()
    return queryData

def loadAllRestaurantAndMenu(loc):
    session = Session(bind=engine)
    try:
        query = session.query(
            RestaurantTable.id,
            RestaurantTable.title,
            RestaurantTable.tag,
            RestaurantTable.rating,
            RestaurantTable.reviewNum,
            RestaurantTable.url,
            MenuTable.name
        ).join(MenuTable, RestaurantTable.id == MenuTable.restaurantId
        ).filter(RestaurantTable.loc == loc
        ).order_by(RestaurantTable.id)
        queryData = query.all()

        queryDict = {}
        for data in queryData:
            if queryDict.get(data[0]):
                queryDict[data[0]]['menu'].append(data[6])
            else:
                queryDict[data[0]] = {
                    "id": data[0],
                    "title": data[1],
                    "tag": data[2],
                    "rating": data[3],
                    "reviewNum": data[4],
                    "menu": [data[6]]
                }
        
        resultText = ""
        for i in queryDict.keys():
            data = queryDict[i]
            resultText += f"title: {data['title']}, tag: {data['tag']}, rating: {data['rating']}, reviewNum: {data['reviewNum']}, id: {data['id']}, menu: {', '.join(data['menu'])}\n "

        return resultText
    
    except Exception as e:
        print(f"오류 발생: {e}")
        return None
    finally:
        session.close()  # 세션 종료