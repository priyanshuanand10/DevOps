from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize the board
board = ['' for _ in range(9)]
current_turn = 'X'

def check_winner():
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != '':
            return board[condition[0]]
    if '' not in board:
        return 'Tie'
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    global current_turn
    index = int(request.json['index'])
    if board[index] == '':
        board[index] = current_turn
        winner = check_winner()
        if winner:
            response = {'board': board, 'winner': winner}
            return jsonify(response)
        current_turn = 'O' if current_turn == 'X' else 'X'
        response = {'board': board, 'winner': None}
        return jsonify(response)
    return jsonify({'board': board, 'winner': None})

@app.route('/reset', methods=['POST'])
def reset():
    global board, current_turn
    board = ['' for _ in range(9)]
    current_turn = 'X'
    return jsonify({'board': board})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
