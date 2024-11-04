import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from recommentAgent import menuRecomment

app = Flask(__name__)
CORS(app)

@app.route('/agent/question', methods=['GET'])
def questionTest():
    paramsDict = request.args.to_dict()
    query = paramsDict['query']
    loc = paramsDict['loc']
    gender = paramsDict['gender']
    age = paramsDict['age']
    
    ans = menuRecomment(query, loc, gender, age)
    print(ans)

    #return 
    return jsonify(ans)


if __name__ == '__main__':
    app.run(port=5001)