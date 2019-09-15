#!/usr/bin/env python

import hashlib
import json
import os

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
    dump_todo_list_to_json()
else:
    with open(path_to_js, 'r') as f:
        todos = json.load(f)


def _hash(text):
    """Return a hash of the given text for use as an id.

    Currently SHA1 hashing is used.  It should be plenty for our purposes.
    """
    return hashlib.sha1(text.encode('utf-8')).hexdigest()


def list_tasks():
    for k1, v1 in todos.items():
        print(k1)
        for k2, v2 in v1.items():
            print(k2, v2)


def list_actions():
    global actions
    actions = {
    'Add task' : 'n',
    'Edit task' : 'e',
    'Remove task' : 'r',
    'Finish task' : 'f',
    'List task' : 't',
    'Cancel' : 'c'
    }
    for action, key in actions.items():
        print(action, key)
    print('')


def _main():
    go = True
    while go:
        print('-'*30)
        list_tasks()
        print('-'*30)

        list_actions()

        new_task = input('Task:\t') or 0

        # there is input
        if new_task:
            print('input was:', new_task)
            # first letter is what to do
            task = new_task[:1].lower()
            print('first letter:', task)
            if len(new_task) > 2:
                text = new_task[2:]
                print('text', text)

            if task in actions.values():
                if task == 'n':
                    print('Adding new task to ToDo-List')
                    task_id = _hash(text)
                    todos[task_id] = {'text' : text, 'status' : 'open'}
                elif task == 'e':
                    print('edit')
                    todos[task_id]['text'] = text
                elif task == 'r':
                    print('Removing task', todos[task_id]['text'])
                    todos.pop(task_id, None)
                elif task == 'f':
                    print('finish')
                    todos[task_id]['status'] = 'finished'
                elif task == 'c':
                    dump_todo_list_to_json()
                    go = False
                else:
                    print('wrong input')

            # sys.stderr.write('The ID "%s" matches more than one task.\n' % e.prefix)
            # sys.stderr.write('The ID "%s" does not match any task.\n' % e.prefix)

if __name__ == '__main__':
    _main()
    print('Good Bye')
