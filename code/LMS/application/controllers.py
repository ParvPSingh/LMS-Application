from flask import current_app as app, jsonify, request, render_template, send_file
from flask_security import auth_required, roles_required
from werkzeug.security import check_password_hash
from .sec import datastore
from application.models import User, Section, Request, Book, Feedback
from flask_restful import fields, marshal
from datetime import datetime, timedelta
from application.database import db
from collections import Counter
# from application.tasks import say_hello
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from .instances import cache
from sqlalchemy import and_

@app.get('/')
def home():
    return render_template("index.html")

@app.get('/librarian')
@auth_required("token")
@roles_required("librarian")
def librarian():
    return 'Yo librarian!!!'

@app.post('/login_user')
def user_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email:
        return jsonify({"error_message": "email is not provided"}), 400
    if not password:
        return jsonify({"error_message": "password is not provided"}), 400

    user = datastore.find_user(email=email)

    if not user:
        return jsonify({"error_message": "User was Not Found"}), 404
    
    if (user.active==False):
        return jsonify({"error_message": "You don't have access to the website"}), 401

    if check_password_hash(user.password, data.get("password")):
        return jsonify({"name": user.name, "token": user.get_auth_token(), "email": user.email, "role": user.roles[0].name, "user_id": user.id, "active": user.active})
    else:
        return jsonify({"error_message": "Wrong Password"}), 400
    
book_out_fields={"book_id": fields.Integer, "book_name": fields.String, "book_author": fields.String, "book_content": fields.String, "book_available": fields.Boolean, "book_create_date": fields.DateTime, "book_user_id": fields.Integer, "book_sec_id": fields.Integer}    
@app.get('/all_books')
@auth_required("token")
def all_books():
    available_books=Book.query.filter_by(book_available=True).all()
    unavailable_books=Book.query.filter_by(book_available=False).all()
    if len(available_books) == 0 and len(unavailable_books)==0:
        return jsonify({"error_message": "No Book Found"}), 404
    return [marshal(available_books,book_out_fields), marshal(unavailable_books,book_out_fields)]

@app.get('/all_books_search/<book_name>')
@auth_required("token")
def all_books_search(book_name):
    if book_name==None:
        return jsonify({"error_message": "No Book Found"}), 404
    available_books = Book.query.filter(and_(Book.book_name.ilike(f'%{book_name}%'), Book.book_available == True)).all()
    unavailable_books = Book.query.filter(and_(Book.book_name.ilike(f'%{book_name}%'), Book.book_available == False)).all()
    if len(available_books) == 0 and len(unavailable_books)==0:
        return jsonify({"error_message": "No Book Found"}), 404
    return [marshal(available_books,book_out_fields), marshal(unavailable_books,book_out_fields)]

new_book_out_fields={"book_id": fields.Integer, "book_name": fields.String, "book_author": fields.String, "book_link": fields.String, "book_content": fields.String, "book_available": fields.Boolean, "book_create_date": fields.DateTime, "book_user_id": fields.Integer, "book_sec_id": fields.Integer}    
@app.get('/my_books/<int:book_user_id>')
@auth_required("token")
def get_my_books(book_user_id):
    my_books=Book.query.filter_by(book_user_id=book_user_id).all()
    if len(my_books)==0:
        return jsonify({"error_message": "No Book Found"}), 404
    for book in my_books:
        now_req = Request.query.filter_by(req_user_id=book_user_id, req_book_id=book.book_id).first()
        if(now_req.req_end_date<datetime.today()):
            book.book_user_id=None
            book.book_available=False
            db.session.commit()
    my_books=Book.query.filter_by(book_user_id=book_user_id).all()
    return marshal(my_books,new_book_out_fields)

@app.put('/return_book/<int:book_id>')
@auth_required("token")
def return_book(book_id):
    ret_book=Book.query.filter_by(book_id=book_id).first()
    if (ret_book):
        ret_book.book_user_id=None
        db.session.commit()
        return jsonify({"error_message": "Book Returned"}), 200
    return jsonify({"error_message": "No Book Found"}), 404

@app.get('/all_books_sectionwise/<int:sec_id>')
@auth_required("token")
def all_books_sectionwise(sec_id):
    available_sec_books=Book.query.filter_by(book_sec_id=sec_id, book_available=True).all()
    unavailable_sec_books=Book.query.filter_by(book_sec_id=sec_id, book_available=False).all()
    if len(available_sec_books) == 0 and len(unavailable_sec_books)==0:
        return jsonify({"error_message": "No Book Found"}), 404
    return [marshal(available_sec_books,book_out_fields), marshal(unavailable_sec_books,book_out_fields)]

