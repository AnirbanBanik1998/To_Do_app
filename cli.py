import argparse
import requests, json
from datetime import datetime, date

app_url = "http://127.0.0.1:5000"

#Get status data from URL
def getdata(func, title=None, date=None):
    if title:
        URL="{}/{}/{}/{}".format(app_url, func, title, date)
    else:
        URL="{}/{}/{}".format(app_url, func, date)
    print("URL:"+URL)
    session = requests.Session()
    session.trust_env = False
    response = session.get(URL)
    print(str(response.status_code))
    if (response.status_code == requests.codes.ok):
        return(response.text)
    else:
        return(None)

#Post data to URL
def postdata(func, title, date, payload=None):
    URL="{}/{}/{}/{}".format(app_url, func, title, date)
    print("URL:"+URL)
    session = requests.Session()
    session.trust_env = False
    response = session.post(URL, json=payload)
    print(str(response.status_code))
    if (response.status_code == requests.codes.ok):
        print(response.text)

#Creating the CLI arguments
my_parser = argparse.ArgumentParser(description="To Do Application")

my_parser.add_argument('-d', '--date', action='store', type=str, 
                help='Date in format of day-month-year')
my_parser.add_argument('-a', '--add', action='store_true', 
                help='Addition')
my_parser.add_argument('-r', '--remove', action='store_true', 
                help='Deletion')
my_parser.add_argument('-t', '--task', action='store', type=str, 
                help='Tasks')
my_parser.add_argument('-s', '--subtask', action='store', type=str, 
                help='Subtasks')

args = my_parser.parse_args()

#If date is not initialized, it is taken as today's date
if not args.date:
    date = date.today()
else:
    date = datetime.strptime(args.date, "%d-%m-%Y").date()
date_str = str(date)

print(date)

payload = {}
if args.task:
    if args.add:
        if args.subtask:
            array = args.subtask.split("->")
            try:
                payload['title'] = array[0]
                payload['content'] = array[1]
                print("Payload: "+str(payload))
            except:
                #Mainly if user has not specified the contents of the subtask
                pass
            #Add subtask to database, if both subtask and task 
            #arguments are given 
            postdata('add_subtask', args.task, date_str, payload)
        else:
            #If subtask argument is not given, add task to database
            postdata('add_task', args.task, date_str)
    elif args.remove:
        if args.subtask:
            array = args.subtask.split("-")
            try:
                payload['title'] = array[0]
                payload['content'] = array[1]
                print("Payload: "+str(payload))
            except:
                pass
            #Remove subtask from database
            postdata('remove_subtask', args.task, date_str, payload)
        else:
            #Remove task from database
            postdata('remove_task', args.task, date_str)
    else:
        #If neither add or remove arguments are specified, get subtask status
        print(getdata('get_subtasks', args.task, date_str))

else:
    #If no arguments are specified, get task status
    print(getdata('get_tasks', date=date_str))