from flask import Flask, jsonify, request
from menuAgent import menuRecomment

app = Flask(__name__)
age = 25
gender = "남성"
weather = "맑음"

@app.route('/question/', methods=['GET'])
def question():
    paramsDict = request.args.to_dict()
    query = paramsDict['query']
    age = paramsDict['age']
    gender = paramsDict['gender']
    loc = paramsDict['loc']
    res = menuRecomment(query, age, gender, loc)
    return jsonify(res)


if __name__ == '__main__':
    app.run()