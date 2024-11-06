from sqlalchemy.orm import Session

from database.sqlSetting import Engine
from database.tables import RestaurantTable, MenuTable

engine = Engine().engine
conn = engine.connect()

def loadMenu(loc):
    session = Session(bind=engine)

    query = session.query(
        MenuTable.name,
        MenuTable.restaurantId
    )
    queryData = query.all()

    queryDict = {}
    for data in queryData:
        queryDict[data[0]] = data[1]

    session.close()
    return queryDict

def loadRestaurantById(id):
    session = Session(bind=engine)

    query = session.query(
        RestaurantTable.title
    ).filter(RestaurantTable.id == id)
    queryData = query.first()[0]

    session.close()
    return queryData

def loadRestaurantUrlById(id):
    session = Session(bind=engine)
    query = session.query(
        RestaurantTable.url
    ).filter(RestaurantTable.id == id)
    queryData = query.first()[0]
    session.close()
    return queryData