from flask import Flask, request, jsonify
from flask_cors import CORS
from recommendAgnet import MenuAgent

app = Flask(__name__)
CORS(app)

# /agent로 리버스 프록시됨
@app.route('/question', methods=['GET'])
def questionTest():
    paramsDict = request.args.to_dict()
    query = paramsDict['query']
    loc = paramsDict['loc']
    gender = paramsDict['gender']
    age = paramsDict['age']
    
    menuAgent = MenuAgent()

    ans = menuAgent.getMenuRecommend(query, loc, gender, age)

    return jsonify(ans)


if __name__ == '__main__':
    app.run(port=5000)