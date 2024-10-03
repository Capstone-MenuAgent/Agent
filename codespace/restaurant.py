import json

def getRestaurant(loc='한국교통대학교 충주캠퍼스'):
    # 네이버 지도를 활용하여 해당 지역의 음식 크롤링

    ''' Test Data
    restaurantList = [
        {
            "name": "권짬뽕",
            "category": "중식",
            "menu": [
                "짜장", "짬뽕"
            ]
        },
        {
            "name": "두꺼비네",
            "category": "한식",
            "menu": [
                "순대국밥", "수육국밥"
            ]
        },
        {
            "name": "타베",
            "category": "일식",
            "menu": [
                "등심돈까스", "가츠동"
            ]
        }
    ]
    '''
    path = f'./codespace/restaurants/{loc}.json'
    with open(path, 'r', encoding='utf-8') as f:
        restaurantList = json.load(f)
    
    return restaurantList