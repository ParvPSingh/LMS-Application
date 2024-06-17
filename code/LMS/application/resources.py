from flask_restful import Resource, fields, marshal_with, reqparse, Api
from application.database import db
from application.models import User, Section, Book, Request, Feedback
from application.validation import ValidationError
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, auth_required, roles_required
from application.sec import datastore
from flask import jsonify
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

api=Api()

user_out_fields={"id": fields.Integer, "name": fields.String, "email": fields.String, "password": fields.String, "active": fields.Boolean, "fs_uniquifier":fields.String, "roles":fields.List(fields.String)}
section_out_fields={"sec_id": fields.Integer, "sec_name": fields.String, "sec_create_date": fields.DateTime, "sec_description": fields.String, "sec_user_id": fields.Integer}
book_out_fields={"book_id": fields.Integer, "book_name": fields.String, "book_author": fields.String, "book_content": fields.String, "book_available": fields.Boolean, "book_create_date": fields.DateTime, "book_user_id": fields.Integer, "book_sec_id": fields.Integer}
request_out_fields={"request_id": fields.Integer, "req_user_id": fields.Integer, "req_book_id": fields.Integer, "req_create_date": fields.DateTime, "req_start_date": fields.DateTime, "req_end_date": fields.DateTime, "req_active": fields.Boolean}
feed_out_fields={"feed_id": fields.Integer, "feed_user_id": fields.Integer, "feed_book_id": fields.Integer, "feed_rating": fields.Integer, "feed_content": fields.String}

create_user_parser=reqparse.RequestParser()
create_user_parser.add_argument("id")
create_user_parser.add_argument("name")
create_user_parser.add_argument("email")
create_user_parser.add_argument("password")
create_user_parser.add_argument("active")
create_user_parser.add_argument("fs_uniquifier")

create_sec_parser=reqparse.RequestParser()
create_sec_parser.add_argument("sec_id")
create_sec_parser.add_argument("sec_name")
create_sec_parser.add_argument("sec_create_date")
create_sec_parser.add_argument("sec_description")
create_sec_parser.add_argument("sec_user_id")
update_sec_parser=reqparse.RequestParser()
update_sec_parser.add_argument("sec_name")
update_sec_parser.add_argument("sec_description")

create_book_parser=reqparse.RequestParser()
create_book_parser.add_argument("book_id")
create_book_parser.add_argument("book_name")
create_book_parser.add_argument("book_content")
create_book_parser.add_argument("book_author")
create_book_parser.add_argument("book_available")
create_book_parser.add_argument("book_create_date")
create_book_parser.add_argument("book_user_id")
create_book_parser.add_argument("book_sec_id")
update_book_parser=reqparse.RequestParser()
update_book_parser.add_argument("book_id")
update_book_parser.add_argument("book_name")
update_book_parser.add_argument("book_content")
update_book_parser.add_argument("book_author")
update_book_parser.add_argument("book_available")
update_book_parser.add_argument("book_user_id")
update_book_parser.add_argument("book_sec_id")

create_request_parser=reqparse.RequestParser()
create_request_parser.add_argument("req_id")
create_request_parser.add_argument("req_user_id")
create_request_parser.add_argument("req_book_id")
create_request_parser.add_argument("req_create_date")
create_request_parser.add_argument("req_start_date")
create_request_parser.add_argument("req_end_date")
create_request_parser.add_argument("req_active")

create_feedback_parser=reqparse.RequestParser()
create_feedback_parser.add_argument("feed_id")
create_feedback_parser.add_argument("feed_user_id")
create_feedback_parser.add_argument("feed_book_id")
create_feedback_parser.add_argument("feed_rating")
create_feedback_parser.add_argument("feed_content")

