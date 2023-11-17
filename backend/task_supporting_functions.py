from models import Shows, Theaters, User, Booking,ShowTheaterRelation
from datetime import datetime, timedelta
from app import app,db
import datetime
import pandas as pd
import json
from send_email import send_email_function


def get_show_name(show_id):#function to get the show name from the show id
    with app.app_context():
        shows = Shows.query.all()
    # print(shows[0].name)
    for show in shows:
        if show.id==show_id:
            return show.name


def get_theater(theater_id):#function to get the theater name from the theater id
    with app.app_context():
        theaters = Theaters.query.all() 
    for theater in theaters:
        if theater.id==theater_id:
            return theater.name+', '+theater.place


def get_current_month():#function to get the current month
    now = datetime.datetime.now()
    current_month = now.strftime('%Y-%m')
    return str(current_month)



def get_inactive_users_email():#function to get the inactive users email
    twelve_hours_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
    with app.app_context():
        users = User.query.all()
    user_data = []
    for user in users:
        user_data.append({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'password': user.password,
            'last_access': user.last_access
        })
    df = pd.DataFrame(user_data)
    df['last_access'] = pd.to_datetime(df['last_access'])
    # print(df.head())
    filtered_emails = df[(df['last_access'] < twelve_hours_ago) | pd.isnull(df['last_access'])]['email'].tolist()
    
    return filtered_emails, 200


def send_email_to_inactive_users(email_list):#function to send email to inactive users
    # code to send the email to the inactive users
    subject = "🎉 Your Entertainment Awaits! Exclusive Offers Inside!"
    body = """
            <!DOCTYPE html>
            <html>
            <head>
              <!-- Add Bootstrap CSS link here -->
              <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            </head>
            <body>

            <div class="container">
              <div class="jumbotron mt-4">

                <p class="lead">Hey,</p>
                <p>Missed you on our platform! 🌟 Your ticket to excitement and fun is still here, waiting for you. 🎭 Don't miss out on electrifying events and jaw-dropping offers!</p>
                <ul>
                  <li>🎁 Exclusive deals just for you!</li>
                  <li>📣 Unforgettable experiences!</li>
                </ul>
                <p>Let's make memories together! 🌈</p>
                <p>Best regards,<br>Team</p>
                <a href="http://localhost:8080/" class="btn btn-primary btn-lg">Click here to book now</a>
              </div>
            </div>

            <!-- Add Bootstrap JS and jQuery script links here, if needed -->
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>

            </body>
            </html>
    """
    print(email_list)
    send_email_function(subject, body, email_list)
    # print(email_list)


def get_user_ids():#function to get the user ids
    with app.app_context():
        users = User.query.all()
    user_ids = [user.id for user in users]
    user_emails = [user.email for user in users]
    # print(user_ids)
    return user_ids,user_emails
    

def get_bookings_for_user(user_id):#function to get the bookings for the user
    # print(get_current_month())
    month=get_current_month()
    with app.app_context():
        bookings=Booking.query.filter(Booking.user_id==user_id,Booking.booking_date.like(f'{month}%')).all()
    return bookings

