from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from models import db, Employee

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

db.init_app(app)


@app.route('/register', methods=['POST'])
def register():
    print(request)
    try:
        data = request.get_json()
        print(data)
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = Employee(emp_id=data['emp_id'], emp_name=data['emp_name'], manager_id=data['manager_id'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Employee registered successfully!'}), 201
    except:
        return jsonify({'message': 'Error in registration. Try again'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Employee.query.filter_by(emp_id=data['emp_id']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'emp_id': user.emp_id})
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)