class UserAPI(Resource):
    @auth_required('token')
    @marshal_with(user_out_fields)
    def get(self, username):
        now_user=User.query.filter_by(name=username).first()
        if now_user:
            return now_user, 200
        else:
            raise ValidationError(status_code=404, error_code="UVE1001", error_message="user doesn't exist")

    @marshal_with(user_out_fields)
    def post(self):
        args=create_user_parser.parse_args()
        name=args.get("name", None)
        email=args.get("email",None)
        password=args.get("password",None)
        print(name)
        if "@" not in email:
            raise ValidationError(status_code=400, error_code="UVE1006", error_message="Not a valid email")
        if len(password)<7:
            raise ValidationError(status_code=400, error_code="UVE1007", error_message="Password should have atleast 8 letters")
        if name is None:
            raise ValidationError(status_code=400, error_code="UVE1002", error_message="username is required")
        if password is None:
            raise ValidationError(status_code=400, error_code="UVE1003", error_message="password is required")
        
        now_user_name=User.query.filter_by(name=name).first()
        if now_user_name:
            raise ValidationError(status_code=400, error_code="UVE1004", error_message="duplicate username")
        
        if not datastore.find_user(email=email):
            new_user=datastore.create_user(name=name, email=email, password=generate_password_hash(password, method="sha256"), roles=['user'])
        db.session.commit()

        return new_user, 201

from .instances import cache

class SectionAPI(Resource):
    @auth_required('token')
    @roles_required("librarian")
    @marshal_with(section_out_fields)
    @cache.cached(timeout=50, query_string=True)
    def get(self, sec_id):
        sec_list=Section.query.filter_by(sec_id=sec_id).first()
        if sec_list:
            return sec_list, 200
        else:
            raise ValidationError(status_code=404, error_code="SVE1001", error_message="section doesn't exist")

    @auth_required('token')
    @roles_required("librarian")
    @marshal_with(section_out_fields)
    @cache.cached(timeout=50, query_string=True)
    def post(self):
        args=create_sec_parser.parse_args()
        sec_name=args.get("sec_name", None)
        sec_description=args.get("sec_description", None)
        sec_user_id=args.get("sec_user_id", None)
        sec_create_date=datetime.today()

        if sec_name is None:
            raise ValidationError(status_code=400, error_code="SVE1002", error_message="section name is required")
        if sec_user_id is None:
            raise ValidationError(status_code=400, error_code="SVE1003", error_message="section user_id is required")

        new_sec=Section(sec_name=sec_name, sec_description=sec_description, sec_user_id=sec_user_id, sec_create_date=sec_create_date)
        db.session.add(new_sec)
        db.session.commit()

        return new_sec, 201

    @auth_required('token')
    @roles_required("librarian")
    @marshal_with(section_out_fields)
    @cache.cached(timeout=50, query_string=True)
    def put(self, sec_id):
        args=update_sec_parser.parse_args()
        sec_name=args.get("sec_name", None)
        sec_description=args.get("sec_description", None)

        if sec_name is None:
            raise ValidationError(status_code=400, error_code="SVE1002", error_message="section name is required")

        new_sec=Section.query.filter_by(sec_id=sec_id).first()
        new_sec.sec_name=sec_name
        new_sec.sec_description=sec_description
        db.session.commit()

        return new_sec, 201

    @auth_required('token')
    @roles_required("librarian")
    @cache.cached(timeout=50, query_string=True)
    def delete(self, sec_id):
        now_sec=Section.query.filter_by(sec_id=sec_id).first()
        if now_sec is None:
            raise ValidationError(status_code=404, error_code="SVE1001", error_message="section doesn't exist")
        db.session.delete(now_sec)
        db.session.commit()
        return "", 200

