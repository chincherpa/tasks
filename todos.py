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
    todos["todos"] = {}
    dump_todo_list_to_json()
else:
    with open(path_to_js, "r") as f:
        todos = json.load(f)


def get_id():
    new_id = todos["ids"] + 1
    todos["ids"] = new_id
    return str(new_id)


def list_all_todos():
    print("ids:", todos["ids"])
    for id_key, todo in todos["todos"].items():
        print("-" * 40)
        print(Fore.BLUE + f'{id_key}', todo["status"], todo["text"])
        print(Fore.YELLOW + f'{todo["tags"]}')


def filter_tag(id_key, tag):
    for t in todos["todos"][id_key]["tags"]:
        if t.lower() == tag:
            return True
    return False


def print_comment(id_key):
    for c in todos["todos"][id_key]["comment"]:
        length_comment = len(c[0])
        length_space = length_overall - (length_comment + 16)
        print(' ' * 3, Fore.BLUE + f'{c[0]}', ' ' * length_space, Fore.BLUE + f'{c[1]}')


def print_tags(id_key):
    id_tags = todos["todos"][id_key]["tags"]
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
    res = todos["todos"][id_key]["result"]
    if len(res) > 0:
        length_result = len(res[0])
        length_space = length_overall - (length_result + 3 + 10)
        print(' ' * 3, Fore.BLUE + f'{res[0]}', '.' * length_space, Fore.BLUE + f'{res[1]}')


def list_todos(status: str, tag_to_show: str = 'all', show_comments: bool = True, show_tags: bool = True, show_date = False, id_to_show = None):
    for id_key, todo in todos["todos"].items():
        title = todo["text"].strip()
        date_added = todo["date_added"]
        length_text = len(title)
        length_space = length_overall - (length_text + 13)
        space_after_id = 3 - len(id_key)
        has_comments = len(todo["comment"][0]) > 0

        if id_to_show and id_key != id_to_show and show_comments: # if show_comments == True and id_to_show -> show only this id
            continue

        if todo["status"] == status:

            # show only todos with date_added greater or lower than SHOW_DATE
            if show_date:
                gt_lt = show_date[0]

                if gt_lt == '<':
                    comp = operator.lt
                else:
                    comp = operator.gt

                date_ = show_date[1:]
                date_filter = datetime.datetime.strptime(date_, '%y-%m-%d')
                todo_date = datetime.datetime.strptime(date_added, '%y-%m-%d')
                if not comp(todo_date, date_filter):
                    continue

            tag_found = True
            if tag_to_show != "all":
                if len(todo["tags"][0]) > 0:
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
                if len(todo["tags"][0]) > 0:
                    print_tags(id_key)
            
            if todo["status"] == "finished":
                if len(todos["todos"][id_key]["result"]) > 0:
                    print_result(id_key)


