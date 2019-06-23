from datetime import date
from application import db

#For the tasks data
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.String(100), nullable=False, 
        default=str(date.today()))
    #Here we are referencing to Subtask class, so uppercase.
    subtask = db.relationship('Subtask', backref='head_task', lazy=True)

    def __repr__(self):
        return "Task - title -> {}, to_do_date -> {}".format(self.title, self.date_posted)

#For the subtask data corresponding to a given task
class Subtask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    #Here we are referencing to table task, column id, so using lower case 
    head_task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    def __repr__(self):
        return "Subtask - title -> {} content -> {}".format(self.title, self.content)