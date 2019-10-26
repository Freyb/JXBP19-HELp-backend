from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/api/getheat', methods=['POST'])
def add_message():
    content = request.json
    print(content['mytext'])
    return jsonify({"response":"Success"})

if __name__ == '__main__':
    app.run()

