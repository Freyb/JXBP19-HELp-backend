from flask import Flask, request, jsonify
from flask_cors import CORS

from heat_map_provider import do_the_job, do_the_job_2

app = Flask(__name__)
CORS(app)


@app.route('/api/getheat', methods=['POST'])
def add_message():
    message_data = request.json   
    list_of_values_per_coord = do_the_job(message_data)
    return jsonify(list_of_values_per_coord)

@app.route('/api/getnearby', methods=['POST'])
def add_message_2():
    message_data = request.json   
    list_of_nearby_places = do_the_job_2(message_data)
    return jsonify(list_of_nearby_places)

if __name__ == '__main__':
    app.run()