class BookAPI(Resource):
    @auth_required('token')
    @roles_required("librarian")
    @marshal_with(book_out_fields)
    @cache.cached(timeout=50, query_string=True)
    def get(self, book_id):
        now_book=Book.query.filter_by(book_id=book_id).first()
        if now_book:
            return now_book, 200
        else:
            raise ValidationError(status_code=404, error_code="BVE1001", error_message="book doesn't exist")

    @auth_required('token')
    @roles_required("librarian")
    @marshal_with(book_out_fields)
    @cache.cached(timeout=50, query_string=True)
    def post(self):
        args=create_book_parser.parse_args()
        book_name=args.get("book_name", None)
        book_content=args.get("book_content", None)
        book_author=args.get("book_author", None)
        book_available=True
        book_create_date=datetime.today()
        book_user_id=args.get("book_user_id", None)
        book_sec_id=args.get("book_sec_id", None)

        if book_name is None:
            raise ValidationError(status_code=400, error_code="BVE1001", error_message="book name is required")
        if book_author is None:
            raise ValidationError(status_code=400, error_code="BVE1002", error_message="book author is required")
        if book_sec_id is None:
            raise ValidationError(status_code=400, error_code="BVE1003", error_message="book section id is required")
        if book_available is None:
            raise ValidationError(status_code=400, error_code="BVE1004", error_message="book availability is required")
        bok = Book.query.filter_by(book_name=book_name, book_author=book_author).first()
        if (bok):
            raise ValidationError(status_code=400, error_code="BVE1005", error_message="You cannot make a duplicate book!")            

        new_book=Book(book_name=book_name, book_content=book_content, book_available=book_available, book_author=book_author, book_create_date=book_create_date, book_user_id=book_user_id, book_sec_id=book_sec_id)
        db.session.add(new_book)
        db.session.commit()

        return new_book, 201

    @auth_required('token')
    @roles_required("librarian")
    @marshal_with(book_out_fields)
    @cache.cached(timeout=50, query_string=True)
    def put(self, book_id):
        args=update_book_parser.parse_args()
        book_name=args.get("book_name", None)
        book_author=args.get("book_author", None)
        book_content=args.get("book_content", None)
        book_available=args.get("book_available", None)
        if book_available=='True':
            book_available=True
        else:
            book_available=False
        book_user_id=args.get("book_user_id", None)
        book_sec_id=args.get("book_sec_id", None)

        if book_name is None:
            raise ValidationError(status_code=400, error_code="BVE1002", error_message="book name is required")
        if book_author is None:
            raise ValidationError(status_code=400, error_code="BVE1003", error_message="book author is required")
        if book_sec_id is None:
            raise ValidationError(status_code=400, error_code="BVE1004", error_message="book section id is required")
        if book_user_id is None:
            raise ValidationError(status_code=400, error_code="BVE1005", error_message="book user id is required")
        if book_available is None:
            raise ValidationError(status_code=400, error_code="BVE1005", error_message="book availability is required")
        new_book=Book.query.filter_by(book_id=book_id).first()
        new_book.book_name=book_name
        new_book.book_content=book_content
        new_book.book_author=book_author
        new_book.book_user_id=book_user_id
        new_book.book_sec_id=book_sec_id
        new_book.book_available=book_available
        db.session.commit()

        return new_book, 201

    @auth_required('token')
    @roles_required("librarian")
    @cache.cached(timeout=50, query_string=True)
    def delete(self, book_id):
        now_book=Book.query.filter_by(book_id=book_id).first()
        if now_book is None:
            raise ValidationError(status_code=404, error_code="BVE1001", error_message="book doesn't exist")
        db.session.delete(now_book)
        db.session.commit()
        return "", 200
    
class RequestAPI(Resource):
    @auth_required('token')
    @marshal_with(request_out_fields)
    @cache.cached(timeout=50, query_string=True)
    def get(self, req_id):
        now_req=Request.query.filter_by(req_id=req_id).first()
        if now_req:
            return now_req, 200
        else:
            raise ValidationError(status_code=404, error_code="RVE1001", error_message="request doesn't exist")


    @marshal_with(request_out_fields)
    @cache.cached(timeout=50, query_string=True)
    def post(self):
        args=create_request_parser.parse_args()
        req_user_id=args.get("req_user_id", None)
        req_book_id=args.get("req_book_id", None)
        req_create_date=datetime.today()
        req_start_date=datetime.today()
        req_end_date=req_start_date+timedelta(days=7)
        req_active=True

        book = Book.query.filter_by(book_user_id=req_user_id, book_id=req_book_id).first()
        if book is not None:
            raise ValidationError(status_code=400, error_code="RVE1002", error_message="You have already made this request!")
        
        books_have = Book.query.filter_by(book_user_id=req_user_id).all()
        if(len(books_have)==5):
            raise ValidationError(status_code=400, error_code="RVE1005", error_message="You already have 5 books issued!")

        if req_user_id is None:
            raise ValidationError(status_code=400, error_code="RVE1001", error_message="user id is required")
        if req_create_date is None:
            raise ValidationError(status_code=400, error_code="RVE1003", error_message="Creation date is required")
        if req_end_date is None:
            raise ValidationError(status_code=400, error_code="RVE1004", error_message="End date is required")
            
        new_req=Request(req_user_id=req_user_id, req_book_id=req_book_id, req_active=req_active, req_create_date=req_create_date, req_start_date=req_start_date, req_end_date=req_end_date)
        db.session.add(new_req)
        db.session.commit()

        return new_req, 201
    
    @auth_required('token')
    @roles_required("librarian")
    @cache.cached(timeout=50, query_string=True)
    def delete(self, req_id):
        now_req=Request.query.filter_by(req_id=req_id).first()
        if now_req is None:
            raise ValidationError(status_code=404, error_code="RVE1001", error_message="request doesn't exist")
        db.session.delete(now_req)
        db.session.commit()
        return "", 200
    
