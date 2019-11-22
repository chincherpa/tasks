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
js_name = "todos_class.json"
path_to_js = os.path.join(dir_path, js_name)

length_overall = 90


class Todo:
    def __init__(self, todo_id, title, status, comment, tags, result, date_added):
        self.todo_id = todo_id
        self.title = title
        self.status = status
        self.comment = comment
        self.tags = tags
        self.result = result
        self.date_added = date_added

    def print_comment(self):
        for c in self.comment:
            length_comment = len(c[0])
            length_space = length_overall - (length_comment + 17)
            print(
                " " * 3,
                Fore.BLUE + f"{c[0]}",
                " " * length_space,
                Fore.BLUE + f"{c[1]}",
            )

    def print_tags(self):
        print(" " * 4, end="")
        if "high" in self.tags:
            print(Fore.WHITE + Back.RED + "HIGH", "- ", end="")
        elif "low" in self.tags:
            print(Fore.BLACK + Back.GREEN + "low", "- ", end="")
        for t in self.tags:
            if t in ["high", "low"]:
                continue
            else:
                print(Fore.YELLOW + f"{t}", "- ", end="")
        print("")

    def print_result(self):
        if len(self.result) > 0:
            length_result = len(self.result[0])
            length_space = length_overall - (length_result + 3 + 10)
            print(
                " " * 3,
                Fore.BLUE + f"{self.result[0]}",
                "." * length_space,
                Fore.BLUE + f"{self.result[1]}",
            )


def dump_todo_list_to_json():
    todos_out = {"ids": todos["ids"], "todos": {}}
    for t_id, instance in todos_classes.items():
        todos_out["todos"][t_id] = instance.__dict__
    with open(path_to_js, "w") as f:
        json.dump(todos_out, f, indent=4)


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

todos_classes = {}


def create_instances():
    for t_id, todo in todos["todos"].items():
        # print(t_id, todo)
        todos_classes[t_id] = Todo(**todo)


def get_id():
    new_id = todos["ids"] + 1
    todos["ids"] = new_id
    return str(new_id)


def list_all_todos():
    print("ids:", todos["ids"])
    for id_key, todo in todos["todos"].items():
        print("-" * 40)
        print(Fore.BLUE + f"{id_key}", todo["status"], todo["title"])
        print(Fore.YELLOW + f'{todo["tags"]}')


def filter_tag(id_key, tag):
    for t in todos_classes[id_key].tags:
        if t.lower() == tag:
            return True
    return False


def list_todos(
    status: str,
    tag_to_show: str = "all",
    show_comments: bool = True,
    show_tags: bool = True,
    show_date=False,
    id_to_show=None,
):
    for id_key, todo in todos_classes.items():
        title = todo.title
        length_title = len(title)
        date_added = todo.date_added
        length_space = length_overall - (length_title + 13)
        space_after_id = 3 - len(id_key)
        has_comments = len(todo.comment[0]) > 0

        if todo.status == status:

            # show only todos with date_added greater or lower than SHOW_DATE
            if show_date:
                gt_lt = show_date[0]

                if gt_lt == "<":
                    comp = operator.lt
                else:
                    comp = operator.gt

                date_ = show_date[1:]
                date_filter = datetime.datetime.strptime(date_, "%Y-%m-%d")
                todo_date = datetime.datetime.strptime(date_added, "%Y-%m-%d")
                if not comp(todo_date, date_filter):
                    continue

            tag_found = True
            if tag_to_show != "all":
                if len(todo.tags[0]) > 0:
                    tag_found = filter_tag(id_key, tag_to_show.lower())
                else:
                    continue

            if not tag_found:
                continue

            comments_plus = ""
            if not show_comments and has_comments:
                if id_to_show:
                    if id_key != id_to_show:
                        comments_plus = Fore.BLUE + "."
                else:
                    comments_plus = Fore.BLUE + "."

            if "privat" in todo.tags[0]:
                title = Fore.YELLOW + f"{title}"

            print(
                Fore.BLUE + f"{id_key}",
                " " * space_after_id,
                title,
                " " * length_space,
                date_added,
                comments_plus,
                sep="",
            )

            if show_comments and has_comments:
                todo.print_comment()
            elif id_key == id_to_show and has_comments:
                todo.print_comment()

            if show_tags:
                if len(todo.tags[0]) > 0:
                    todo.print_tags()

            if todo.status == "finished":
                if len(todo.result) > 0:
                    todo.print_result()


actions = {
    "Add todo 'n title'": "n",
    "Edit todo.title": "e",
    "Edit todo.title (replace)": "er",
    "Add comment": "c",
    "Add tag": "t",
    "Finish todo": "f",
    "Reopen todo": "r",
    "List all todo": "l",
    "List finished todos": "lf",
    "List tags": "lt",
    "List actions": "a",
    "Cancel": "y",
    "Reset ALL": "resetall",
    "Add key/value to todos.json": "addkey",
    "Filter todos by date": "<2019-01-01",
}


