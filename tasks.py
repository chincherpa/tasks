#!/usr/bin/env python

from time import sleep

import datetime
import json
import operator
import os
import re

from colorama import init, Fore, Back, Style
init(autoreset=True)
# colorama: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.

dir_path = os.path.dirname(os.path.realpath(__file__))
js_name = "todos.json"
path_to_js = os.path.join(dir_path, js_name)

length_overall = 90


def dump_todo_list_to_json():
    with open(path_to_js, "w") as f:
        json.dump(todos, f, indent=4)


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
        print(Fore.BLUE + f'{id_key}', task["status"], task["text"])
        print(Fore.YELLOW + f'{task["tags"]}')


def filter_tag(id_key, tag):
    for t in todos["tasks"][id_key]["tags"]:
        if t.lower() == tag:
            return True
    return False


def print_comment(id_key):
    for c in todos["tasks"][id_key]["comment"]:
        length_comment = len(c[0])
        length_space = length_overall - (length_comment + 16)
        print(' ' * 3, Fore.BLUE + f'{c[0]}', ' ' * length_space, Fore.BLUE + f'{c[1]}')


def print_tags(id_key):
    id_tags = todos["tasks"][id_key]["tags"]
    print(' ' * 4, end='')
    if "high" in id_tags:
        print(Fore.WHITE + Back.RED + "HIGH", '- ', end='')
    elif "low" in id_tags:
        print(Fore.BLACK + Back.GREEN + "low", '- ', end='')
    for t in id_tags:
        if t in ["high", "low"]:
            continue
        else:
            print(Fore.YELLOW + f'{t}', '- ', end='')
    print('')


def print_result(id_key):
    res = todos["tasks"][id_key]["result"]
    if len(res) > 0:
        length_result = len(res[0])
        length_space = length_overall - (length_result + 3 + 10)
        print(' ' * 3, Fore.BLUE + f'{res[0]}', '.' * length_space, Fore.BLUE + f'{res[1]}')


def list_tasks(status: str, tag_to_show: str = 'all', show_comments: bool = True, show_tags: bool = True, show_date = False, id_to_show = None):
    for id_key, task in todos["tasks"].items():
        title = task["text"].strip()
        date_added = task["date_added"]
        length_text = len(title)
        length_space = length_overall - (length_text + 13)
        space_after_id = 3 - len(id_key)
        has_comments = len(task["comment"][0]) > 0

        if id_to_show and id_key != id_to_show and show_comments: # if show_comments == True and id_to_show -> show only this id
            continue

        if task["status"] == status:

            # show only tasks with date_added greater or lower than SHOW_DATE
            if show_date:
                gt_lt = show_date[0]

                if gt_lt == '<':
                    comp = operator.lt
                else:
                    comp = operator.gt

                date_ = show_date[1:]
                date_filter = datetime.datetime.strptime(date_, '%y-%m-%d')
                task_date = datetime.datetime.strptime(date_added, '%y-%m-%d')
                if not comp(task_date, date_filter):
                    continue

            tag_found = True
            if tag_to_show != "all":
                if len(task["tags"][0]) > 0:
                    tag_found = filter_tag(id_key, tag_to_show.lower())
                else:
                    continue

            if not tag_found:
                continue

            comments_plus = ''
            if not show_comments and has_comments:
                comments_plus = Fore.BLUE + ' +'

            print(Fore.BLUE + f'{id_key}', " " * space_after_id, title, " " * length_space, date_added, comments_plus, sep='')

            if show_comments:
                if has_comments:
                    print_comment(id_key)
            else:
                if id_key == id_to_show and has_comments:
                    print_comment(id_key)

            if show_tags:
                if len(task["tags"][0]) > 0:
                    print_tags(id_key)
            
            if task["status"] == "finished":
                if len(todos["tasks"][id_key]["result"]) > 0:
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
    "Filter tasks by date": "<2019-01-01",
}


def list_actions():
    length = 24
    print('-' * length)
    for action, key in actions.items():
        x = length - len(action) - 6
        if action == "Reset ALL":
            x = 2
            print('|', Fore.YELLOW + f'{action}', ' ' * x, '[', Fore.YELLOW + f'{key.upper()}', ']', ' |', sep='')
        else:
            print('|', Fore.YELLOW + f'{action}', ' ' * x, '[', Fore.YELLOW + f'{key.upper()}', ']', ' |', sep='')
    print('-' * length, '\n')


