from flask import Flask, request, jsonify
app = Flask(__name__)

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

