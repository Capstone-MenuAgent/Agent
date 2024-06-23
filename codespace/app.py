from flask import Flask, request, redirect
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
    url = f"http://127.0.0.1:8080/agent/answer?ans={res}"
    #jsonify(res)
    return redirect(url)


if __name__ == '__main__':
    app.run()