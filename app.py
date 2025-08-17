from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Bus, Route, Stop, WaitRequest
from utils import hash_password, verify_password, calculate_eta, haversine, send_sms
from config import Config
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database and sample data function
def create_tables():
    if not os.path.exists('database'):
        os.makedirs('database')
    db.create_all()
    
    # Create sample data if not exists
    if User.query.count() == 0:
        # Create admin user
        admin = User(
            username='admin',
            email='admin@college.edu',
            password=hash_password('admin123'),
            role='admin'
        )
        
        # Create sample driver
        driver = User(
            username='driver1',
            email='driver1@college.edu',
            password=hash_password('driver123'),
            role='driver',
            phone='+1234567890'
        )
        
        # Create sample student
        student = User(
            username='student1',
            email='student1@college.edu',
            password=hash_password('student123'),
            role='student',
            phone='+1234567891'
        )
        
        db.session.add_all([admin, driver, student])
        db.session.commit()
        
        # Create sample bus
        bus = Bus(
            bus_number='BUS001',
            driver_id=driver.id,
            current_lat=40.7589,
            current_lng=-73.9851
        )
        
        db.session.add(bus)
        db.session.commit()
        
        # Create sample route
        route = Route(
            bus_id=bus.id,
            route_name='Vadavalli to KGISL Campus',
            start_time='08:00',
            end_time='18:00'
        )
        
        db.session.add(route)
        db.session.commit()
        
        # Create sample stops
        stops = [
            Stop(route_id=route.id, name='Vadavalli', lat=40.7589, lng=-73.9851, stop_order=1, estimated_time='08:00'),
            Stop(route_id=route.id, name='PN pudur', lat=40.7614, lng=-73.9776, stop_order=2, estimated_time='08:10'),
            Stop(route_id=route.id, name='Edarpalayam', lat=40.7505, lng=-73.9934, stop_order=3, estimated_time='08:20'),
            Stop(route_id=route.id, name='Goundapalayam', lat=40.7282, lng=-74.0776, stop_order=4, estimated_time='08:30'),
            Stop(route_id=route.id, name='Thudiyalore', lat=40.7282, lng=-74.0776, stop_order=4, estimated_time='08:40'),
            Stop(route_id=route.id, name='Kgisl Campus', lat=40.7282, lng=-74.0776, stop_order=4, estimated_time='08:50')
        ]
        
        db.session.add_all(stops)
        db.session.commit()

# Initialize database with app context (replaces @app.before_first_request)
with app.app_context():
    create_tables()

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and verify_password(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        phone = request.form.get('phone', '')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('register.html')
        
        user = User(
            username=username,
            email=email,
            password=hash_password(password),
            role=role,
            phone=phone
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'driver':
        return redirect(url_for('driver_dashboard'))
    elif current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return render_template('dashboard.html')

@app.route('/driver')
@login_required
def driver_dashboard():
    if current_user.role != 'driver':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    bus = Bus.query.filter_by(driver_id=current_user.id).first()
    wait_requests = []
    
    if bus:
        wait_requests = WaitRequest.query.filter_by(
            bus_id=bus.id, 
            acknowledged=False, 
            declined=False
        ).order_by(WaitRequest.timestamp.desc()).all()
    
    return render_template('driver.html', bus=bus, wait_requests=wait_requests)

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    buses = Bus.query.all()
    users = User.query.all()
    routes = Route.query.all()
    
    return render_template('admin.html', buses=buses, users=users, routes=routes)

@app.route('/bus_tracking')
@login_required
def bus_tracking():
    buses = Bus.query.filter_by(is_active=True).all()
    routes = Route.query.all()
    return render_template('bus_tracking.html', buses=buses, routes=routes)

# API Routes
@app.route('/api/update_location', methods=['POST'])
@login_required
def update_location():
    if current_user.role != 'driver':
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')
    
    if not lat or not lng:
        return jsonify({'error': 'Location data required'}), 400
    
    bus = Bus.query.filter_by(driver_id=current_user.id).first()
    
    if bus:
        bus.current_lat = float(lat)
        bus.current_lng = float(lng)
        bus.last_updated = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True})
    
    return jsonify({'error': 'Bus not found'}), 404

@app.route('/api/bus_locations')
@login_required
def get_bus_locations():
    buses = Bus.query.filter_by(is_active=True).all()
    locations = []
    
    for bus in buses:
        if bus.current_lat and bus.current_lng:
            locations.append({
                'id': bus.id,
                'bus_number': bus.bus_number,
                'lat': bus.current_lat,
                'lng': bus.current_lng,
                'driver': bus.driver.username if bus.driver else 'Unknown',
                'last_updated': bus.last_updated.isoformat() if bus.last_updated else None
            })
    
    return jsonify(locations)