class FeedbackAPI(Resource):
    @auth_required('token')
    @marshal_with(feed_out_fields)
    @cache.cached(timeout=50, query_string=True)
    def get(self, feed_id):
        now_req=Request.query.filter_by(feed_id=feed_id).first()
        if feed_id:
            return now_req, 200
        else:
            raise ValidationError(status_code=404, error_code="FVE1001", error_message="feedback doesn't exist")


    @marshal_with(feed_out_fields)
    @cache.cached(timeout=50, query_string=True)
    def post(self, book_id):
        args=create_feedback_parser.parse_args()
        feed_user_id=args.get("feed_user_id", None)
        feed_book_id=book_id
        feed_rating=args.get("feed_rating", None)
        feed_content=args.get("feed_content", None)

        feedback = Feedback.query.filter_by(feed_user_id=feed_user_id, feed_book_id=feed_book_id).first()
        if feedback is not None:
            raise ValidationError(status_code=400, error_code="FVE1002", error_message="You have already given feedback for this book!")

        if feed_rating is None:
            raise ValidationError(status_code=400, error_code="FVE1001", error_message="rating is required")
        if feed_content is None:
            raise ValidationError(status_code=400, error_code="RVE1003", error_message="feedback is required")
            
        new_feed=Feedback(feed_user_id=feed_user_id, feed_book_id=feed_book_id, feed_rating=feed_rating, feed_content=feed_content)
        db.session.add(new_feed)
        db.session.commit()

        return new_feed, 201
    
    @auth_required('token')
    @roles_required("librarian")
    @cache.cached(timeout=50, query_string=True)
    def delete(self, feed_id):
        now_feed=Feedback.query.filter_by(feed_id=feed_id).first()
        if now_feed is None:
            raise ValidationError(status_code=404, error_code="FVE1001", error_message="feedback doesn't exist")
        db.session.delete(now_feed)
        db.session.commit()
        return "", 200
    
class SummaryAPI(Resource):
    @auth_required("token")
    @roles_required("librarian")
    @cache.cached(timeout=50, query_string=True)
    def get(self):
        books = Book.query.all()
        requests = Request.query.all()
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
        plt.savefig("frontend/src/assets/graph_librarian_book_authors_dist.png")
        plt.close()
        book_genres_dict = Counter(book_genres)
        namesBookGenre=list(book_genres_dict.keys())
        valuesBookGenre=list(book_genres_dict.values())
        plt.pie(valuesBookGenre, labels=namesBookGenre)
        plt.savefig("frontend/src/assets/graph_librarian_book_genres_dist.png")
        plt.close()
        book_avails_dict = Counter(book_avails)
        namesBookAvails=list(book_avails_dict.keys())
        valuesBookAvails=list(book_avails_dict.values())
        plt.pie(valuesBookAvails, labels=namesBookAvails)
        plt.savefig("frontend/src/assets/graph_librarian_book_availability_dist.png")
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
        plt.savefig("frontend/src/assets/graph_librarian_active_requests.png")
        plt.close()
        result = [no_of_books, no_of_requests, req_deadlines]
        return jsonify(result)


api.add_resource(UserAPI, "/api/user/<string:username>", "/api/user")
api.add_resource(SectionAPI, "/api/sec/<int:sec_id>", "/api/sec")
api.add_resource(BookAPI, "/api/book/<int:book_id>", "/api/book")
api.add_resource(RequestAPI, "/api/req/<int:req_id>", "/api/req")
api.add_resource(FeedbackAPI, "/api/feed/<int:feed_id>", "/api/feed/book/<int:book_id>")
api.add_resource(SummaryAPI, "/api/sum")