from flask import Flask, jsonify, request
from simpleMenuBot import menuBotChain

app = Flask(__name__)
age = 25
gender = "남성"
weather = "맑음"

@app.route('/ask', methods=['POST'])
def ask():
    query = request.json
    question = query['question']
    res = menuBotChain.invoke(
        {
            "question": question,
            "age": age,
            "gender": gender,
            "weather": weather
        }
    )
    return jsonify(res)


if __name__ == '__main__':
    app.run()