@app.get('/all_books_sectionwise_search/<int:sec_id>/<book_name>')
@auth_required("token")
def all_books_sectionwise_search(book_name, sec_id):
    if book_name==None:
        return jsonify({"error_message": "No Book Found"}), 404
    available_books = Book.query.filter(and_(Book.book_sec_id == sec_id, Book.book_name.ilike(f'%{book_name}%'), Book.book_available == True)).all()
    unavailable_books = Book.query.filter(and_(Book.book_sec_id == sec_id, Book.book_name.ilike(f'%{book_name}%'), Book.book_available == False)).all()
    if len(available_books) == 0 and len(unavailable_books)==0:
        return jsonify({"error_message": "No Book Found"}), 404
    return [marshal(available_books,book_out_fields), marshal(unavailable_books,book_out_fields)]

section_out_fields={"sec_id": fields.Integer, "sec_name": fields.String, "sec_create_date": fields.DateTime, "sec_description": fields.String, "sec_user_id": fields.Integer}
@app.get('/all_sections')
@auth_required("token")
def all_sections():
    all_sections=Section.query.all()
    if len(all_sections)==0:
        return jsonify({"error_message": "No Section Found"}), 404
    return marshal(all_sections,section_out_fields)

@app.get('/all_sections_search/<sec_name>')
@auth_required("token")
def all_sections_search(sec_name):
    if sec_name==None or sec_name=='':
        return jsonify({"error_message": "No Genre Found"}), 404
    all_sections=Section.query.filter(Section.sec_name.ilike(f'%{sec_name}%')).all()
    if len(all_sections)==0:
        return jsonify({"error_message": "No Genre Found"}), 404
    return marshal(all_sections,section_out_fields)

@app.get('/all_feedback')
@auth_required("token")
def all_feedback():
    all_feedback=Feedback.query.all()
    if len(all_feedback)==0:
        return jsonify({"error_message": "No Feedback Found"}), 404
    res = []
    for feedback in all_feedback:
        feed_book = Book.query.filter_by(book_id=feedback.feed_book_id).first()
        feed_user = User.query.filter_by(id=feedback.feed_user_id).first()
        feed_data = {
            "feed_id": feedback.feed_id,
            "book_name": feed_book.book_name,
            "user_name": feed_user.name,
            "book_id": feedback.feed_book_id,
            "user_id": feedback.feed_user_id,
            "rating": feedback.feed_rating,
            "content": feedback.feed_content
        }
        res.append(feed_data)
    return jsonify(res)

@app.get('/all_requests')
@auth_required("token")
@roles_required("librarian")
def all_requests():
    active_requests = Request.query.filter_by(req_active=True).all()
    inactive_requests = Request.query.filter_by(req_active=False).all()
    active_req_list = []
    inactive_req_list = []

    
    for request in active_requests:
        req_book = Book.query.filter_by(book_id=request.req_book_id).first()
        req_user = User.query.filter_by(id=request.req_user_id).first()
        req_data = {
            "req_id": request.req_id,
            "book_name": req_book.book_name,
            "user_name": req_user.name,
            "book_id": request.req_book_id,
            "user_id": request.req_user_id,
            "req_active": request.req_active
        }
        active_req_list.append(req_data)
    for request in inactive_requests:
        req_book = Book.query.filter_by(book_id=request.req_book_id).first()
        req_user = User.query.filter_by(id=request.req_user_id).first()
        req_data = {
            "req_id": request.req_id,
            "book_name": req_book.book_name,
            "user_name": req_user.name,
            "book_id": request.req_book_id,
            "user_id": request.req_user_id,
            "req_active": request.req_active
        }
        inactive_req_list.append(req_data)
    req_list = [active_req_list, inactive_req_list]
    return jsonify(req_list)

@app.get('/my_requests/<int:user_id>')
@auth_required("token")
def my_requests(user_id):
    active_requests = Request.query.filter_by(req_active=True, req_user_id=user_id).all()
    inactive_requests = Request.query.filter_by(req_active=False, req_user_id=user_id).all()
    active_req_list = []
    inactive_req_list = []

    
    for request in active_requests:
        req_book = Book.query.filter_by(book_id=request.req_book_id).first()
        req_user = User.query.filter_by(id=request.req_user_id).first()
        req_data = {
            "req_id": request.req_id,
            "book_name": req_book.book_name,
            "user_name": req_user.name,
            "book_id": request.req_book_id,
            "user_id": request.req_user_id,
            "req_active": request.req_active
        }
        active_req_list.append(req_data)
    for request in inactive_requests:
        req_book = Book.query.filter_by(book_id=request.req_book_id).first()
        req_user = User.query.filter_by(id=request.req_user_id).first()
        req_data = {
            "req_id": request.req_id,
            "book_name": req_book.book_name,
            "user_name": req_user.name,
            "book_id": request.req_book_id,
            "user_id": request.req_user_id,
            "req_active": request.req_active
        }
        inactive_req_list.append(req_data)
    req_list = [active_req_list, inactive_req_list]
    return jsonify(req_list)

