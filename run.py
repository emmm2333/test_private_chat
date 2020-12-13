from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'

socketio = SocketIO(app, cors_allowed_origins='*')


all_sid = {}


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        if username:
            session['username'] = username
            return jsonify({'code': 200, 'username': username})
        return jsonify({'code': 500})
    return render_template('login.html')


@app.route('/chat')
def chat():
    return render_template('chat.html', username=session['username'])


@socketio.on('store_sid')
def store_sid(data):
    all_sid[data['username']] = request.sid
    print('username added!      all_sid: ', all_sid)


@socketio.on('new_message')
def new_message(data):
    recipient = data['recipient']
    sender = data['sender']
    message = data['message']
    print(recipient, type(recipient))
    print('message: ', message)
    print(all_sid, all_sid[recipient])
    emit('message_resp', {'message': message}, room=all_sid[recipient])


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=2323, debug=True)
