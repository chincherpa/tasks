#!/usr/bin/env python

import datetime
import json
import os
import re

import crayons

dir_path = os.path.dirname(os.path.realpath(__file__))
js_name = "my_todolist.json"
path_to_js = os.path.join(dir_path, js_name)

length_overall = 90

# crayons: 'red', 'green', 'yellow', 'blue'
# crayons: 'black', 'magenta', 'cyan', 'white'


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
    new_id = todos["ids"] + 1
    todos["ids"] = new_id
    return str(new_id)


def list_all_tasks():
    print("ids:", todos["ids"])
    for id_key, task in todos["tasks"].items():
        print("-" * 40)
        print(crayons.blue(id_key), task["status"], task["text"])
        print(crayons.yellow(task["tags"]))


def filter_tag(id_key, tag):
    for t in todos["tasks"][id_key]["tags"]:
        if t.lower() == tag:
            return True
    return False


def print_comment(id_key):
    for c in todos["tasks"][id_key]["comment"]:
        length_comment = len(c[0])
        length_space = length_overall - (length_comment + 16)
        print(' ' * 3, crayons.blue(c[0]), ' ' * length_space, crayons.blue(c[1]))


def print_tags(id_key):
    id_tags = todos["tasks"][id_key]["tags"]
    print(' ' * 4, end='')
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


def print_result(id_key):
    res = todos["tasks"][id_key]["result"]
    length_result = len(res[0])
    length_space = length_overall - (length_result + 3 + 10)
    print(' ' * 3, crayons.blue(res[0]), '.' * length_space, crayons.blue(res[1]))


def list_tasks(status: str, tag_to_show: str = 'all', show_comments: bool = True):
    for id_key, task in todos["tasks"].items():
        title = task["text"].strip()
        date_added = task["date_added"]
        length_text = len(title)
        length_space = length_overall - (length_text + 13)
        space_after_id = 3 - len(id_key)

        if task["status"] == status:

            tag_found = True
            if tag_to_show != "all":
                if len(task["tags"][0]) > 0:
                    tag_found = filter_tag(id_key, tag_to_show.lower())
                else:
                    continue

            if not tag_found:
                continue

            if 'privat' in task["tags"]:
                print(crayons.blue(id_key), " " * space_after_id, "## ", crayons.magenta(title), " ##", " " * (length_space - 6), date_added, sep='')
            else:
                print(crayons.blue(id_key), " " * space_after_id, title, " " * length_space, date_added, sep='')

            if show_comments:
                if len(task["comment"][0]) > 0:
                    print_comment(id_key)

            if len(task["tags"][0]) > 0:
                print_tags(id_key)
            
            if task["status"] == "finished":
                if len(todos["tasks"][id_key]["result"]) != 0:
                    print_result(id_key)


actions = {
    "Add task 'n Description'": "n",
    "Edit task": "e",
    "Add comment": "c",
    "Add tag": "t",
    "Remove task": "r",
    "Finish task": "f",
    "Reopen task": "o",
    "List all task": "l",
    "List finished tasks": "lf",
    "List actions": "a",
    "Cancel": "y",
    "Reset ALL": "resetall",
    "Add key/value to my_todolist.json": "addkey",
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
    elif inp == "addkey":
        action = "addkey"
    else:
        action = inp[:1].lower()
        if action not in actions.values():
            action = None

    # TAGS
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
        text = inp.partition(task_id)[2].strip()
    except TypeError:
        try:
            text = inp.partition('n')[2].strip()
        except TypeError:
            text = None

    return action, task_id, text, tags


def add_key_value_to_my_todolist_json():
    key = input(">>>>  Name of new key:\t") or 0
    if key:
        value = input(">>>>>>  Value:\t") or 0
        if value:
            for k in todos["tasks"].keys():
                print(f"Adding [{key}] to [{k}].")
                todos["tasks"][k][key] = value


def print_params(bList_open_tasks, bList_finished_tasks, bList_actions, tag):
    color_open_tasks = crayons.green('open') if bList_open_tasks else crayons.red('open')
    color_finished_tasks = crayons.green('finished') if bList_finished_tasks else crayons.red('finished')
    color_actions = crayons.green('actions') if bList_actions else crayons.red('actions')

    print(color_open_tasks, '|', color_finished_tasks, '|', color_actions, '|', 'Tag:', crayons.yellow(tag))


def _main():
    go = True
    bList_finished_tasks = False
    bList_open_tasks = True
    bList_actions = False
    bShow_comments = True
    tag = "all"
    while go:
        today = str(datetime.date.today())
        # clear screen
        os.system('cls')

        print("#" * length_overall, sep='')
        print("#" * ((length_overall // 2) - 4), crayons.yellow(" TASKS "), "#" * ((length_overall // 2) - 5))
        print("#" * length_overall)

        if bList_finished_tasks:
            print("\n##", crayons.blue(" FINISHED "), "#" * (length_overall - 12), sep='')
            list_tasks('finished', tag, bShow_comments)

        if bList_open_tasks:
            x = length_overall - 12 - len(tag)
            print("\n##", crayons.green(" OPEN "), "## ", crayons.yellow(tag.upper()), " ", "#" * x, "\n", sep='')
            list_tasks('open', tag, bShow_comments)
            print("\n", "#" * length_overall, sep='')

        print_params(bList_open_tasks, bList_finished_tasks, bList_actions, tag)

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
                else:
                    tag = "all"

            action, task_id, text, tags = extract_data(action_input)

            if action == "resetall":
                sure = input(">>  SURE? Delete ALL?\t('yes'/'y'):  ")
                if sure.lower() in ['yes', 'y']:
                    todos["ids"] = 0
                    todos["tasks"] = {}
                    dump_todo_list_to_json()
                continue

            if action == "y":                                               # Cancel program
                go = False
            elif action == "l":
                if action_input.lower() == "lf":
                    bList_finished_tasks = True                             # Show ONLY finished tasks
                    bList_open_tasks = False
                else:
                    bList_finished_tasks = not bList_finished_tasks         # Toggle show finished tasks
                    bList_open_tasks = True
            elif action == "a":                                             # List all available actions
                bList_actions = not bList_actions
            elif action == "c":
                if task_id:                                                 # Add comment
                    if len(todos["tasks"][task_id]["comment"][0]) == 0:
                        todos["tasks"][task_id]["comment"] = [[text, today]]
                    else:
                        todos["tasks"][task_id]["comment"].append([text, today])
                else:
                    bShow_comments = not bShow_comments                     # Toggle show comments
            elif action == "n":                                             # New entry
                task_id = get_id()
                todos["tasks"][task_id] = {"text": text, "status": "open", "comment": [""], "tags": tags, "date_added": today}
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
            elif action == "addkey":                                             # Edit existing task
                add_key_value_to_my_todolist_json()
            dump_todo_list_to_json()


if __name__ == "__main__":
    _main()
