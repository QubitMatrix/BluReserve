from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = 'employee'
    emp_id = db.Column(db.String(100), primary_key=True)
    emp_name = db.Column(db.String(80), nullable=False)
    manager_id = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Seat(db.Model):
    __tablename__ = 'seat1'
    seat_id = db.Column(db.Integer)
    #capacity = db.Column(db.Integer, nullable=False)
    #is_booked = db.Column(db.Boolean, default=False)
    booked_by = db.Column(db.String(100))
    booking_start_time = db.Column(db.DateTime)
    booking_end_time = db.Column(db.DateTime)

    __table_args__ = (db.PrimaryKeyConstraint('seat_id', 'booking_start_time', 'booking_end_time'),)

    def to_dict(self):
        return {
            'seat_id': self.seat_id,
            'booked_by': self.booked_by,
            'booking_start_time': self.booking_start_time.isoformat(),
            'booking_end_time': self.booking_end_time.isoformat()
        }