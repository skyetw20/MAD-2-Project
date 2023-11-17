# routes.py
from flask import jsonify, request, session,make_response
from app import app, db
from models import Shows, Theaters, User, Booking,ShowTheaterRelation
import os
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from functools import wraps
import jwt
from tasks import export_csv
import datetime
import pandas as pd
import json

################
import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)
###############################
def token_required(f):#decorator function to check if token is present or not
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # print(request.headers)
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        # print(token)
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        # print(app.config['SECRET_KEY'])
        try:
            # print('inside try')
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            # print(decoded_token)
            current_user = User.query.get(decoded_token['user_id'])
            # print(current_user)
        except:
            return jsonify({'message': 'Token is invalid'}), 402
        return f(*args, **kwargs)
    return decorated


@app.route('/shows', methods=['GET'])#route to get all shows
def get_shows():
    cache_key = 'shows_data'
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print('used cached data')
        return jsonify(json.loads(cached_data))
    shows = Shows.query.all()
    show_data = [{'id': show.id, 'name': show.name, 'rating': show.rating, 'tag': show.tag, 'duration': show.duration, 'ticket_price': show.ticket_price} for show in shows]
    redis_client.setex(cache_key, 3600, json.dumps({'shows': show_data}))
    return jsonify({'shows': show_data})



@app.route('/relation', methods=['GET'])#route to get the relation between shows and theaters
def get_realtions():
    strs = ShowTheaterRelation.query.all()
    realtion_data = [{'id': str.id, 'showid': str.show_id, 'theaterid': str.theater_id} for str in strs]
    user_info = {'status': 'Not signed in', 'user_id': None}
    if 'user_id' in session:
        user_info = {'status': 'Signed in', 'user_id': session['user_id']}
    return jsonify({'realtions': realtion_data })



@app.route('/theaters', methods=['GET'])#route to get all theaters
def get_theaters():
    cache_key = 'theaters_data'
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print('used cached data')
        return jsonify(json.loads(cached_data))
    theaters = Theaters.query.all()
    theater_data = [{'id': theater.id, 'name': theater.name, 'place': theater.place, 'capacity': theater.capacity, 'capacity_booked': theater.capacity_booked, 'rating': theater.rating} for theater in theaters]
    redis_client.setex(cache_key, 3600, json.dumps({'theaters': theater_data}))
    return jsonify({'theaters': theater_data})




@app.route('/login', methods=['POST'])#route for user login
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        # Update last_access column
        user.last_access = datetime.datetime.now() # Update the last_access column
        db.session.commit()  # Commit the changes to the database
        
        # Successful login
        session['user_id'] = user.id
        
        # Create and send JWT token
        # access_token = create_access_token(identity=user.id)
        access_token = jwt.encode({"user_id": user.id}, app.config['SECRET_KEY'], algorithm="HS256")
        print(access_token)
        return jsonify({
            'message': 'Login successful',
            'user_id': user.id,
            'username': user.name,
            'role': user.role,
            'email': email,
            'access_token': access_token
        }), 200
    else:
        # Incorrect credentials
        return jsonify({'message': 'Invalid email or password'}), 401




