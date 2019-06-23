from flask import request
from application import app, db
from application.models import Task, Subtask

#Get the tasks as a list
@app.route("/get_tasks/<date>")
def get_tasks(date):
    #Filtering tasks by date
    tasks = Task.query.filter_by(date_posted=date).all()
    return str(tasks)

#Get the subtasks according to the corresponding head task and date
@app.route("/get_subtasks/<task>/<date>")
def get_subtasks(task, date):
    #Filtering subtasks by date and head task
    subtasks = Subtask.query.filter_by(head_task=Task.query.filter_by(title=task, date_posted=date).first()).all()
    return str(subtasks)

#Add a particular task to the database for a particular date
@app.route("/add_task/<title>/<date>", methods=['POST'])
def add_task(title, date):
    #Filtering tasks data to check whether task is already present or not
    task = Task.query.filter_by(title=title, date_posted=date).first()
    #If not already present, add task to the database
    if not task:
        new_task = Task(title=title, date_posted=date)
        db.session.add(new_task)
        db.session.commit()
    tasks = Task.query.all()
    return str(tasks)

#Remove a particular task from the database
@app.route("/remove_task/<title>/<date>", methods=['POST'])
def remove_task(title, date):
    task = Task.query.filter_by(title=title, date_posted=date).first()
    if task:    #If task present in database
        subtasks = Subtask.query.filter_by(head_task=task).all()
        #Filter out the subtasks whose head task is the particular task
        for subtask in subtasks:
            #Loop through the list of subtasks and 
            #delete them from the database
            db.session.delete(subtask)
            db.session.commit()
        #Finally, delete the head task
        db.session.delete(task)
        db.session.commit()
    tasks = Task.query.all()
    return str(tasks)

#Add subtasks corresponding to a date and a head task
@app.route("/add_subtask/<head_task>/<date>", methods=['POST'])
def add_subtask(head_task, date):
    task = Task.query.filter_by(title=head_task, date_posted=date).first()
    if task:
        subtask = Subtask.query.filter_by(title=request.json['title'], content=request.json['content'], head_task=task).first()
        #If the particular subtask not already exists in the database
        if not subtask:
            new_subtask = Subtask(title=request.json['title'], content=request.json['content'], head_task=task)
            db.session.add(new_subtask)
            db.session.commit()
        subtasks = Subtask.query.all()
        return str(subtasks)
    else:
        #If we are trying to add subtask corresponding to a task 
        #which has still not been created 
        return "Create task {} first".format(head_task)

#Remove subtasks corresponding to a head task and date
@app.route("/remove_subtask/<head_task>/<date>", methods=['POST'])
def remove_subtask(head_task, date):
    task = Task.query.filter_by(title=head_task, date_posted=date).first()
    if task:
        subtask = Subtask.query.filter_by(title=request.json['title'], head_task=task).first()
        if subtask: #If subtask exists in database
            db.session.delete(subtask)
            db.session.commit()
        subtasks = Subtask.query.all()
        return str(subtasks)
