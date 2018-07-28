import jwt
import json
from time import time
from datetime import datetime
from root import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140), nullable=False, unique=True)
    email = db.Column(db.String(140), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(120), default='default.jpg', nullable=False)
    resume = db.Column(db.String(120), default='default.pdf', nullable=False)

    # personal details
    name = db.Column(db.String(40))
    mobile = db.Column(db.String(14))
    phone = db.Column(db.String(14))
    dob = db.Column(db.String(20))
    address = db.Column(db.String(200))
    hobbies = db.Column(db.String(100))
    country = db.Column(db.String(30))
    city = db.Column(db.String(30))

    # for Messages
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='author', lazy='dynamic')
    messages_received = db.relationship('Message', foreign_keys='Message.recipient_id', backref='recipient',
                                        lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)

    notifications = db.relationship('Notification', backref='user', lazy='dynamic')

    # for resume
    resume_details = db.relationship('Resume', backref='resume_details', lazy='dynamic')

    # add notification
    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n

    # for getting new Messages
    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(Message.timestamp > last_read_time).count()

    # for password reset
    def get_reset_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, app.config['SECRET_KEY'],
                          algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        try:
            print(token)
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.query.get(id)

    def __repr__(self):
        return "{0.username} - {0.email}".format(self)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(240))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))


class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category = db.Column(db.String(40), index=True)
    year = db.Column(db.String(30), index=True)
    title = db.Column(db.String(300), index=True)
    sub_title = db.Column(db.String(300), index=True)
    body = db.Column(db.String(800))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "{0.user_id} - {0.body}".format(self)
