from flask import Flask, jsonify, request
from menuAgent import menuRecomment

app = Flask(__name__)

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