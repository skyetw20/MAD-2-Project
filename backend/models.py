from app import db


class Shows(db.Model):#model for shows
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float)
    tag = db.Column(db.String(50))
    duration = db.Column(db.Integer)
    ticket_price = db.Column(db.Float)

class Theaters(db.Model):#model for theaters
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(100))
    capacity = db.Column(db.Integer)
    capacity_booked = db.Column(db.Integer)
    rating = db.Column(db.Float)

class User(db.Model):#model for users
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='user')
    password = db.Column(db.String(100), nullable=False)
    last_access=db.Column(db.String(100))

class Booking(db.Model):#model for bookings
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'))
    booking_date = db.Column(db.String)
    booking_time = db.Column(db.String)
    total_price = db.Column(db.Integer)
    num_seats_booked = db.Column(db.Integer)
    theater_id=db.Column(db.Integer)



class ShowTheaterRelation(db.Model):#model for show theater relation
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)
    theater_id = db.Column(db.Integer, db.ForeignKey('theaters.id'), nullable=False)
    show = db.relationship('Shows', backref=db.backref('theater_relations', lazy=True))
    theater = db.relationship('Theaters', backref=db.backref('show_relations', lazy=True))