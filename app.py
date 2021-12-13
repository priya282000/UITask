import os
from datetime import date
from flask import Flask, render_template, url_for, request, redirect
import smtplib
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

""" MySQL connectivity """
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class task_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    assignee = db.Column(db.String(50), nullable=False)
    assignee_email = db.Column(db.String(50), nullable=False)
    reporter = db.Column(db.String(50), nullable=False)
    due = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), default='Pending')


@app.route("/")
def home():
    """ Display task details """
    tasks = task_details.query.order_by(task_details.id)
    for task in tasks:
        due_date = task.due
        today = date.today()
        days_left = (due_date - today).days
        if days_left == 1 and task.status == 'Pending':
            message = 'You have one day left to complete the task, '+task.task+'. Thank You, XXX.'
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(os.environ.get('mail_id'), os.environ.get('mail_pass'))
            server.sendmail(os.environ.get('mail_id'), task.assignee_email, message)
    return render_template("home.html", datas=tasks)


@app.route("/todo", methods=["GET","POST"])
def add_todo():
    """ Add todo in the table """
    if request.method == "POST":
        task = request.form['task']
        assignee = request.form['assignee']
        assignee_email = request.form['assignee_email']
        reporter = request.form['reporter']
        due = request.form['due']
        new_task = task_details(task=task, assignee=assignee, assignee_email=assignee_email, reporter=reporter, due=due)
        try:
            db.session.add(new_task)
            db.session.commit()
        except:
            return "Error adding task"

        """ Send mail to the assignee if task assigned """
        message = 'You have been assigned with a new task, '+ task+ ' by '+ reporter+'. Thank You, xxx'
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(os.environ.get('mail_id'), os.environ.get('mail_pass'))
        server.sendmail(os.environ.get('mail_id'), assignee_email, message)
    return redirect(url_for('home'))


@app.route("/changeStatus/<int:id>", methods=["GET","POST"])
def change_status(id):
    """ Change status if done """
    update_task = task_details.query.get_or_404(id)
    update_task.status = 'Done'
    try:
        db.session.commit()
        return redirect(url_for('home'))
    except:
        return "Not updated"
    return redirect(url_for('home'))


@app.route("/deleteTask/<int:id>", methods=["GET", "POST"])
def delete_task(id):
    """ Delete task if needed """
    delete_task = task_details.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect(url_for('home'))
    except:
        return "Not deleted"
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)

