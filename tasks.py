#!/usr/bin/env python

import hashlib
import json
import os
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
js_name = 'my_todolist.js'
path_to_js = os.path.join(dir_path, js_name)

def dump_todo_list_to_json():
    print('dumping todo-list to JSON file')
    with open(path_to_js, 'w') as f:
        json.dump(todos, f, indent=4)


if not os.path.isfile(path_to_js):
    print('not os.path.isfile(path_to_js)')
    open(js_name, 'a').close()
    todos = {}
    todos['id'] = 0
    todos['tasks'] = {}
    dump_todo_list_to_json()
else:
    with open(path_to_js, 'r') as f:
        todos = json.load(f)


def get_id():
    new_id = todos['id'] + 1
    todos['id'] = new_id
    return str(new_id)


def list_all_tasks():
    print('id:', todos['id'])
    for id_key, task in todos['tasks'].items():
        print('-'*40)
        print(id_key, task['status'], task['text'])


def list_open_tasks():
    # print('id:', todos['id'])
    for id_key, task in todos['tasks'].items():
        if task['status'] == 'open':
            print('-'*40)
            print(id_key, task['status'], task['text'])


def list_finished_tasks():
    # print('id:', todos['id'])
    for id_key, task in todos['tasks'].items():
        if task['status'] == 'finished':
            print('-'*40)
            print(id_key, task['status'], task['text'])


actions = {
    'Add task' : 'n',
    'Edit task' : 'e',
    'Remove task' : 'r',
    'Finish task' : 'f',
    'List task' : 't',
    'Cancel' : 'c'
    }
def list_actions():
    for action, key in actions.items():
        print(action, key)
    print('')


def _main():
    go = True
    while go:
        list_open_tasks()
        print('#'*80)

        # list_actions()

        action_input = input('Task:\t') or 0

        if action_input:
            # print('input was:', action_input)
            action = action_input[:1].lower()
            # print('action', action)
            # print('actions.values()')

            if action in actions.values():
                if action == 'n':   # New entry
                    print('Adding new task to ToDo-List')
                    task_id = get_id()
                    text = action_input[2:]
                    todos['tasks'][task_id] = {'text' : text, 'status' : 'open'}
                elif action == 'c': # Cancel program
                    go = False
                elif action == 't': # List all tasks
                    print('list tasks')
                else:
                    task_id = re.search('\d+', action_input).group()
                    if action == 'f':   # Set status to FINISH
                        # task_id = action_input[2:]
                        print('finishing task')
                        todos['tasks'][task_id]['status'] = 'finished'
                    elif action == 'r': # Remove existing task
                        print('Removing task', todos[task_id]['text'])
                        todos.pop(task_id, None)
                    else:
                    # try:
                        _, task_id, text = re.split(" ", action_input, 2)
                    # except:

                        if action == 'e':   # Edit existing task
                            print('editing', todos['tasks'][task_id]['text'])
                            todos['tasks'][task_id]['text'] = text
            else:
                print('wrong input')

            dump_todo_list_to_json()

            # sys.stderr.write('The ID "%s" matches more than one task.\n' % e.prefix)
            # sys.stderr.write('The ID "%s" does not match any task.\n' % e.prefix)

if __name__ == '__main__':
    _main()
    print('Good Bye\n')
