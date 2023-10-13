import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)


# Initialisation de la base de données SQLite
def init_db():
    conn = sqlite3.connect('pixels.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pixels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            x INTEGER,
            y INTEGER,
            color TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Initialiser la base de données
init_db()


@app.route('/')
def index():
    # Récupérer les données de la base de données
    conn = sqlite3.connect('pixels.db')
    cursor = conn.cursor()
    cursor.execute('SELECT x, y, color FROM pixels')
    pixels = cursor.fetchall()
    conn.close()

    return render_template('index.html', pixels=pixels)


@socketio.on('draw')
def handle_draw(data):
    x, y, color = data['x'], data['y'], data['color']

    # Enregistrement de la position du pixel dans la base de données
    conn = sqlite3.connect('pixels.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO pixels (x, y, color) VALUES (?, ?, ?)', (x, y, color))
    conn.commit()
    conn.close()

    # Émission de l'événement aux clients connectés
    socketio.emit('draw', {'x': x, 'y': y, 'color': color})


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
