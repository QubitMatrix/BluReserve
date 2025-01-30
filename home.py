from flask import Flask, render_template, request, redirect, url_for
import requests
from validation import validate_reg_input, validate_login_input

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        validation_error = validate_reg_input(request.form)
        if validation_error:
            return validation_error
        emp_id = request.form['emp_id']
        emp_name = request.form['emp_name']
        manager_id = request.form['manager_id']
        password = request.form['password']

        response = requests.post('http://127.0.0.1:5001/register', json={'emp_id': emp_id, 'emp_name': emp_name, 'manager_id': manager_id, 'password': password})

        if response.status_code == 201:
            return redirect(url_for('home'))  # Redirect to home on success
        else:
            return response.json()['message']  # Show error message from API
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        validation_error = validate_login_input(request.form)
        if validation_error:
            return validation_error
        emp_id = request.form['emp_id']
        password = request.form['password']

        response = requests.post('http://127.0.0.1:5001/login', json={'emp_id': emp_id, 'password': password})

        if response.status_code == 200:
            return redirect(url_for('reservation', emp_id=emp_id))  # Redirect to reservation on success
        else:
            return response.json()['message']  # Show error message from API
    
    return render_template('login.html')

@app.route('/reservation', methods=['GET','POST'])
def reservation():
    emp_id = request.args.get('emp_id')
    print(emp_id)
    return render_template('reservation.html', emp_id=emp_id)

if __name__ == '__main__':
    app.run(debug=True, port=5000)