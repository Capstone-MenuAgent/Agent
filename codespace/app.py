import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from menuAgent import menuRecomment

app = Flask(__name__)
CORS(app)

@app.route('/agent/question', methods=['POST'])
def question():
    paramsDict = request.args.to_dict()
    query = paramsDict['query']
    id = paramsDict['id']
    loc = paramsDict['loc']
    gender = paramsDict['gender']
    age = paramsDict['age']

    auth = request.headers.get('Authorization')
    

    ans = menuRecomment(query, loc, gender, age)
    res = ans.split("\n")
    data = {
                "id": id,
                "answer": res[0],
                "addr": res[1]
            }
    
    url = "http://127.0.0.1:8080/api/v1/agent/answer"
    headers = {
        "Authorization": auth,
        "Content-Type": "application/json"
    }
    response = requests.get(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return jsonify({"status": "success", "response": response.json()})
    else:
        return jsonify({"status": "failed", "error": response.status_code}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)