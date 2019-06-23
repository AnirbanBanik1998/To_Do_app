from flask import request
from application import app, db
from application.models import Task, Subtask

@app.route("/get_tasks/<date>")
def get_tasks(date):
    tasks = Task.query.filter_by(date_posted=date).all()
    return str(tasks)

@app.route("/get_subtasks/<task>/<date>")
def get_subtasks(task, date):
    subtasks = Subtask.query.filter_by(head_task=Task.query.filter_by(title=task, date_posted=date).first()).all()
    return str(subtasks)

@app.route("/add_task/<title>/<date>", methods=['POST'])
def add_task(title, date):
    task = Task.query.filter_by(title=title, date_posted=date).first()
    if not task:
        new_task = Task(title=title, date_posted=date)
        db.session.add(new_task)
        db.session.commit()
    tasks = Task.query.all()
    return str(tasks)

@app.route("/remove_task/<title>/<date>", methods=['POST'])
def remove_task(title, date):
    task = Task.query.filter_by(title=title, date_posted=date).first()
    if task:
        subtasks = Subtask.query.filter_by(head_task=task).all()
        for subtask in subtasks:
            db.session.delete(subtask)
            db.session.commit()
        db.session.delete(task)
        db.session.commit()
    tasks = Task.query.all()
    return str(tasks)

@app.route("/add_subtask/<head_task>/<date>", methods=['POST'])
def add_subtask(head_task, date):
    task = Task.query.filter_by(title=head_task, date_posted=date).first()
    if task:
        subtask = Subtask.query.filter_by(title=request.json['title'], content=request.json['content'], head_task=task).first()
        if not subtask:
            new_subtask = Subtask(title=request.json['title'], content=request.json['content'], head_task=task)
            db.session.add(new_subtask)
            db.session.commit()
        subtasks = Subtask.query.all()
        return str(subtasks)
    else:
        return "Create task {} first".format(head_task)

@app.route("/remove_subtask/<head_task>/<date>", methods=['POST'])
def remove_subtask(head_task, date):
    task = Task.query.filter_by(title=head_task, date_posted=date).first()
    if task:
        subtask = Subtask.query.filter_by(title=request.json['title'], head_task=task).first()
        if subtask:
            db.session.delete(subtask)
            db.session.commit()
        subtasks = Subtask.query.all()
        return str(subtasks)
