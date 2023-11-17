from workers import celery
import time
from datetime import datetime
from app import app
from task_supporting_functions import get_inactive_users_email,get_user_ids,send_email_to_inactive_users,send_entertainment_report,get_current_month,get_show_name,generate_theater_report,send_theater_report





@celery.task()#task to expert the theater report
def export_csv(id):
    # time.sleep(5) 
    send_theater_report(id)
    return 'Done'

from celery.schedules import crontab
print("crontab ", crontab)


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, send_email_to_inactive_users_task.s(), name='send_email_to_inactive_users', expires=60)
    sender.add_periodic_task(60.0, send_monthly_report.s(), name='send_monthly_report', expires=60)

    # sender.add_periodic_task(
    #     crontab(hour=18, minute=30,),
    #     send_mail_to_inactive_users.s,
    # )
    # sender.add_periodic_task(
    # crontab(day_of_month="1", hour=10, minute=30,),
    # send_monthly_report.s(),
    #     )



@celery.task()#task to send email to inactive users
def send_email_to_inactive_users_task():
    print("START")
    inactive_users_email=get_inactive_users_email()
    print('fetched inactive users email:::::::',inactive_users_email[0])
    send_email_to_inactive_users(inactive_users_email[0])
    print("COMPLETE")



@celery.task()#task to send monthly report
def send_monthly_report():
    user_ids,user_emails=get_user_ids()
    print('got user ids')
    send_entertainment_report(user_ids,user_emails)
    print('completed sending monthly report')