def list_actions():
    length = 37
    print("-" * (length + 1))
    for action, key in actions.items():
        x = length - len(action) - 6
        if action == "Reset ALL":
            x -= 6
            print(
                "|",
                Fore.YELLOW + f"{action}",
                " " * x,
                "[",
                Fore.YELLOW + f"{key.upper()}",
                "]",
                " |",
                sep="",
            )
        else:
            print(
                "|",
                Fore.YELLOW + f"{action}",
                " " * x,
                "[",
                Fore.YELLOW + f"{key.upper()}",
                "]",
                " " * (3 - len(key)),
                "|",
                sep="",
            )
    print("-" * (length + 1), "\n")


def list_tags(status: str):
    """
    Prints all used tags in todos with status and the number of their occurences

    Parameters:
    status (str): check only for todos with this status (open/finished)
    """
    space_max = 15
    num_of_tags = {}

    for id_key, todo in todos_classes.items():
        if todo.status == status:
            for t in todo.tags:
                if t:
                    if t in num_of_tags.keys():
                        num_of_tags[t] += 1
                    else:
                        num_of_tags[t] = 1

    tags = list(num_of_tags.keys())
    tags.sort()

    print("")
    print(
        "#" * ((length_overall // 2) - 6),
        Fore.YELLOW + " USED TAGS ",
        "#" * ((length_overall // 2) - 10),
    )
    print("")

    for tag in tags:
        space = space_max - len(tag)
        if tag.lower() == "high":
            print(Fore.RED + f"{tag}", " " * space, num_of_tags[tag])
        elif tag.lower() == "low":
            print(Fore.GREEN + f"{tag}", " " * space, num_of_tags[tag])
        elif tag.lower() == "privat":
            print(Fore.MAGENTA + f"{tag}", " " * space, num_of_tags[tag])
        else:
            print(tag, " " * space, num_of_tags[tag])


def extract_input(inp: str):
    action, todo_id, text = re.match("([a-zA-Z]+)(\d*) ?(.*]*)", inp).groups()

    # Action
    if action not in actions.values():
        action = None

    # Tags
    if action == "t":
        tags = [x.strip(" ") for x in text.split("*")[1:]]
    else:
        tags = None

    return action, todo_id, text, tags

    # # ACTION
    # ########################################## ([a-zA-Z]+)(\d*) ?(.*]*)
    # if inp == "resetall":
    #     action = "resetall"
    # elif inp == "addkey":
    #     action = "addkey"
    # else:
    #     action = inp[:1].lower()
    #     if action not in actions.values():
    #         action = None

    # # TAGS
    # tags = [x.strip(" ") for x in inp.split("*")[1:]]
    # if not tags:
    #     tags = [""]

    # # input Tags abschneiden
    # inp = inp.split("*")[0]
    # # todo ID
    # try:
    #     todo_id = re.search(r"\d+", inp).group()
    #     if todo_id not in todos["todos"].keys():
    #         todo_id = None
    # except AttributeError:
    #     todo_id = None

    # # title
    # try:
    #     title = inp.partition(todo_id)[2].strip()
    # except TypeError:
    #     try:
    #         title = inp.partition("n")[2].strip()
    #     except TypeError:
    #         title = None

    # # ONLY Python Ver. >= 3.8
    # # print(f'{action=}, {todo_id=}, {title=}, {tags=}')
    # # sleep(5)
    # return action, todo_id, title, tags


def print_params(
    bToggle_open_todos,
    bToggle_finished_todos,
    bToggle_comments,
    comments_id,
    bToggle_actions,
    tag,
    date_,
):
    color_open_todos = Fore.GREEN + "open" if bToggle_open_todos else Fore.RED + "open"
    color_finished_todos = (
        Fore.GREEN + "finished" if bToggle_finished_todos else Fore.RED + "finished"
    )
    if comments_id:
        color_comments = Fore.RED + "comments " + Fore.GREEN + f"(only {comments_id})"
    else:
        color_comments = (
            Fore.GREEN + "comments" if bToggle_comments else Fore.RED + "comments"
        )
    color_actions = Fore.GREEN + "actions" if bToggle_actions else Fore.RED + "actions"

    print(
        color_open_todos,
        color_finished_todos,
        color_comments,
        color_actions,
        "Tag: " + Fore.YELLOW + f"{tag}",
        Fore.YELLOW + f"{date_}" if date_ else "",
        sep=" | ",
    )


def _main():
    global length_overall
    go = True
    bList_finished_todos = False
    bList_open_todos = True
    bList_actions = False
    bShow_comments = False
    bShow_tags = False
    bList_tags = False
    date_str = False
    show_this_id = None
    tag = "all"

    create_instances()

    while go:
        today = str(datetime.date.today())
        # clear screen
        os.system("cls")

        # print("#" * length_overall, sep='')
        print(
            "#" * ((length_overall // 2) - 4),
            Fore.YELLOW + " ToDoS ",
            "#" * ((length_overall // 2) - 5),
        )
        # print("#" * length_overall)

        if bList_tags:
            list_tags("open")
            bList_tags = False
            input(">>  continue... ")
        else:
            if bList_finished_todos:
                print(
                    "\n##",
                    Fore.BLUE + " FINISHED ",
                    "#" * (length_overall - 12),
                    sep="",
                )
                list_todos(
                    "finished", tag, bShow_comments, bShow_tags, date_str, show_this_id
                )

            if bList_open_todos:
                x = length_overall - 12 - len(tag)
                print(
                    "\n##",
                    Fore.GREEN + " OPEN ",
                    "## ",
                    Fore.YELLOW + f"{tag.upper()}",
                    " ",
                    "#" * x,
                    "\n",
                    sep="",
                )
                list_todos(
                    "open", tag, bShow_comments, bShow_tags, date_str, show_this_id
                )
                print("\n", "#" * length_overall, sep="")

            print_params(
                bList_open_todos,
                bList_finished_todos,
                bShow_comments,
                show_this_id,
                bList_actions,
                tag,
                date_str,
            )
            print()
            show_this_id = None  # Which ID shows comments - RESET
            # Reset date to show
            date_str = False

            if bList_actions:
                list_actions()

            action_input = input(">>  ") or 0

            if action_input == "resetall":
                sure = input(">>  SURE? Delete ALL?\t('yes'/'y'):  ")
                if sure.lower() in ["yes", "y"]:
                    todos["ids"] = 0
                    todos["todos"] = {}
                    dump_todo_list_to_json()
                continue
            elif action_input == "length":
                length_overall = int(
                    input(">>  New length (" + str(length_overall) + "):  ")
                )
                continue

            if action_input:
                # continue if missing todo id ("e4")
                if action_input in ["n", "f", "o", "r", "e"]:
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

                action, todo_id, title, tags = extract_input(action_input)

                if action == "y":  # Cancel program
                    go = False
                elif action == "l":
                    if action_input.lower() == "lf":
                        bList_finished_todos = True  # Show ONLY finished todos
                        bList_open_todos = False
                    elif action_input.lower() == "lt":  # Show list of used tags
                        bList_tags = not bList_tags
                    else:
                        bList_finished_todos = (
                            not bList_finished_todos
                        )  # Toggle show finished todos
                        bList_open_todos = True
                elif action == "a":  # List all available actions
                    bList_actions = not bList_actions
                elif action == "c":
                    if todo_id:  # Add comment
                        if title:
                            if todos_classes[todo_id].comment[0] == 0:
                                todos_classes[todo_id].comment = [[title, today]]
                            else:
                                todos_classes[todo_id].comment.append([title, today])
                            # if len(todos["todos"][todo_id]["comment"][0]) == 0:
                            #     todos["todos"][todo_id]["comment"] = [[title, today]]
                            # else:
                            #     todos["todos"][todo_id]["comment"].append([title, today])
                        else:
                            bShow_comments = False
                        show_this_id = todo_id
                    else:
                        bShow_comments = not bShow_comments  # Toggle show comments
                elif action == "n":  # New entry
                    todo_id = get_id()
                    todos_classes[todo_id] = Todo(
                        todo_id, title, "open", [""], tags, "", today
                    )

                    # todos["todos"][todo_id] = {}
                    # todos["todos"][todo_id]["title"] = title
                    # todos["todos"][todo_id]["status"] = "open"
                    # todos["todos"][todo_id]["comment"] = [""]
                    # todos["todos"][todo_id]["tags"] = tags
                    # todos["todos"][todo_id]["date_added"] = today
                    # todos["todos"][todo_id]["result"] = ""
                elif action == "f":  # Set status to FINISH
                    todos_classes[todo_id].status = "finished"
                    todos_classes[todo_id].result = [title, today]
                elif action == "r":  # Set status to OPEN
                    todos_classes[todo_id].status = "open"
                elif action == "e":  # Edit existing todo
                    if action_input[:2].lower() == "er":
                        if len(title.split(">")) == 2:
                            old, new = title.split(">")
                            new_title = todos_classes[todo_id].title.replace(old, new)
                            print("#", new_title, "#")
                            ok = input("Apply changes?:\t")
                            if ok.lower() in ["y", "yes"]:
                                todos_classes[todo_id].title = new_title
                    else:
                        todos_classes[todo_id].title = title
                elif action == "t":  # add tags
                    if todo_id:
                        # show_this_id = todo_id
                        if len(todos_classes[todo_id].tags[0]) == 0:
                            todos_classes[todo_id].tags = tags
                        else:
                            for new_tag in tags:
                                if new_tag not in todos_classes[todo_id].tags:
                                    todos_classes[todo_id].tags.append(new_tag)
                    else:
                        bShow_tags = not bShow_tags

                dump_todo_list_to_json()


if __name__ == "__main__":
    _main()
