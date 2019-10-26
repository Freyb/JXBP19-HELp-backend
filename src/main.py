from flask import Flask, request, jsonify
from flask_cors import CORS

from heat_map_provider import do_the_job

app = Flask(__name__)
CORS(app)


@app.route('/api/getheat', methods=['POST'])
def add_message():
    message_data = request.json   
    list_of_values_per_coord = do_the_job(message_data)
    return jsonify(list_of_values_per_coord)

if __name__ == '__main__':
    app.run()