def list_tags(status: str):
    '''
    Prints all used tags in tasks with status and the number of their occurences

    Parameters:
    status (str): check only for tasks with this status (open/finished)
    '''
    space_max = 15
    num_of_tags = {}
    for id_key, task in todos["tasks"].items():
        if task["status"] == status:
            for t in todos["tasks"][id_key]["tags"]:
                if t:
                    if t in num_of_tags.keys():
                        num_of_tags[t] += 1
                    else:
                        num_of_tags[t] = 1

    tags = list(num_of_tags.keys())
    tags.sort()

    print('')
    print("#" * ((length_overall // 2) - 6), Fore.YELLOW + " USED TAGS ", "#" * ((length_overall // 2) - 10))
    print('')

    for tag in tags:
        space = space_max - len(tag)
        if tag.lower() == "high":
            print(Fore.RED + f'{tag}', " " * space, num_of_tags[tag])
        elif tag.lower() == "low":
            print(Fore.GREEN + f'{tag}', " " * space, num_of_tags[tag])
        elif tag.lower() == "privat":
            print(Fore.MAGENTA + f'{tag}', " " * space, num_of_tags[tag])
        else:
            print(tag, " " * space, num_of_tags[tag])


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

    # ONLY Python Ver. >= 3.8
    # print(f'{action=}, {task_id=}, {text=}, {tags=}')
    # sleep(5)
    return action, task_id, text, tags


def add_key_value_to_my_todolist_json():
    key = input(">>>>  Name of new key:\t") or 0
    if key:
        value = input(">>>>>>  Value:\t") or 0
        if value:
            for k in todos["tasks"].keys():
                print(f"Adding [{key}] to [{k}].")
                todos["tasks"][k][key] = value


def print_params(bToggle_open_tasks, bToggle_finished_tasks, bToggle_comments, comments_id, bToggle_actions, tag, date_):
    color_open_tasks = Fore.GREEN + 'open' if bToggle_open_tasks else Fore.RED + 'open'
    color_finished_tasks = Fore.GREEN + 'finished' if bToggle_finished_tasks else Fore.RED + 'finished'
    if comments_id:
        color_comments = Fore.RED + 'comments' + f' (only {comments_id})'
    else:
        color_comments = Fore.GREEN + 'comments' if bToggle_comments else Fore.RED + 'comments'
    color_actions = Fore.GREEN + 'actions' if bToggle_actions else Fore.RED + 'actions'

    print(color_open_tasks, color_finished_tasks, color_comments, color_actions, 'Tag: ' + Fore.YELLOW + f'{tag}', Fore.YELLOW + f'{date_}' if date_ else '', sep=' | ')


def _main():
    go = True
    bList_finished_tasks = False
    bList_open_tasks = True
    bList_actions = False
    bShow_comments = True
    bShow_tags = True
    bList_tags = False
    date_str = False
    task_id = None
    tag = "all"
    while go:
        today = str(datetime.date.today())
        # clear screen
        os.system('cls')

        # print("#" * length_overall, sep='')
        print("#" * ((length_overall // 2) - 4), Fore.YELLOW + " TASKS ", "#" * ((length_overall // 2) - 5))
        # print("#" * length_overall)

        if bList_tags:
            list_tags('open')
            bList_tags = False
            action_input = input(">>  continue... ")
        else:
            if bList_finished_tasks:
                print("\n##", Fore.BLUE + " FINISHED ", "#" * (length_overall - 12), sep='')
                list_tasks('finished', tag, bShow_comments, bShow_tags, date_str, task_id)

            if bList_open_tasks:
                x = length_overall - 12 - len(tag)
                print("\n##", Fore.GREEN + " OPEN ", "## ", Fore.YELLOW + f'{tag.upper()}', " ", "#" * x, "\n", sep='')
                list_tasks('open', tag, bShow_comments, bShow_tags, date_str, task_id)
                print("\n", "#" * length_overall, sep='')


            print_params(bList_open_tasks, bList_finished_tasks, bShow_comments, task_id, bList_actions, tag, date_str)
            task_id = None                                  # Which ID shows comments - RESET
            # Reset date to show
            date_str = False

            if bList_actions:
                list_actions()

            action_input = input(">>  ") or 0

            if action_input:
                # continue if missing task id ("e4")
                if action_input in ['n', 'f', 'o', 'r', 'e']:
                    continue

                # *TAG_TO_FILTER "*992" - Default "all"
                if action_input[0] == "*":
                    if len(action_input) > 1:
                        tag = action_input[1:]
                        continue
                    else:
                        tag = "all"
                # Filter by date
                elif re.match("^(<|>)(\d){4}-(\d){2}-(\d){2}", action_input):
                    date_str = action_input
                    continue

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
                    elif action_input.lower() == "lt":                          # Show list of used tags
                        bList_tags = not bList_tags
                    else:
                        bList_finished_tasks = not bList_finished_tasks         # Toggle show finished tasks
                        bList_open_tasks = True
                elif action == "a":                                             # List all available actions
                    bList_actions = not bList_actions
                elif action == "c":
                    if task_id:                                                 # Add comment
                        if text:
                            if len(todos["tasks"][task_id]["comment"][0]) == 0:
                                todos["tasks"][task_id]["comment"] = [[text, today]]
                            else:
                                todos["tasks"][task_id]["comment"].append([text, today])
                        else:
                            # this_id = task_id
                            bShow_comments = False
                    else:
                        bShow_comments = not bShow_comments                     # Toggle show comments
                elif action == "n":                                             # New entry
                    task_id = get_id()
                    todos["tasks"][task_id] = {}
                    todos["tasks"][task_id]["text"] = text
                    todos["tasks"][task_id]["status"] = "open"
                    todos["tasks"][task_id]["comment"] = [""]
                    todos["tasks"][task_id]["tags"] = tags
                    todos["tasks"][task_id]["date_added"] = today
                    todos["tasks"][task_id]["result"] = ""
                elif action == "f":                                             # Set status to FINISH
                    todos["tasks"][task_id]["status"] = "finished"
                    todos["tasks"][task_id]["result"] = [text, today]
                elif action == "o":                                             # Set status to OPEN
                    todos["tasks"][task_id]["status"] = "open"
                elif action == "r":                                             # Remove existing task
                    todos["tasks"].pop(task_id, None)
                elif action == "e":                                             # Edit existing task
                    todos["tasks"][task_id]["text"] = text
                elif action == "t":                                             # add tags
                    if task_id:                                                 # Add comment
                        if len(todos["tasks"][task_id]["tags"][0]) == 0:
                            todos["tasks"][task_id]["tags"] = tags
                        else:
                            for new_tag in tags:
                                todos["tasks"][task_id]["tags"].append(new_tag)
                    else:
                        bShow_tags = not bShow_tags
                elif action == "addkey":                                             # Edit existing task
                    add_key_value_to_my_todolist_json()
                dump_todo_list_to_json()


if __name__ == "__main__":
    _main()