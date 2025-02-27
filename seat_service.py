from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
from datetime import datetime
from models import db, Seat
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5000"])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seat.db'
app.config['SQLALCHEMY_BINDS'] = {
    'db1': 'sqlite:///employee.db',
    'db2': 'sqlite:///seat.db',
    'db3': 'sqlite:///manager.db' 
}

# Swagger setup
SWAGGER_URL="/swagger"
API_URL="/static/swagger_seat.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Seat API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

db.init_app(app)


@app.route('/seats', methods=['GET'])
def get_seats():
    slot_start = request.args.get('slot_start')
    slot_end = request.args.get('slot_end')
    parsed_slot_start = datetime.strptime(slot_start, "%Y-%m-%dT%H:%M")
    parsed_slot_end = datetime.strptime(slot_end, "%Y-%m-%dT%H:%M")
    if(parsed_slot_end < parsed_slot_start):
        return jsonify({"message":"start time should be before end time"}), 400
    else:
        available_seats = set()
        seats = Seat.query.all()
        for seat in seats:
            print(seat)
            if(seat.booking_start_time):
                if(seat.booking_start_time > parsed_slot_end or seat.booking_end_time < parsed_slot_start):
                    available_seats.add(seat.seat_id)
                else:
                    print(seat.booking_start_time > parsed_slot_end,seat.booking_end_time < parsed_slot_start)
                    try:
                        available_seats.remove(seat.seat_id)
                    except:
                        pass
            else:
                available_seats.add(seat.seat_id)
        available_seats = list(available_seats)
        print(available_seats)
        return jsonify({"seats": available_seats}), 200

# @app.route('/seats/<int:seat_id>', methods=['GET'])
# def get_seat(seat_id):
#     seat = Seat.query.get_or_404(seat_id)
#     return jsonify({'id': seat.id, 'number': seat.number, 'is_booked': seat.is_booked})

@app.route('/add_seats', methods=['POST'])
def add_seats():
    data = request.get_json()
    count = data['count']
    existing_count = db.session.query(func.max(Seat.seat_id)).scalar()
    for i in range(1, count+1):
        new_id = existing_count + i
        new_seat = Seat(seat_id=new_id)
        db.session.add(new_seat)
        db.session.commit()
    print(count, existing_count)
    # datetime_string = "2025-01-23T21:10"
    # a1 = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M")
    # datetime_string = "2025-01-23T21:30"
    # a2 = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M")
    # new_seat = Seat(seat_id=22,booked_by="eid1", booking_start_time=a1, booking_end_time=a2)
    # db.session.add(new_seat)
    # db.session.commit()
    return jsonify({"message": "new seats added"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5002)