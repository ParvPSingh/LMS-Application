from application.database import db
from flask_security import UserMixin, RoleMixin

class RolesUsers(db.Model):
    __tablename__ = 'RolesUsers'
    ru_id = db.Column(db.Integer(), primary_key=True)
    ru_user_id = db.Column('user_id', db.Integer(), db.ForeignKey('User.id'))
    ru_role_id = db.Column('role_id', db.Integer(), db.ForeignKey('Role.id'))

class Role(db.Model, RoleMixin):
    __tablename__="Role"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(25), unique=True, nullable=False)
    description=db.Column(db.String(255), unique=True, nullable=False)

class User(db.Model, UserMixin):
    __tablename__="User"
    id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    name=db.Column(db.String(25), unique=True)
    email=db.Column(db.String(25), unique=True, nullable=False)
    password=db.Column(db.String(25), unique=True, nullable=False)
    active=db.Column(db.Boolean)
    fs_uniquifier=db.Column(db.String(25), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='RolesUsers', backref=db.backref('users', lazy='dynamic'))
    requests = db.relationship('Book', secondary='Request', backref=db.backref('users', lazy='dynamic'))
    feedback = db.relationship('Book', secondary='Feedback', backref=db.backref('user_feedback', lazy='dynamic'))
    Section=db.relationship("Section", backref="librarian", lazy=True)
    Book=db.relationship("Book", backref="user", lazy=True)


class Section(db.Model):
    __tablename__="Section"
    sec_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    sec_name=db.Column(db.String(25), nullable=False)
    sec_create_date=db.Column(db.DateTime, nullable=False)
    sec_description=db.Column(db.String(525))
    sec_user_id = db.Column(db.Integer, db.ForeignKey('User.id'),nullable=False)
    books=db.relationship("Book", backref="section", cascade="all, delete", lazy=True)

class Request(db.Model):
    __tablename__="Request"
    req_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    req_user_id = db.Column(db.Integer, db.ForeignKey('User.id'),nullable=False)
    req_book_id = db.Column(db.Integer, db.ForeignKey('Book.book_id'),nullable=False)
    req_create_date=db.Column(db.DateTime, nullable=False)
    req_start_date=db.Column(db.DateTime, nullable=False)
    req_end_date=db.Column(db.DateTime, nullable=False)
    req_active=db.Column(db.Boolean, nullable=False ,default=True)


class Book(db.Model):
    __tablename__="Book"
    book_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_name=db.Column(db.String(25), nullable=False)
    book_content=db.Column(db.String(125))
    book_author=db.Column(db.String(25))
    book_link=db.Column(db.String(),  default='https://www.isibang.ac.in/~athreya/psweur/')
    book_create_date=db.Column(db.DateTime, nullable=False)
    book_available=db.Column(db.Boolean, nullable=False, default=True)
    book_user_id = db.Column(db.Integer, db.ForeignKey('User.id'),nullable=True)
    book_sec_id = db.Column(db.Integer, db.ForeignKey('Section.sec_id'),nullable=False)

class Feedback(db.Model):
    __tablename__="Feedback"
    feed_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    feed_user_id = db.Column(db.Integer, db.ForeignKey('User.id'),nullable=False)
    feed_book_id = db.Column(db.Integer, db.ForeignKey('Book.book_id'),nullable=False)
    feed_rating=db.Column(db.Integer, nullable=False)
    feed_content=db.Column(db.String, nullable=False)
