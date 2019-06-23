# To_Do_app

A Command Line Interface to maintain daily to do tasks.

## Usage

* To start the flask server, execute -> python3 run.py.
* To use the Command Line Interface(CLI), execute -> python3 cli.py [arguments]
Arguments:
	-d --date -> Store date in form of day-month-year.
	-a --add -> Add to the database.
	-r --remove -> Remove from the database.
	-t --task -> Specify the task title.
	-s --subtask -> Specify the subtask title.


## Documentation

* **run.py** -> To start the flask server in debug mode.

* **cli.py** -> To use the CLI to fetch, push updates to/from the database.
Functions:
	1. getdata(func, title=None, date=None) -> Fetch updates through GET requests.
		Arguments:
			func -> Function name to specify route endpoint.
			title -> Task title. Initialized to None to specify GET tasks.
			date -> To do date.

	2. postdata(func, title, date, payload=None) -> Push updates using POST requests.
		Arguments:
			func -> Function name to specify route endpoint.
			title -> Task title.
			date -> To do date.
			payload -> Addition information to be passed. This is required to add/remove subtasks.
						Set to None to specify addition or removal of tasks.

* **application/** -> Package.
Contents:
	* **__init__.py** -> Initialization script.

	* **models.py** -> Specify the database models, in the form of Task or Subtask.
		Classes:
		1. Task -> Contents - title, date_posted.
		2. Subtask -> Contents - title.

	* **routes.py** -> Specify the routing endpoints, to get data from or post data to.
	Functions:
		1. get_tasks(date) -> Fetch tasks from database specific to a particular date.
		2. get_subtasks(title, date) -> Fetch subtasks specific to a particular task and date.
		3. add_task(title, date) -> Add a task to the database, with a title, and to do date.
		4. remove_task(title, date) -> Remove a particular task from the database.
		5. add_subtask(head_task, date) -> Add a subtask corresponding to a particular head_task and to do date.
		6. remove_subtask(head_task, date) -> Remove a subtask from the database.
