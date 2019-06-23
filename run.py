from application import app, db
from application.models import Task, Subtask

#Creating the database tables
db.create_all()

#Running the application in debug mode
app.run(debug=True)