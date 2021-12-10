from flask import Flask, jsonify, abort, make_response, request
from models import paintings
import sys


app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/api/v1/paintings/", methods=["GET"])
def paintings_list_api_v1():
    return jsonify(paintings.all())

@app.route("/api/v1/paintings/<int:painting_id>", methods=["GET"])
def get_todo(painting_id):
    painting = paintings.get(painting_id)
    if not painting:
        abort(404)
    return jsonify({"painting": painting})

@app.route("/api/v1/paintings/", methods=["POST"])
def create_painting():
    if not request.json or not 'name' in request.json:
        print('This is error output', file=sys.stderr)
        abort(400)
    data = request.json    
    painting = {
        'id': paintings.all()[-1]['id'] + 1,
        'name': data.get('name'),
        'year': data.get('year')
    }
    paintings.create(painting)
    return jsonify({'painting': painting}), 201

@app.route("/api/v1/paintings/<int:painting_id>", methods=['DELETE'])
def delete_painting(painting_id):
    result = paintings.delete(painting_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/paintings/<int:painting_id>", methods=["PUT"])
def update_painting(painting_id):
    painting = paintings.get(painting_id)
    if not painting:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'name' in data and not isinstance(data.get('name'), str),
        'year' in data and not isinstance(data.get('year'), int),
    ]):
        abort(400)
    painting = {
        'id': painting_id,
        'name': data.get('name', painting['name']),
        'year': data.get('year', painting['year'])
    }
    paintings.update(painting_id, painting)
    return jsonify({'painting': painting})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

if __name__ == "__main__":
    app.run(debug=True)