def send_entertainment_report(user_ids,user_emails):#function to send the entertainment report
    for id,email in zip(user_ids,user_emails):
        print(id)
        bookings=get_bookings_for_user(id)
        user_bookings = []
        for booking in bookings:
            user_bookings.append({
                
                'show_name': get_show_name(booking.show_id),
                'theater_name': get_theater(booking.theater_id),
                'date': booking.booking_date,
                'time': booking.booking_time,
                'seats': booking.num_seats_booked,
                'amount': booking.total_price
            })
        df = pd.DataFrame(user_bookings)
        print(email)
        # print(df)
        subject = "Your Monthly Entertainment Report "
        table_rows = "".join([f"""<tr>
                            <td>{ booking.show_name }</td>
                            <td>{ booking.theater_name }</td>
                            <td>{ booking.date }</td>
                            <td>{ booking.time }</td>
                            <td>{ booking.seats }</td>
                            <td>{ booking.amount }</td>
                        </tr>"""
                      for _, booking in df.iterrows()])
        no_bookings_message = "<p>You have not booked anything this month. 😔</p>" if df.shape[0] == 0 else ""
        body = f"""<!DOCTYPE html>
                   <html>
                   <head>
                     <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
                   </head>
                   <body>
                     <div class="container">
                       <div class="jumbotron mt-4">
                         <p class="lead">Hello,</p>
                         <p>Here are your entertainment bookings for the month:</p>
                         {no_bookings_message}
                         <div class="table-responsive">
                           <table class="table table-bordered">
                             <thead>
                               <tr>
                                 <th>Show Name</th>
                                 <th>Theater Name</th>
                                 <th>Date</th>
                                 <th>Time</th>
                                 <th>Seats</th>
                                 <th>Amount</th>
                               </tr>
                             </thead>
                             <tbody>
                               {table_rows}
                             </tbody>
                           </table>
                         </div>
                         <p>Thank you for choosing our platform for your entertainment needs. We hope you had a great time!</p>
                         <p>Best regards,<br>Team</p>
                       </div>
                     </div>
                   </body>
                   </html>"""
        # print(body)
        email_list=[]
        email_list.append(email)
        print(email_list)
        send_email_function(subject, body, email_list)
       

def generate_theater_report(id):#function to generate the theater report
    with app.app_context():
        theaters = Theaters.query.filter(Theaters.id == id).all()
        relations = ShowTheaterRelation.query.filter(ShowTheaterRelation.theater_id == id).all()
    theater_name = theaters[0].name
    theater_place = theaters[0].place
    theater_capacity = theaters[0].capacity
    theater_capacity_booked = theaters[0].capacity_booked
    theater_rating = theaters[0].rating
    total_shows = len(relations)
    print(theater_name, theater_place, theater_capacity, theater_capacity_booked, theater_rating, total_shows)
    return theater_name, theater_place, theater_capacity, theater_capacity_booked, theater_rating, total_shows


def send_theater_report(id):#function to send the theater report
    theater_name, theater_place, theater_capacity, theater_capacity_booked, theater_rating, total_shows = generate_theater_report(id)
    data={
        'theater_name':theater_name,
        'theater_place':theater_place,
        'theater_capacity':theater_capacity,
        'theater_capacity_booked':theater_capacity_booked,
        'theater_rating':theater_rating,
        'total_shows':total_shows
    }
    df=pd.DataFrame(data,index=[0])
    df.to_csv(f'attachments/theater_report_{theater_name}.csv',index=False)
    subject = f"Theater Report for {theater_name}"
    body = f"""<!DOCTYPE html>
                <html>
                <head>
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
                </head>
                <body>
                    <div class="container">
                        <div class="jumbotron mt-4">
                            <p class="lead">Hello,</p>
                            <p>Here is the report for the theater:</p>
                            <div class="table-responsive">
                                <table class="table table-bordered">
                                    <thead>
                                        <tr>
                                            <th>Name</th>   
                                            <th>Place</th>
                                            <th>Capacity</th>
                                            <th>Capacity Booked</th>
                                            <th>Rating</th>
                                            <th>Total Shows</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>{theater_name}</td> 
                                            <td>{theater_place}</td>
                                            <td>{theater_capacity}</td>
                                            <td>{theater_capacity_booked}</td>
                                            <td>{theater_rating}</td>
                                            <td>{total_shows}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <p>Thank you for choosing our platform for your entertainment needs. We hope you had a great time!</p>
                            <p>Best regards,<br>Team</p>
                        </div>
                    </div>
                </body>
                </html>"""
    email_list=['sachin@admin.com']
    send_email_function(subject, body, email_list,attachment_filename='theater_report.csv')
    