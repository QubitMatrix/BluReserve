from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from seat_service import Seat
from sqlalchemy import func
from datetime import datetime
from models import db, Seat, Employee, Manager
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5000"])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['SQLALCHEMY_BINDS'] = {
    'db1': 'sqlite:///employee.db',
    'db2': 'sqlite:///seat2.db',
    'db3': 'sqlite:///manager.db' 
}
db.init_app(app)

@app.route('/reserve', methods=['POST'])
def reserve_seat():
    data = request.get_json()
    seat_id = data['seat_id']
    start_time = data['start_time']
    start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
    end_time = data['end_time']
    end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
    emp_id = data['emp_id']
    booked_seat = Seat(seat_id=seat_id, booked_by=emp_id, booking_start_time=start_time, booking_end_time=end_time)
    db.session.add(booked_seat)
    db.session.commit()
    emp = Employee.query.filter_by(emp_id=emp_id).first()
    manager_id = emp.manager_id
    print(manager_id)
    manager = Manager.query.filter_by(manager_id=manager_id).first()
    print(manager.blu_dollars)
    if(manager):
        manager.blu_dollars -= 1
        db.session.commit()
    return jsonify({"message":"Booking successful"}), 201

@app.route('/view_reserved', methods=['POST'])
def get_reserved_seats():
    data = request.get_json()
    emp_id = data['emp_id']
    seats = Seat.query.filter_by(booked_by=emp_id).all()
    seats_arr = []
    for seat in seats:
        seats_arr.append(seat.to_dict())
    print(seats_arr)
    if(seats_arr):
        return jsonify({"reserved_seats": seats_arr}), 200
    else:
        return jsonify({"message": "no seats reserved"}), 400

@app.route('/cancel_reservation', methods=['POST'])
def cancel_reservation():
    data = request.get_json()
    emp_id = data['emp_id']
    seat_id = int(data['seat_id'])
    start_time = data['start_time']
    start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
    end_time = data['end_time']
    end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
    seat = Seat.query.filter_by(seat_id=seat_id, booking_start_time=start_time, booking_end_time=end_time).first()
    if seat:
        seat.booked_by = None
        seat.booking_start_time=None
        seat.booking_end_time = None
        db.session.commit()
        emp = Employee.query.filter_by(emp_id=emp_id).first()
        manager_id = emp.manager_id
        print(manager_id)
        manager = Manager.query.filter_by(manager_id=manager_id).first()
        print(manager.blu_dollars)
        if(manager):
            manager.blu_dollars += 1
            db.session.commit()
        return jsonify({"message": "Seat canceled successfully"})
    else:
        return jsonify({"message": "Seat not found"})
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5003)