@app.route('/api/wait_request', methods=['POST'])
@login_required
def wait_request():
    try:
        data = request.json
        bus_id = data.get('bus_id')
        stop_id = data.get('stop_id')
        message = data.get('message', '')
        
        if not bus_id or not stop_id:
            return jsonify({'error': 'Bus ID and Stop ID are required'}), 400
        
        # Check if bus is within range of stop
        bus = Bus.query.get(bus_id)
        stop = Stop.query.get(stop_id)
        
        if not bus or not stop:
            return jsonify({'error': 'Bus or stop not found'}), 404
        
        if not bus.current_lat or not bus.current_lng:
            return jsonify({'error': 'Bus location not available'}), 400
        

        
        # Check if user already has a pending request for this bus
        existing_request = WaitRequest.query.filter_by(
            bus_id=bus_id,
            user_id=current_user.id,
            acknowledged=False,
            declined=False
        ).first()
        
        if existing_request:
            return jsonify({'error': 'You already have a pending request for this bus'}), 400
        
        # Create wait request
        wait_req = WaitRequest(
            bus_id=bus_id,
            user_id=current_user.id,
            stop_id=stop_id,
            message=message
        )
        
        db.session.add(wait_req)
        db.session.commit()
        
        # Send notification to driver (if phone number available)
        if bus.driver and bus.driver.phone:
            sms_message = f"Wait request from {current_user.username} at {stop.name}. Message: {message}"
            send_sms(bus.driver.phone, sms_message)
        
        return jsonify({'success': True, 'message': 'Wait request sent'})
    
    except Exception as e:
        print(f"Error in wait_request: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/respond_wait_request', methods=['POST'])
@login_required
def respond_wait_request():
    if current_user.role != 'driver':
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        data = request.json
        request_id = data.get('request_id')
        response = data.get('response')  # 'acknowledge' or 'decline'
        
        if not request_id or not response:
            return jsonify({'error': 'Request ID and response are required'}), 400
        
        wait_req = WaitRequest.query.get(request_id)
        
        if not wait_req:
            return jsonify({'error': 'Request not found'}), 404
        
        # Verify the driver owns this bus
        if wait_req.bus.driver_id != current_user.id:
            return jsonify({'error': 'Access denied'}), 403
        
        if response == 'acknowledge':
            wait_req.acknowledged = True
        elif response == 'decline':
            wait_req.declined = True
        else:
            return jsonify({'error': 'Invalid response'}), 400
        
        db.session.commit()
        
        # Send response to student
        if wait_req.user.phone:
            action = "acknowledged" if response == 'acknowledge' else "declined"
            sms_message = f"Your wait request has been {action} by the driver."
            send_sms(wait_req.user.phone, sms_message)
        
        return jsonify({'success': True})
    
    except Exception as e:
        print(f"Error in respond_wait_request: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/eta/<int:bus_id>/<int:stop_id>')
@login_required
def get_eta(bus_id, stop_id):
    try:
        bus = Bus.query.get(bus_id)
        stop = Stop.query.get(stop_id)
        
        if not bus or not stop:
            return jsonify({'eta': None, 'error': 'Bus or stop not found'})
        
        if not bus.current_lat or not bus.current_lng:
            return jsonify({'eta': None, 'error': 'Bus location not available'})
        
        eta_minutes = calculate_eta(bus.current_lat, bus.current_lng, stop.lat, stop.lng)
        return jsonify({'eta': eta_minutes})
    
    except Exception as e:
        print(f"Error in get_eta: {e}")
        return jsonify({'eta': None, 'error': 'Internal server error'})

@app.route('/api/routes/<int:bus_id>')
@login_required
def get_route_stops(bus_id):
    try:
        bus = Bus.query.get(bus_id)
        if not bus:
            return jsonify({'error': 'Bus not found'}), 404
        
        stops = []
        for route in bus.routes:
            route_stops = Stop.query.filter_by(route_id=route.id).order_by(Stop.stop_order).all()
            for stop in route_stops:
                eta = None
                if bus.current_lat and bus.current_lng:
                    eta = calculate_eta(bus.current_lat, bus.current_lng, stop.lat, stop.lng)
                
                stops.append({
                    'id': stop.id,
                    'name': stop.name,
                    'lat': stop.lat,
                    'lng': stop.lng,
                    'stop_order': stop.stop_order,
                    'estimated_time': stop.estimated_time,
                    'eta': eta
                })
        
        return jsonify(stops)
    
    except Exception as e:
        print(f"Error in get_route_stops: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    
@app.route('/api/driver/wait_requests')
@login_required
def get_driver_wait_requests():
    if current_user.role != 'driver':
        return jsonify({'error': 'Access denied'}), 403
    
    bus = Bus.query.filter_by(driver_id=current_user.id).first()
    if not bus:
        return jsonify([])
    
    wait_requests = WaitRequest.query.filter_by(
        bus_id=bus.id, 
        acknowledged=False, 
        declined=False
    ).order_by(WaitRequest.timestamp.desc()).all()
    
    requests_data = []
    for req in wait_requests:
        requests_data.append({
            'id': req.id,
            'user': {
                'username': req.user.username
            },
            'stop': {
                'name': req.stop.name
            },
            'message': req.message,
            'timestamp': req.timestamp.isoformat()
        })
    
    return jsonify(requests_data)

# Add a health check route
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error_code=404, error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', error_code=500, error_message="Internal server error"), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
