import re

from flask import jsonify, request

def validate_name(name):
    print(f"name: {name}")
    name_pattern = r'^[a-zA-Z ]+$'  # regex to accept one or more letters or spaces
    return bool(re.match(name_pattern, name)) and len(name.strip()) > 0

def validate_email(email):
    print(f"Email: {email}")
    email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'  # regex to validate email address
    return bool(re.match(email_pattern, email))

def validate_password(password):
    print(f"Password: {password}")
    password_pattern = r'^[a-zA-Z0-9@#$!%&]{8,30}$'  # regex to validate password (8 to 30 characters, letters, digits, or special symbols)
    return bool(re.match(password_pattern, password))

def validate_reg_input(data):
    """Validate the input for user registration."""
    print(data)
    # Validate name
    name = data['emp_name']
    valid = validate_name(name)
    if not valid:
        return jsonify({"error": "Use only letters"}), 400

    # Validate email
    email = data['emp_id']
    if email:
        valid = validate_email(email)
        if not valid:
            return jsonify({"error": "Use only email regex"}), 400
        
    # Validate email (manager)
    manager_email = data['manager_id']
    if manager_email:
        valid = validate_email(manager_email)
        if not valid:
            return jsonify({"error": "Use only emial regex"}), 400

    # Validate password
    password = data['password']
    valid = validate_password(password)
    if not valid:
        return jsonify({"error": "Use min 8 and max 30 characters, only letters and number and non scripting characters"}), 400

    return None  # No errors

def validate_login_input(data):
    print(data)

    # Validate email
    email = data['emp_id']
    if email:
        valid = validate_email(email)
        if not valid:
            return jsonify({"error": "Use only emial regex"}), 400
        
    # Validate password
    password = data['password']
    valid= validate_password(password)
    if not valid:
        return jsonify({"error": "Use min 8 and max 30 characters, only letters and number and non scripting characters"}), 400

    return None  # No errors
