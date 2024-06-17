from main import app
from application.sec import datastore
from application.models import db
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    datastore.find_or_create_role(name='librarian', description='Librarian role found/created')
    datastore.find_or_create_role(name='user', description='User role found/created')
    db.session.commit()
    if not datastore.find_user(email='admin@gmail.com'):
        datastore.create_user(name='Librarian', email='admin@gmail.com', password=generate_password_hash('librarian', method="sha256"), roles=['librarian'])
    if not datastore.find_user(email='user@gmail.com'):
        datastore.create_user(name='User', email='user@gmail.com', password=generate_password_hash('useruser', method="sha256"), roles=['user'])
    db.session.commit()