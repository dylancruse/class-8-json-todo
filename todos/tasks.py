from datetime import datetime

from .exceptions import (
    InvalidTaskStatus, TaskAlreadyDoneException, TaskDoesntExistException)
from .utils import parse_date, parse_int


def new():
    return []


def create_task(tasks, name, description=None, due_on=None):
    if due_on and type(due_on) != datetime:
        due_on = parse_date(due_on)

    task = {
        'task': name,
        'description': description,
        'due_on': due_on,
        'status': 'pending'
    }
    tasks.append(task)


def list_tasks(tasks, status='all'):
    if not status in ('all', 'done', 'pending'):
        raise InvalidTaskStatus
    
    task_list = []
    for idx, task in enumerate(tasks, 1):
        if task['due_on'] is not None:
            due_on = task['due_on'].strftime('%Y-%m-%d %H:%M:%S')
        else:
            due_on = None

        t = (idx, task['task'], due_on, task['status'])
        if status == 'all' or task['status'] == status:
            task_list.append(t)

    return task_list



#should raise an exception if the task is already done
#or if the task doesn't exist
def complete_task(tasks, name):
    new_tasks = []
    idx = parse_int(name)
    
    found = False
    for index, task in enumerate(tasks, 1):
        if name == task['task'] or index == idx:
            #we found the task
            if task['status'] == 'done':
                raise TaskAlreadyDoneException
            task = task.copy()
            task['status'] = 'done'
            found = True
        new_tasks.append(task)
    
    if not found:
        raise TaskDoesntExistException
    

    return new_tasks

