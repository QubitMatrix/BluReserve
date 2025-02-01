## Problem Statement
Design a seat booking system for an office cafeteria.   

### Required Features
- Register and login using office email
- Booking seats uses manager's blu-dollars and is refunded on cancelation
- Uses Swagger for API documentation

### Additional Features
- Security
   - Store hashed passwords
   - Input sanitization
   - Secure HTTP methods (POST over GET)
- Built as microservices
- Additional API support to add more seats and view manager details

### Tech Stack
- HTML
- CSS
- Javascript
- Python
    - Flask
    - SQLAlchemy for SQLite database

## Setting Up
`pip install -r requirements.txt`

## Running Frontend GUI
`python3 home.py` -> runs on port 5000

### Routes
1. Register
    - Implemented input sanitization to avoid injection attacks
    - Stores password as hash to ensure confidentiality
    - Registration functionality achieved through **Register** API in **Authentication** microservice

2. Login
    - Password check to authenticate
    - Login functionality achieved through **Login** API in **Authentication** microservice

3. Reservation
    - Page to view, book and cancel reservations

## Running Authentication Microservice
`python3 auth_service.py` -> runs on port 5001

### APIs
1. Register
2. Login
3. Add Manager -> to add new manager details (manager_id and blu_dollars)

## Running Seating Microservice
`python3 seat_service.py` -> runs on port 5002

### APIs
1. Seats -> takes the start and end of slot and shows available seats
2. Add_seats -> allows additional seats to be added to cafeteria

## Running Reservation Microservice
`python3 reservation_service.py` -> runs on port 5003

### APIs
1. Reserve -> takes the slot timings and seat_id and makes the booking by resrving the seat and deducting blu_dollars from manager account
2. View_reserved -> shows all the bookings by logged user
3. Cancel_reservation -> cancels the seat booked for given slot and refunds the blu_dollars

## Database Models
1. Employee Table: Stores employee details   
    - emp_id: string (Primary Key)
    - emp_name: string
    - manager_id: string (Foreign Key)
    - password: string

2. Seat Table: Stores the seat details   
    - seat_id: integer
    - booked_by: string
    - booking_start_time: datetime
    - booking_end_time: datetime
  
    > (seat_id, booking_start_time, booking_end_time) form the compound primary key   

3. Manager: Stores the manager details   
    - manager_id: string (Primary Key)
    - Blu_dollars: integer

## Swagger
Access `http://127.0.0.1:5001/swagger` 
