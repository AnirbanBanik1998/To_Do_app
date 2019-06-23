from application import app, db
from application.models import Task, Subtask

db.create_all()

app.run(debug=True)