@app.put('/accept_req/<int:req_id>')
def accept_req(req_id):
    curr_req = Request.query.filter_by(req_id=req_id).first()
    if (curr_req):
        curr_book = Book.query.filter_by(book_id=curr_req.req_book_id).first()
        books_have = Book.query.filter_by(book_user_id=curr_req.req_user_id).all()
    if(len(books_have)==5):
        return jsonify({"error_message": "This user already has 5 books"}), 409
    if (curr_book):
        if(curr_book.book_user_id==None or curr_book.book_user_id==0):
            curr_book.book_user_id = curr_req.req_user_id
            curr_book.book_available = False
            curr_req.req_start_date = datetime.today()
            curr_req.req_end_date = datetime.today() + timedelta(days=7)
            curr_req.req_active = False
            db.session.commit()
            return jsonify({"error_message": "Request Accepted"}), 200
        else:
            return jsonify({"error_message": "Book issued to another user!"}), 409
    else:
        return jsonify({"error_message": "No Request Found"}), 404

@app.put('/revoke_book/<int:book_id>')
@auth_required("token")
@roles_required("librarian")
def revoke_book(book_id):
    book = Book.query.filter_by(book_id=book_id).first()
    if not book:
        return jsonify({"error_message": "Book not found"}), 404
    book.book_user_id = None
    book.book_available = True
    db.session.commit()
    return jsonify({"error_message": "Book Privileges Revoked"}), 200

@app.put('/revoke_user/<int:user_id>')
@auth_required("token")
@roles_required("librarian")
def revoke_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"error_message": "User not found"}), 404
    user.active = False
    db.session.commit()
    return jsonify({"error_message": "User Deactivated"}), 200

@app.put('/activate_user/<int:user_id>')
@auth_required("token")
@roles_required("librarian")
def activate_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"error_message": "User not found"}), 404
    user.active = True
    db.session.commit()
    return jsonify({"error_message": "User Activated"})

user_out_fields={"id": fields.Integer, "name": fields.String, "email": fields.String, "password": fields.String, "active": fields.Boolean, "fs_uniquifier":fields.String, "roles":fields.List(fields.String)}
@app.get('/all_users')
@auth_required("token")
@roles_required("librarian")
def all_users():
    users=User.query.all()
    if len(users) == 0:
        return jsonify({"error_message": "No Book Found"}), 404
    return marshal(users,user_out_fields)

# @app.get('/say_hello')
# def say_hello_view():
#     t = say_hello.delay()
#     return jsonify({"task_id": t.id})

@app.get('/summary/<int:user_id>')
@auth_required("token")
def summary(user_id):
    user = User.query.filter_by(id=user_id).first()
    books = Book.query.filter_by(book_user_id=user_id).all()
    requests = Request.query.filter_by(req_user_id=user_id).all()
    no_of_books = len(books)
    no_of_requests = len(requests)
    book_authors = []
    book_names = []
    book_genres = []
    book_avails = []
    for book in books:
        book_authors.append(book.book_author)
        book_names.append(book.book_name)
        book_genre = Section.query.filter_by(sec_id=book.book_sec_id).first()
        book_genres.append(book_genre.sec_name)
        book_avails.append(book.book_available)
    book_authors_dict = Counter(book_authors)
    namesBookAuth=list(book_authors_dict.keys())
    valuesBookAuth=list(book_authors_dict.values())
    plt.pie(valuesBookAuth, labels=namesBookAuth)
    plt.savefig("frontend/src/assets/graph_"+str(user.id)+"_book_authors_dist.png")
    plt.close()
    book_genres_dict = Counter(book_genres)
    namesBookGenre=list(book_genres_dict.keys())
    valuesBookGenre=list(book_genres_dict.values())
    plt.pie(valuesBookGenre, labels=namesBookGenre)
    plt.savefig("frontend/src/assets/graph_"+str(user.id)+"_book_genres_dist.png")
    plt.close()
    book_avails_dict = Counter(book_avails)
    namesBookAvails=list(book_avails_dict.keys())
    valuesBookAvails=list(book_avails_dict.values())
    plt.pie(valuesBookAvails, labels=namesBookAvails)
    plt.savefig("frontend/src/assets/graph_"+str(user.id)+"_book_availability_dist.png")
    plt.close()

    req_actives = []
    req_deadlines = []
    for request in requests:
        req_actives.append(request.req_active)
        req_book = Book.query.filter_by(book_id=request.req_book_id).first()
        req_book_name = req_book.book_name
        deadline = request.req_end_date
        format = '%Y-%m-%d %H:%M:%S'
        deadline_string = deadline.strftime(format)
        req_data = {
            "req_id": request.req_id,
            "book_name": req_book_name,
            "book_deadline": deadline_string,
        }
        req_deadlines.append(req_data)
    req_actives_dict = Counter(req_actives)
    namesReqActive=list(req_actives_dict.keys())
    valuesReqActive=list(req_actives_dict.values())
    plt.pie(valuesReqActive, labels=namesReqActive)
    plt.savefig("frontend/src/assets/graph_"+str(user.id)+"_active_requests.png")
    plt.close()
    result = [no_of_books, no_of_requests, req_deadlines]
    return jsonify(result), 200