@app.route('/logout', methods=['GET'])#route for user logout
@token_required
def logout():
    # Check if the user is signed in
    if 'user_id' not in session:
        return make_response(jsonify({'message': 'You are not signed in'}), 401)  # Unauthorized status code

    # Clear the user_id from the session
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/signup', methods=['POST'])#route for user signup
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    print(name, email, password)
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'User with this email already exists. Signup not allowed.'}), 400
    new_user = User(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Signup successful'})



def get_show_name(show_id):#function to get the show name
    shows = Shows.query.all()
    # print(shows[0].name)
    for show in shows:
        if show.id==show_id:
            return show.name
def get_theater(theater_id):#function to get the theater name
    theaters = Theaters.query.all() 
    for theater in theaters:
        if theater.id==theater_id:
            return theater.name+', '+theater.place




@app.route('/account', methods=['GET'])#route to get the account details of the user
@token_required
def get_account_details():
    user_id = request.args.get('user_id') 
    if not user_id:
        return jsonify({'message': 'User ID not provided'})
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'})
    user_data = {'name': user.name, 'email': user.email}
    # Get the bookings for the user from the Booking table and add to user_data
    bookings = Booking.query.filter_by(user_id=user_id).all()
           
    user_data['bookings'] = [{'show': get_show_name(booking.show_id),'theater':get_theater(booking.theater_id),'date':booking.booking_date,'time':booking.booking_time,'seats':booking.num_seats_booked,'price':booking.total_price} for booking in bookings]
    # print(user_data['bookings'])
    return jsonify(user_data)



@app.route('/bookings', methods=['POST'])#route to add booking details of the user
@token_required
def add_booking():
    data = request.get_json()
    show_id = data.get('show_id')
    theater_id = data.get('theater_id')
    time = data.get('time')
    date = data.get('date')
    num_seats = data.get('num_seats')
    total_price = data.get('total_price')
    user_id = data.get('user_id')
   #vrify the details being sent from the request
    # Check if the user has already booked for this show
    existing_booking = Booking.query.filter_by(user_id=user_id, show_id=show_id).first()
    # if existing_booking:
    #     return jsonify({'message': 'You have already booked for this show'}), 400
    
    new_booking = Booking(user_id=user_id, show_id=show_id,theater_id=theater_id,
                            booking_date=date,booking_time=time,num_seats_booked=num_seats,
                            total_price=total_price)
    db.session.add(new_booking)
    # show.capacity_booked += 1
    db.session.commit()
    return jsonify({'message': 'Booking successful'})

@app.route('/addshow', methods=['POST'])#route to add show details
@token_required
def add_show():
    data = request.get_json()
    user = data.get('email')
    show_name = data.get('name')
    duration = data.get('duration')
    price = data.get('price')
    rating = data.get('rating')
    tag = data.get('tag')
    theaters = data.get('theaters')  
    user_instance = User.query.filter_by(email=user).first()
    if user_instance.role == 'admin':
        new_show = Shows(name=show_name, rating=rating, tag=tag, duration=duration, ticket_price=price)
        db.session.add(new_show)
        db.session.commit()
        for theater_id in theaters:
            relation = ShowTheaterRelation(show_id=new_show.id, theater_id=theater_id)
            db.session.add(relation)
        db.session.commit()
        return jsonify({'message': 'Show and relations added successfully.'}), 200
    else:
        return jsonify({'message': 'You do not have access to add the show'}), 400
    
@app.route('/addtheater',methods=['POST'])#route to add theater details
@token_required
def add_theater():
    data=request.get_json()
    user=data.get('email')
    name=data.get('name')
    place=data.get('place')
    capacity=data.get('capacity')
    rating=data.get('rating')
    capacity_booked=data.get('capacity_booked')
    users=User.query.filter_by(email=user).first()
    print(users.role)
    if users.role=='admin':
        new_show=Theaters(name=name,rating=rating,place=place,capacity=capacity,
                        capacity_booked=capacity_booked)
        db.session.add(new_show)
        db.session.commit()
        return jsonify({'message':'Added Successfully.'}),200
    else:
        return jsonify({'message': 'You do not have access to add.'}), 400
    

@app.route('/updateshow', methods=['PUT'])#route to update show details
@token_required
def update_show():
    data = request.get_json()
    user = data.get('email')
    show_id = data.get('show_id')  
    new_show_name = data.get('new_name')
    new_duration = data.get('new_duration')
    new_price = data.get('new_price')
    new_rating = data.get('new_rating')
    new_tag = data.get('new_tag')
    user_data = User.query.filter_by(email=user).first()
    print(show_id,new_show_name,new_duration,new_price,new_rating,new_tag)
    if user_data.role == 'admin':
        show_to_update = Shows.query.get(show_id)
        if not show_to_update:
            return jsonify({'message': 'Show not found'}), 404
        if new_show_name:
            show_to_update.name = new_show_name
        if new_duration:
            show_to_update.duration = new_duration
        if new_price:
            show_to_update.ticket_price = new_price
        if new_rating:
            show_to_update.rating = new_rating
        if new_tag:
            show_to_update.tag = new_tag
        db.session.commit()
        cache_key = 'shows_data'
        deleted = redis_client.delete(cache_key)
        return jsonify({'message': 'Show updated successfully'}), 200
    else:
        return jsonify({'message': 'You do not have access to update the show'}), 400



@app.route('/updatetheater', methods=['PUT'])#route to update theater details
@token_required
def update_theater():
    data = request.get_json()
    user = data.get('email')
    theater_id = data.get('theater_id')  
    new_name = data.get('new_name')
    new_place = data.get('new_place')
    new_capacity = data.get('new_capacity')
    new_rating = data.get('new_rating')
    new_capacity_booked = data.get('new_capacity_booked')
    
    user_data = User.query.filter_by(email=user).first()
    
    if user_data.role == 'admin':
        theater_to_update = Theaters.query.get(theater_id)
        if not theater_to_update:
            return jsonify({'message': 'Theater not found'}), 404
        if new_name:
            theater_to_update.name = new_name
        if new_place:
            theater_to_update.place = new_place
        if new_capacity:
            theater_to_update.capacity = new_capacity
        if new_rating:
            theater_to_update.rating = new_rating
        if new_capacity_booked:
            theater_to_update.capacity_booked = new_capacity_booked
        db.session.commit()
        cache_key = 'theaters_data'
        deleted = redis_client.delete(cache_key)
        return jsonify({'message': 'Theater updated successfully'}), 200
    else:
        return jsonify({'message': 'You do not have access to update the theater'}), 400



@app.route('/deleteshow', methods=['DELETE'])#route to delete show details
@token_required
def delete_show():
    data = request.get_json()
    user_email = data.get('email')
    show_id=data.get('show_id')
    user = User.query.filter_by(email=user_email).first()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    if user.role != 'admin':
        return jsonify({'message': 'You do not have access to delete shows'}), 403
    show_to_delete = Shows.query.get(show_id)
    if show_to_delete is None:
        return jsonify({'message': 'Show not found'}), 404
    db.session.delete(show_to_delete)
    cache_key = 'shows_data'
    deleted = redis_client.delete(cache_key)
    db.session.commit()
    return jsonify({'message': 'Show deleted successfully'}), 200



@app.route('/deletetheater', methods=['DELETE'])#route to delete theater details
@token_required
def delete_theater():
    data = request.get_json()
    user_email = data.get('email')
    id=data.get('theater_id')
    user = User.query.filter_by(email=user_email).first()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    if user.role != 'admin':
        return jsonify({'message': 'You do not have access to delete shows'}), 403
    theather_to_delete = Theaters.query.get(id)
    if theather_to_delete is None:
        return jsonify({'message': 'Theater not found'}), 404
    db.session.delete(theather_to_delete)
    cache_key = 'theaters_data'
    deleted = redis_client.delete(cache_key)
    db.session.commit()
    return jsonify({'message': 'Theater deleted successfully'}), 200



@app.route('/exporttheater',methods=['POST'])#route to export theater details
# @token_required
def export():
    data = request.get_json()
    # print(data)
    theater_id = data.get('theater_id')
    # print(theater_id)
    job = export_csv.apply_async(args=[int(theater_id)])
    return jsonify({"job_id": job.id}), 200


@app.route('/test')#route to test the api
def test_api():
    # job = say_hello.delay()
    return jsonify({"job_id": "hello, i'm working"}), 200






from sqlalchemy import inspect
@app.before_request#function to create tables if not present in the database before the request is made
def create_tables():
    inspector = inspect(db.engine)
    print(not inspector.has_table('User'))
    if not inspector.has_table('User'):
        db.create_all()
        print('added admin user')
        new_user = User(name='Sachin', email='sachin@admin.com', role='admin', password='admin')
        db.session.add(new_user)
        db.session.commit()