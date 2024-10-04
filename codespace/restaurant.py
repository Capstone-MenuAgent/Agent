import json

def getRestaurant(loc='한국교통대학교 충주캠퍼스'):
    path = f'./codespace/restaurants/{loc}.json'
    with open(path, 'r', encoding='utf-8') as f:
        restaurantList = json.load(f)

    restaurantDataText = ""
    for restaurant in restaurantList:
        restaurantDataText += f"음식점 이름: {restaurant['title']}, 분류: {restaurant['tag']}, 별점: {restaurant['rating']}, 리뷰수: {restaurant['reviewNum']}, 주소: {restaurant['address']}, 메뉴: {', '.join(restaurant['menu'])}\n"
        
    return restaurantDataText