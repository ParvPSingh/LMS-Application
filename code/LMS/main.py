from flask import Flask
from flask_cors import CORS
from application.models import db, User, Role
from config import DevelopmentConfig
from application.resources import api
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
from application.sec import datastore
from application.worker import celery_init_app
from celery.schedules import crontab
from application.tasks import reminder, reminder_webhook
from application.instances import cache

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    CORS(app, resources={r"/*":{'origins': "*"}})
    #CORS(app, resources={r"/*":{'origins': 'http://127.0.0.1:8080', "allow_headers":"Access-Control-Allow-Origin"}})
    db.init_app(app)
    api.init_app(app)
    cache.init_app(app)
    app.security = Security(app, datastore=datastore)
    with app.app_context():
        import application.controllers
    return app

app = create_app()
celery_app = celery_init_app(app)



@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(crontab(hour='*', minute='*', day_of_week='*'),reminder.s(),)
    sender.add_periodic_task(crontab(hour='*', minute='*', day_of_week='*'),reminder_webhook.s())

if __name__=='__main__':
    
    app.run(debug=True)