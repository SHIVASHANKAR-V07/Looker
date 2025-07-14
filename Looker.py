from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'this_791'

def init_users_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_users_db()

@app.route('/')
def home_page():
    return render_template('Looker_Home.htm')

def get_user(email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()
    return user

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user(email)
        if user and user[2] == password:
            session['user'] = email
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home_page'))
        else:
            flash('Invalid credentials!', 'error')
            return redirect(url_for('signin'))
    return render_template('Looker_Signin.htm')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
            conn.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('signin'))
        except sqlite3.IntegrityError:
            flash('Email already exists.', 'error')
            return redirect(url_for('signup'))
        finally:
            conn.close()
    return render_template('Looker_Signup.htm')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully!', 'info')
    return redirect(url_for('home_page'))

@app.route('/shirt_1')
def blue_shirt():
    return render_template('Blue_shirt.htm')

@app.route('/shirt_2')
def grey_hoodie():
    return render_template('Grey_hoodie.htm')

@app.route('/pant_1')
def formal_pant():
    return render_template('Formal_pant.htm')

@app.route('/pant_2')
def track_pant():
    return render_template("Track_pant.htm")

if __name__ == '__main__':
    app.run(debug=True)
