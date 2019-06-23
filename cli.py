import argparse
import requests, json
from datetime import datetime, date

def getdata(func, title=None, date=None):
    if title:
        URL="http://127.0.0.1:5000/{}/{}/{}".format(func, title, date)
    else:
        URL="http://127.0.0.1:5000/{}/{}".format(func, date)
    print("URL:"+URL)
    session = requests.Session()
    session.trust_env = False
    response = session.get(URL)
    print(str(response.status_code))
    if (response.status_code == requests.codes.ok):
        return(response.text)
    else:
        return(None)

def postdata(func, title, date, payload=None):
    URL="http://127.0.0.1:5000/{}/{}/{}".format(func, title, date)
    print("URL:"+URL)
    session = requests.Session()
    session.trust_env = False
    response = session.post(URL, json=payload)
    print(str(response.status_code))
    if (response.status_code == requests.codes.ok):
        print(response.text)

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
                pass
            postdata('add_subtask', args.task, date_str, payload)
        else:
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
            postdata('remove_subtask', args.task, date_str, payload)
        else:
            postdata('remove_task', args.task, date_str)
    else:
        print(getdata('get_subtasks', args.task, date_str))

else:
    print(getdata('get_tasks', date=date_str))