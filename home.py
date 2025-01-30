from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        response = requests.post('http://127.0.0.1:5001/register', json={'username': username, 'password': password})

        if response.status_code == 201:
            return redirect(url_for('home'))  # Redirect to home on success
        else:
            return response.json()['message']  # Show error message from API
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        response = requests.post('http://127.0.0.1:5001/login', json={'username': username, 'password': password})

        if response.status_code == 200:
            return redirect(url_for('reservation'))  # Redirect to reservation on success
        else:
            return response.json()['message']  # Show error message from API
    
    return render_template('login.html')

@app.route('/reservation', methods=['GET','POST'])
def reservation():
    return render_template('reservation.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)