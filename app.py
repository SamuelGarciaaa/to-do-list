from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    error = request.args.get('error')
    return render_template('index.html', error=error)

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    password = request.form.get('password')
    email = request.form.get('email')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            name TEXT,
            email TEXT,
            password TEXT
            )
    ''')

    cursor.execute('''
        SELECT * FROM users WHERE name = ? AND email = ?
    ''', (name, email))
    exists = cursor.fetchall()

    if exists:
        conn.close()
        return redirect(url_for('index', error='Error! There is already a user with that name or email, try logging in.'))
    
    else:
        cursor.execute('''
            INSERT INTO users(name, password, email) VALUES (?, ?, ?)
        ''', (name, password, email))

        conn.commit()
        conn.close()

        return redirect(url_for('main', name=name))
    
@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            name TEXT, 
            password TEXT
            )
    ''')

    cursor.execute('''
        SELECT * FROM users WHERE name = ? AND password = ?
    ''', (name, password))
    exists = cursor.fetchall()

    if exists:
        conn.close()
        return redirect(url_for('main', name=name))

    else:
        conn.close()
        return redirect(url_for('index', error='Error! Incorrect username or password.'))
    
@app.route('/main/<name>')
def main(name):
    return render_template('main.html', name=name)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")