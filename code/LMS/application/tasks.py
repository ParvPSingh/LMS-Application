from celery import shared_task
from .mail_service import send_message
import matplotlib.pyplot as plt
from application.models import User, Section, Request, Book
from collections import Counter
from jinja2 import Template
from .utils import webhook

@shared_task(ignore_result=True)
def reminder_webhook():
    users = User.query.all()
    
    for user in users:
        webhook(user.name)
        

@shared_task(ignore_result=True)
def reminder():
    users = User.query.all()
    for user in users:
        books = Book.query.filter_by(book_user_id=user.id).all()
        requests = Request.query.filter_by(req_user_id=user.id).all()
        no_of_books = len(books)
        no_of_requests = len(requests)

        req_deadlines = []
        for request in requests:
            req_book = Book.query.filter_by(book_id=request.req_book_id).first()
            req_book_name = req_book.book_name
            deadline = request.req_end_date
            deadline_string = deadline.strftime('%Y-%m-%d %H:%M:%S')
            req_data = {
                "req_id": request.req_id,
                "book_name": req_book_name,
                "book_deadline": deadline_string,
            }
            req_deadlines.append(req_data)
        
        
        from application.utils import generate_report_template
        rendered_template = generate_report_template(user.name, no_of_books, no_of_requests, req_deadlines)
        
        send_message(user.email, 'Your Library Report', rendered_template)
        print(f"Reminder Mail sent to {user.name}")
    
    return "OK"