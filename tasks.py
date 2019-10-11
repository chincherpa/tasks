#!/usr/bin/env python

import json
import os
import re
from time import sleep

import crayons

dir_path = os.path.dirname(os.path.realpath(__file__))
js_name = "my_todolist.js"
path_to_js = os.path.join(dir_path, js_name)


def dump_todo_list_to_json():
    with open(path_to_js, "w") as f:
        json.dump(todos, f, indent=4)
    print(crayons.yellow("\n[INFO] saved", bold=True))


if not os.path.isfile(path_to_js):
    print("not os.path.isfile(path_to_js)")
    open(js_name, "a").close()
    todos = {}
    todos["ids"] = 0
    todos["tasks"] = {}
    dump_todo_list_to_json()
else:
    with open(path_to_js, "r") as f:
        todos = json.load(f)


def get_id():
    new_id = todos["id"] + 1
    todos["id"] = new_id
    return str(new_id)


def list_all_tasks():
    print("id:", todos["id"])
    for id_key, task in todos["tasks"].items():
        print("-" * 40)
        print(crayons.blue(id_key), task["status"], task["text"])
        print(crayons.yellow(task["tags"]))


def filter_tag(id_key, tag):
    for t in todos["tasks"][id_key]["tags"]:
        if t.lower() == tag:
            return True
    return False


def print_comment(id_key, x):
    for c in todos["tasks"][id_key]["comment"]:
        print(' ' * (x + 1), crayons.blue(c))


def print_tags(id_key, x):
    id_tags = todos["tasks"][id_key]["tags"]
    print(' ' * (x + 2), end='')
    if "high" in id_tags:
        print(crayons.red("HIGH"), '- ', end='')
    elif "low" in id_tags:
        print(crayons.green("low"), '- ', end='')
    for t in id_tags:
        if t in ["high", "low"]:
            continue
        else:
            print(crayons.yellow(t), '- ', end='')
    print('')


def print_result(id_key, x):
    print(' ' * (x + 2), end='')
    print(crayons.cyan('-> ' + todos["tasks"][id_key]["result"]))


def list_open_tasks(tag_to_show):
    for id_key, task in todos["tasks"].items():
        if task["status"] == "open":
            tag_found = True
            if tag_to_show != "all":
                if len(task["tags"][0]) > 0:
                    tag_found = filter_tag(id_key, tag_to_show.lower())

            if not tag_found:
                continue

            print(crayons.blue(id_key), task["text"])
            x = len(id_key)

            if len(task["comment"][0]) > 0:
                print_comment(id_key, x)

            if len(task["tags"][0]) > 0:
                print_tags(id_key, x)


def list_finished_tasks():
    for id_key, task in todos["tasks"].items():
        if task["status"] == "finished":
            print(crayons.blue(id_key), task["text"])
            x = len(id_key)

            if len(task["comment"][0]) > 0:
                print_comment(id_key, x)

            if len(task["tags"][0]) > 0:
                print_tags(id_key, x)

            if len(task["result"]) > 0:
                print_result(id_key, x)


actions = {
    "Add task": "n",
    "Edit task": "e",
    "Add comment": "c",
    "Add tag": "t",
    "Remove task": "r",
    "Finish task": "f",
    "Reopen task": "o",
    "List task": "l",
    "List actions": "a",
    "Cancel": "y",
    "Reset ALL": "resetall",
}


def list_actions():
    length = 24
    print('-' * length)
    for action, key in actions.items():
        x = length - len(action) - 6
        if action == "Reset ALL":
            x = 2
            print('|', crayons.yellow(action), ' ' * x, '[', crayons.yellow(key.upper()), ']', ' |', sep='')
        else:
            print('|', crayons.yellow(action), ' ' * x, '[', crayons.yellow(key.upper()), ']', ' |', sep='')
    print('-' * length, '\n')


def extract_data(inp: str):
    # ACTION
    if inp == "resetall":
        action = "resetall"
    else:
        action = inp[:1].lower()
        if action not in actions.values():
            action = None

    # TAGS
    # tags = inp.split("*")[1:]
    tags = [x.strip(' ') for x in inp.split("*")[1:]]
    if not tags:
        tags = [""]

    # input Tags abschneiden
    inp = inp.split("*")[0]
    # TASK ID
    try:
        task_id = re.search(r"\d+", inp).group()
        if task_id not in todos["tasks"].keys():
            task_id = None
    except AttributeError:
        task_id = None

    # TEXT
    try:
        text = inp.partition(task_id)[2].lstrip()
    except TypeError:
        try:
            text = inp.partition('n')[2].lstrip()
        except TypeError:
            text = None

    return action, task_id, text, tags


def _main():
    go = True
    bList_tasks = False
    bList_actions = False
    tag = "all"
    while go:
        # clear screen
        os.system('cls')

        print("#" * 82, sep='')
        print("#" * 37, crayons.yellow(" TASKS "), "#" * 36)
        print("#" * 82)

        if bList_tasks:
            print("\n##", crayons.blue(" FINISHED "), "#" * 70, sep='')
            list_finished_tasks()

        x = 70 - len(tag)
        print("\n##", crayons.green(" OPEN "), "## ", crayons.yellow(tag.upper()), " ", "#" * x, "\n", sep='')
        list_open_tasks(tag)
        print("\n", "#" * 82, sep='')

        tag = "all"

        if bList_actions:
            list_actions()

        action_input = input(">>  ") or 0

        if action_input:
            # continue if missing parameter ("e4")
            if len(action_input) == 1 and action_input in ['n', 'f', 'o', 'r', 'e', 't']:
                continue

            # *TAG_TO_FILTER "*992" - Default "all"
            if action_input[0] == "*":
                if len(action_input) > 1:
                    tag = action_input[1:]

            action, task_id, text, tags = extract_data(action_input)

            if action == "resetall":
                sure = input(">>  SURE? Delete ALL?\t('yes'/'y'):  ") or 0
                if sure.lower() in ['yes', 'y']:
                    todos["ids"] = 0
                    todos["tasks"] = {}
                    dump_todo_list_to_json()
                continue

            if action == "y":                                               # Cancel program
                go = False
            elif action == "l":                                             # List all tasks
                bList_tasks = not bList_tasks
            elif action == "a":                                             # List all available actions
                bList_actions = not bList_actions
            elif action == "c":                                             # Add comment
                if len(todos["tasks"][task_id]["comment"][0]) == 0:
                    todos["tasks"][task_id]["comment"] = [text]
                else:
                    todos["tasks"][task_id]["comment"].append(text)
            elif action == "n":                                             # New entry
                task_id = get_id()
                todos["tasks"][task_id] = {"text": text, "status": "open", "comment": [""], "tags": tags}
            elif action == "f":                                             # Set status to FINISH
                todos["tasks"][task_id]["status"] = "finished"
                if text:                                                    # and set Result
                    todos["tasks"][task_id]["result"] = text
            elif action == "o":                                             # Set status to OPEN
                todos["tasks"][task_id]["status"] = "open"
            elif action == "r":                                             # Remove existing task
                todos["tasks"].pop(task_id, None)
            elif action == "e":                                             # Edit existing task
                todos["tasks"][task_id]["text"] = text
            elif action == "t":                                             # add tags
                if len(todos["tasks"][task_id]["tags"][0]) == 0:
                    todos["tasks"][task_id]["tags"] = tags
                else:
                    for tag in tags:
                        todos["tasks"][task_id]["tags"].append(tag)
                tag = 'all'                                                 # reset variable tag, coz filter
            dump_todo_list_to_json()


if __name__ == "__main__":
    _main()