actions = {
    "Add todo 'n Description'": "n",
    "Edit todo": "e",
    "Add comment": "c",
    "Add tag": "t",
    "Remove todo": "r",
    "Finish todo": "f",
    "Reopen todo": "o",
    "List all todo": "l",
    "List finished todos": "lf",
    "List actions": "a",
    "Cancel": "y",
    "Reset ALL": "resetall",
    "Add key/value to todos.json": "addkey",
    "Filter todos by date": "<2019-01-01",
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
    Prints all used tags in todos with status and the number of their occurences

    Parameters:
    status (str): check only for todos with this status (open/finished)
    '''
    space_max = 15
    num_of_tags = {}
    for id_key, todo in todos["todos"].items():
        if todo["status"] == status:
            for t in todos["todos"][id_key]["tags"]:
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
    # todo ID
    try:
        todo_id = re.search(r"\d+", inp).group()
        if todo_id not in todos["todos"].keys():
            todo_id = None
    except AttributeError:
        todo_id = None

    # TEXT
    try:
        text = inp.partition(todo_id)[2].strip()
    except TypeError:
        try:
            text = inp.partition('n')[2].strip()
        except TypeError:
            text = None

    # ONLY Python Ver. >= 3.8
    # print(f'{action=}, {todo_id=}, {text=}, {tags=}')
    # sleep(5)
    return action, todo_id, text, tags


def add_key_value_to_my_todolist_json():
    key = input(">>>>  Name of new key:\t") or 0
    if key:
        value = input(">>>>>>  Value:\t") or 0
        if value:
            for k in todos["todos"].keys():
                print(f"Adding [{key}] to [{k}].")
                todos["todos"][k][key] = value


def print_params(bToggle_open_todos, bToggle_finished_todos, bToggle_comments, comments_id, bToggle_actions, tag, date_):
    color_open_todos = Fore.GREEN + 'open' if bToggle_open_todos else Fore.RED + 'open'
    color_finished_todos = Fore.GREEN + 'finished' if bToggle_finished_todos else Fore.RED + 'finished'
    if comments_id:
        color_comments = Fore.RED + 'comments' + f' (only {comments_id})'
    else:
        color_comments = Fore.GREEN + 'comments' if bToggle_comments else Fore.RED + 'comments'
    color_actions = Fore.GREEN + 'actions' if bToggle_actions else Fore.RED + 'actions'

    print(color_open_todos, color_finished_todos, color_comments, color_actions, 'Tag: ' + Fore.YELLOW + f'{tag}', Fore.YELLOW + f'{date_}' if date_ else '', sep=' | ')


def _main():
    global length_overall
    go = True
    bList_finished_todos = False
    bList_open_todos = True
    bList_actions = False
    bShow_comments = True
    bShow_tags = True
    bList_tags = False
    date_str = False
    show_this_id = None
    tag = "all"
    while go:
        today = str(datetime.date.today())
        # clear screen
        os.system('cls')

        # print("#" * length_overall, sep='')
        print("#" * ((length_overall // 2) - 4), Fore.YELLOW + " todoS ", "#" * ((length_overall // 2) - 5))
        # print("#" * length_overall)

        if bList_tags:
            list_tags('open')
            bList_tags = False
            action_input = input(">>  continue... ")
        else:
            if bList_finished_todos:
                print("\n##", Fore.BLUE + " FINISHED ", "#" * (length_overall - 12), sep='')
                list_todos('finished', tag, bShow_comments, bShow_tags, date_str, show_this_id)

            if bList_open_todos:
                x = length_overall - 12 - len(tag)
                print("\n##", Fore.GREEN + " OPEN ", "## ", Fore.YELLOW + f'{tag.upper()}', " ", "#" * x, "\n", sep='')
                list_todos('open', tag, bShow_comments, bShow_tags, date_str, show_this_id)
                print("\n", "#" * length_overall, sep='')


            print_params(bList_open_todos, bList_finished_todos, bShow_comments, show_this_id, bList_actions, tag, date_str)
            show_this_id = None                                  # Which ID shows comments - RESET
            # Reset date to show
            date_str = False

            if bList_actions:
                list_actions()

            action_input = input(">>  ") or 0

            if action_input == "resetall":
                sure = input(">>  SURE? Delete ALL?\t('yes'/'y'):  ")
                if sure.lower() in ['yes', 'y']:
                    todos["ids"] = 0
                    todos["todos"] = {}
                    dump_todo_list_to_json()
                continue
            elif action_input == "length":
                length_overall = int(input(">>  New length (" + str(length_overall) + "):  "))
                continue

            if action_input:
                # continue if missing todo id ("e4")
                if action_input in ['n', 'f', 'o', 'r', 'e']:
                    continue

                # *TAG_TO_FILTER "*992" - Default "all"
                if action_input[0] == "*":
                    # if len(action_input) > 1:
                    if re.match("^(\*)(\d)+$", action_input):
                        tag = action_input[1:]
                        continue
                    else:
                        tag = "all"
                # Filter by date
                elif re.match("^(<|>)(\d){4}-(\d){2}-(\d){2}", action_input):
                    date_str = action_input
                    continue

                action, todo_id, text, tags = extract_data(action_input)

                if action == "y":                                               # Cancel program
                    go = False
                elif action == "l":
                    if action_input.lower() == "lf":
                        bList_finished_todos = True                             # Show ONLY finished todos
                        bList_open_todos = False
                    elif action_input.lower() == "lt":                          # Show list of used tags
                        bList_tags = not bList_tags
                    else:
                        bList_finished_todos = not bList_finished_todos         # Toggle show finished todos
                        bList_open_todos = True
                elif action == "a":                                             # List all available actions
                    bList_actions = not bList_actions
                elif action == "c":
                    if todo_id:                                                 # Add comment
                        if text:
                            if len(todos["todos"][todo_id]["comment"][0]) == 0:
                                todos["todos"][todo_id]["comment"] = [[text, today]]
                            else:
                                todos["todos"][todo_id]["comment"].append([text, today])
                        else:
                            bShow_comments = False
                    else:
                        bShow_comments = not bShow_comments                     # Toggle show comments
                elif action == "n":                                             # New entry
                    todo_id = get_id()
                    todos["todos"][todo_id] = {}
                    todos["todos"][todo_id]["text"] = text
                    todos["todos"][todo_id]["status"] = "open"
                    todos["todos"][todo_id]["comment"] = [""]
                    todos["todos"][todo_id]["tags"] = tags
                    todos["todos"][todo_id]["date_added"] = today
                    todos["todos"][todo_id]["result"] = ""
                elif action == "f":                                             # Set status to FINISH
                    todos["todos"][todo_id]["status"] = "finished"
                    todos["todos"][todo_id]["result"] = [text, today]
                elif action == "o":                                             # Set status to OPEN
                    todos["todos"][todo_id]["status"] = "open"
                elif action == "r":                                             # Remove existing todo
                    todos["todos"].pop(todo_id, None)
                elif action == "e":                                             # Edit existing todo
                    todos["todos"][todo_id]["text"] = text
                elif action == "t":                                             # add tags
                    if todo_id:
                        # show_this_id = todo_id
                        if len(todos["todos"][todo_id]["tags"][0]) == 0:
                            todos["todos"][todo_id]["tags"] = tags
                        else:
                            for new_tag in tags:
                                if new_tag not in todos["todos"][todo_id]["tags"]:
                                    todos["todos"][todo_id]["tags"].append(new_tag)
                    else:
                        bShow_tags = not bShow_tags
                elif action == "addkey":                                             # Edit existing todo
                    add_key_value_to_my_todolist_json()
                dump_todo_list_to_json()


if __name__ == "__main__":
    _main()
