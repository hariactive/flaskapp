from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from dotenv import load_dotenv
import os
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
from bson import ObjectId # it is used for update unique id find

load_dotenv()

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]  
app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token_cookie" 
app.config["JWT_COOKIE_CSRF_PROTECT"] = False  

jwt = JWTManager(app)

# My collections - Hari
users = mongo.db.users
records = mongo.db.records


@app.route('/create', methods=['GET', 'POST'])
@jwt_required() 
def create():
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        age_string = request.form['age']

        age = int(age_string)
        if records.count_documents({"name": name}) > 0:
            return jsonify({"error": "Record with this name already exists!"}), 400

        record_data = {
            "name": name,
            "city": city,
            "age": age,
            "created_at": datetime.utcnow(),  
            "updated_at": datetime.utcnow()   
        }
        records.insert_one(record_data)
        return jsonify({"message": "created succesfully"}), 201
    return render_template('create.html')

@app.route('/update/<record_id>', methods=['PUT'])
@jwt_required() 
def update_record(record_id):
    data = request.get_json() 

    if not ObjectId.is_valid(record_id):
        return jsonify({"error": "Invalid record ID"}), 400
    record = records.find_one({"_id": ObjectId(record_id)})
    if not record:
        return jsonify({"error": "Record not found"}), 404
    update_data = {}
    if "name" in data:
        update_data["name"] = data["name"]
    if "city" in data:
        update_data["city"] = data["city"]
    if "age" in data:
        update_data["age"] = int(data["age"])  # converting age to int kuki jsno data by default string hota hai
    if not update_data:
        return jsonify({"error": "No valid fields provided for update"}), 400
    updated_at_time = datetime.utcnow()
    # print("Updated At:", updated_at_time)
    update_data["updated_at"] = updated_at_time  
    records.update_one({"_id": ObjectId(record_id)}, {"$set": update_data})
    return jsonify({"message": "Record updated successfully!", "updated_at": str(updated_at_time)}), 200

@app.route('/delete/<record_id>', methods=['DELETE'])
@jwt_required() 
def delete_record(record_id):
    if not ObjectId.is_valid(record_id):
        return jsonify({"error": "Invalid record ID"}), 400
    record = records.find_one({"_id": ObjectId(record_id)})
    if not record:
        return jsonify({"error": "Record not found"}), 404
    records.delete_one({"_id": ObjectId(record_id)})
    return jsonify({"message": "Record deleted successfully!"}), 200

@app.route('/read', methods=['GET'])
@jwt_required() 
def get_all_records_page():
    records_list = []
    for record in records.find():
        records_list.append({
            "id": str(record["_id"]),
            "name": record["name"],
            "city": record["city"],
            "age": record["age"],
            "created_at": record.get("created_at", ""),
            "updated_at": record.get("updated_at", "")
        })
    return jsonify({"records": records_list})
    # return render_template('read.html', records=records_list)


@app.route('/read/<record_id>', methods=['GET'])
@jwt_required()
def get_record_page(record_id):
    if not ObjectId.is_valid(record_id):
        return "Invalid record ID", 400

    record = records.find_one({"_id": ObjectId(record_id)})
    if not record:
        return "Record not found", 404
    
    return jsonify({"records": record})
    # return render_template('record.html', record={
    #     "id": str(record["_id"]),
    #     "name": record["name"],
    #     "city": record["city"],
    #     "age": record["age"],
    #     "created_at": record.get("created_at", ""),
    #     "updated_at": record.get("updated_at", "")
    # })

@app.route('/home')
@app.route('/',methods =['GET'])
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if users.find_one({"email": email}):
            return jsonify({"error": "Email already exists!"}), 400
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "created_at": datetime.utcnow(),  
            "updated_at": datetime.utcnow()   
        }
        # mogo insert methods
        users.insert_one(user_data)
        return jsonify({"message": "User registered successfully!"}), 201
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # mogo database find the user 
        user = users.find_one({"email": email})
        if not user:
            return jsonify({"error": "Invalid email or password!"}), 401
        if not bcrypt.check_password_hash(user["password"], password):
            return jsonify({"error": "Invalid email or password!"}), 401
        access_token = create_access_token(identity=email, additional_claims={"username": user["username"]})
        print("acce", access_token)
        response = make_response(redirect(url_for("home")))  # Redirect to dashboard after login
        response.set_cookie("access_token_cookie", access_token, httponly=True, secure=True, samesite="Strict")
        return response
    return render_template('login.html')

@app.route('/dashboard', methods=['GET'])
@jwt_required() 
def dashboard():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Welcome {current_user}!"})

if __name__ == '__main__':
    app.run(debug=True)
