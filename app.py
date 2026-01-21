from flask import Flask, request, jsonify, render_template 
35  
  
from flask_sqlalchemy import SQLAlchemy 
import serial 
import threading 
 
app = Flask(__name__, template_folder="template") 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
 
db = SQLAlchemy(app) 
 
# Database Models 
class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(50), nullable=False) 
    password = db.Column(db.String(50), nullable=False) 
    email = db.Column(db.String(100), nullable=False) 
    phone = db.Column(db.String(15), nullable=False) 
    history = db.Column(db.Text, nullable=True) 
 
class ParkingSlot(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    slot_number = db.Column(db.Integer, nullable=False) 
    occupied = db.Column(db.Boolean, nullable=False, default=False) 
 
# Create tables and insert initial data 
@app.before_request 
def create_tables(): 
    if not hasattr(app, 'tables_created'): 
        db.create_all() 
        if ParkingSlot.query.count() == 0: 
            for i in range(1, 7): 
                slot = ParkingSlot(slot_number=i, occupied=False) 
                db.session.add(slot) 
            db.session.commit() 
 
        # Insert a user record with name "shiva" and password "12345" 
        if not User.query.filter_by(name="shiva").first(): 
            new_user = User(name="shiva", password="12345", email="shiva@example.com", 
phone="1234567890") 
            db.session.add(new_user) 
            db.session.commit() 
         
        app.tables_created = True 
36  
  
 
# Routes 
@app.route('/') 
def index(): 
    return render_template('index.html') 
 
@app.route('/register', methods=['POST']) 
def register(): 
    data = request.get_json() 
    new_user = User(name=data['name'], password=data['password'], email=data['email'], 
phone=data['phone'], history=data.get('history', '')) 
    db.session.add(new_user) 
    db.session.commit() 
    return jsonify({'message': 'User registered successfully!'}) 
 
@app.route('/login', methods=['POST']) 
def login(): 
    data = request.get_json() 
    user = User.query.filter_by(name=data['name'], password=data['password']).first() 
    if user: 
        return jsonify({'message': 'Login successful!', 'user_id': user.id}) 
    else: 
        return jsonify({'message': 'Invalid credentials'}), 401 
 
@app.route('/slots', methods=['GET']) 
def get_slots(): 
    slots = ParkingSlot.query.all() 
    return jsonify([{'slot_number': slot.slot_number, 'occupied': slot.occupied} for slot in slots]) 
 
@app.route('/update_slot/<int:slot_number>', methods=['POST']) 
def update_slot(slot_number): 
    slot = ParkingSlot.query.filter_by(slot_number=slot_number).first() 
    if slot: 
        slot.occupied = request.get_json()['occupied'] 
        db.session.commit() 
        return jsonify({'message': 'Slot updated successfully!'}) 
    else: 
        return jsonify({'message': 'Slot not found'}), 404 
 
# Arduino Integration (only updates slot 2) 
def read_arduino_data(): 
    arduino = serial.Serial('COM3', 9600)  # Replace with your Arduino's serial port 
    with app.app_context():  # Create application context 
37  
  
        while True: 
            try: 
                slot_status = arduino.readline().decode('utf-8').strip() 
                slot_occupied = bool(int(slot_status)) 
                slot = ParkingSlot.query.filter_by(slot_number=2).first()  # Update only slot 2 
                if slot: 
                    slot.occupied = slot_occupied 
                    db.session.commit() 
            except Exception as e: 
                print(f"Error reading from Arduino: {e}") 
 
# Start a background thread to read Arduino data 
threading.Thread(target=read_arduino_data, daemon=True).start() 
 
if __name__ == '__main__': 
    app.run(debug=True) 
