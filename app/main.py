from flask import Flask, redirect, url_for, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from database_init import db
from models import Tasks

# Init
app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db.init_app(app)
 
with app.app_context():
    db.create_all()


# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sheduler', methods=['POST', 'GET'])
def sheduler():
    if request.method == 'POST':
        action_type = request.form['action_type']
        form_value = request.form['form_value']
        new_task = Tasks(task_type=action_type, task_value=form_value, task_result='Pending...')
        new_task.save_to_db()
        flash('Your request has been sended. Now you can look for it in the tasklist.')
    return render_template('sheduler.html')


@app.route('/tasklist')
def tasklist():
    tasks = list(Tasks.return_all())
    return render_template('tasklist.html', tasks=tasks)


if __name__ == '__main__':
    app.run(debug=True)
