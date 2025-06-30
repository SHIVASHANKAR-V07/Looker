from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def check_login(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

@app.route('/')
def show_login():
    return render_template('Looker_Login.htm')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if check_login(username, password):
        return render_template('Looker_Home.htm')
    else:
        return "Invalid username or password. Please go back and try again."
    
@app.route('/home')
def home_page():
    return render_template('Looker_Home.htm')

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
