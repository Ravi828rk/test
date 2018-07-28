from root import app, db
from root.models import User, Notification, Message


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Message': Message,
            'Notification': Notification}


if __name__ == '__main__':
    app.run(debug=True)
