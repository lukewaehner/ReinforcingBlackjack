from flask import Flask, jsonify, request
from flask_cors import CORS
from models import RLModel

app = Flask(__name__)
CORS(app)

model = RLModel()


@app.route('/', methods=['GET'])
def start_game():
    state = model.initialize_game()
    return jsonify(state)


@app.route('/draw', methods=['POST'])
def draw_card():
    user_move = request.json.get('move')
    state, ai_move = model.play(user_move)
    return jsonify({"state": state, "ai_move": ai_move})


@app.route('/ai_turn', methods=['POST'])
def ai_turn():
    state = model.ai_turn()
    return jsonify(state)


@app.route('/reset', methods=['POST'])
def reset_game():
    state = model.initialize_game()
    return jsonify(state)


@app.route('/reset_deck', methods=['POST'])
def reset_deck():
    state = model.reset_deck()
    return jsonify(state)


if __name__ == '__main__':
    app.run(debug=True)
