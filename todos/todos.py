#!/usr/bin/env python

from time import sleep

import datetime
import json
import operator
import os
from pathlib import Path
import re
import sys

from colorama import init, Fore
from emoji import emojize

init(autoreset=True)
# colorama: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.

dir_path = os.path.dirname(os.path.realpath(__file__))
js_name = "todos.json"
global path_to_js
path_to_js = os.path.join(dir_path, js_name)

width_overall = 90

EMOJI_HIGH = ":collision:"
EMOJI_LOW = ":small_blue_diamond:"
EMOJI_PRIVAT = ":construction:"

TEST = "ABC"


class Todo:
    def __init__(
        self, id, title, status, comments, tags, result, date_added, rem_time
    ):

        self.id = id
        self.title = title
        self.status = status
        self.comments = comments
        self.tags = tags
        self.result = result
        self.date_added = date_added
        self.rem_time = rem_time

    def print_comments(self):
        for c in self.comments:
            length_comment = len(c[0])
            length_space = width_overall - (length_comment + 17)
            print(
                " " * 3,
                Fore.BLUE + f"{c[0]}",
                " " * length_space,
                Fore.BLUE + f"{c[1]}",
            )

    def print_tags(self):
        output = " " * 4
        dash = ""
        if "privat" in self.tags:
            output += dash + Fore.CYAN + emojize(EMOJI_PRIVAT)
            dash = "  - "
        if "high" in self.tags:
            output += dash + Fore.RED + emojize(EMOJI_HIGH)
            dash = "  - "
        if "low" in self.tags:
            output += dash + Fore.BLUE + emojize(EMOJI_LOW)
            dash = "  - "

        for t in self.tags:
            if t in ["high", "low", "privat"]:
                continue
            elif len(t) > 0:
                output += dash + Fore.YELLOW + f"{t}"
                dash = " - "

        print(output)

    def print_result(self):
        # if len(self.result) > 0:
        length_result = len(self.result[0])
        length_space = width_overall - (length_result + 5 + 10)
        print(
            " " * 3,
            Fore.BLUE + f"{self.result[0]}",
            " " * length_space,
            Fore.BLUE + f"{self.result[1]}",
        )

    def print_rem_time(self):
        today = datetime.date.today()
        dateformat = "%Y-%m-%d %H:%M:%S"
        rem_time = datetime.datetime.strptime(self.rem_time, dateformat)
        if rem_time.date() <= today:
            print(" " * 3, Fore.RED + f"-> {self.rem_time}")
        else:
            print(" " * 3, Fore.BLUE + f"-> {self.rem_time}")


def load_json(path):
    try:
        if path[-5:] == ".json":
            path_to_js = Path(path)
            if path_to_js.is_file():
                with open(path_to_js, "r") as jsf:
                    todos = json.load(jsf)
                return path_to_js, todos
    except IndexError as e:
        print(f"Something is wrong!\n{e}")
        sleep(2)


def dump_todo_list_to_json():
    todos_out = {"ids": todos["ids"], "langEN": True, "todos": {}}
    for t_id, instance in todos_classes.items():
        todos_out["todos"][t_id] = instance.__dict__
    with open(path_to_js, "w") as f:
        json.dump(todos_out, f, indent=4)


if not os.path.isfile(path_to_js):
    print("not os.path.isfile(path_to_js)")
    todos = {"ids": 0, "langEN": True, "todos": {}}
    with open(path_to_js, "w") as f:
        json.dump(todos, f, indent=4)
else:
    with open(path_to_js, "r") as jsf:
        todos = json.load(jsf)

todos_classes = {}


def create_instances(todos):
    for t_id, todo in todos["todos"].items():
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

    has_no_comments = False
    lto_remind = []
    now = datetime.datetime.now()
    dateformat = "%Y-%m-%d %H:%M:%S"

    for id_key, todo in todos_classes.items():
        title = todo.title
        length_title = len(title)
        date_added = todo.date_added
        rem_time = todo.rem_time
        length_space = width_overall - (length_title + 13)
        space_after_id = 3 - len(id_key)
        has_comments = len(todo.comments[0]) > 0

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
                if len(todo.tags) > 0:
                    tag_found = filter_tag(id_key, tag_to_show.lower())
                else:
                    continue

            if not tag_found:
                continue

            comments_plus = ""
            if not show_comments and has_comments:
                if id_to_show:
                    if id_key != id_to_show:
                        comments_plus = Fore.BLUE + "+"
                else:
                    comments_plus = Fore.BLUE + "+"

            if "privat" in todo.tags:
                title = Fore.YELLOW + f"{title}"

            if "high" in todo.tags:
                colorID = Fore.RED + f"{id_key}"
            elif "low" in todo.tags:
                colorID = Fore.BLUE + f"{id_key}"
            else:
                colorID = Fore.YELLOW + f"{id_key}"

            print(
                colorID,
                " " * space_after_id,
                title,
                " " * length_space,
                date_added,
                comments_plus,
                sep="",
            )

            if show_comments and has_comments:
                todo.print_comments()
            elif id_key == id_to_show and has_comments:
                todo.print_comments()

            if show_tags:
                if len(todo.tags) > 0:
                    todo.print_tags()

            if todo.status == "finished":
                if len(todo.result) > 0:
                    todo.print_result()

            if len(rem_time) > 0:
                todo.print_rem_time()
                rem_time_dt = datetime.datetime.strptime(rem_time, dateformat)
                res = rem_time_dt - now
                # h = divmod(res.seconds, 3600)
                # h[0] = Stunden
                # h[1] = Sekunden
                # m = divmod(h[1]), 60)
                # m[0] = Minuten
                # m[1] = Sekunden
                if res.days < 1:
                    lto_remind.append((rem_time, id_key, title))

            if status == "open":
                if id_key == id_to_show and not has_comments:
                    has_no_comments = True

    return has_no_comments, lto_remind


actions = {
    "Add todo [n title]": "n",
    "Edit todo.title": "e",
    "Search/replace todo.title [old|new]": "er",
    "Add comment": "c",
    "Add tag": "t",
    "Add reminder [rem#]": "rem",
    "Delete reminder [rem# del]": "",
    "Finish todo [f#]": "f",
    "Toggle show finished todos": "f",
    "Toggle show open todos": "o",
    "Reopen todo": "r",
    "List all todo": "l",
    "List tags": "lt",
    "Show this list": "a",
    "Cancel": "y",
    "Reset ALL": "resetall",
    "Filter todos by date": "<2019-01-01",
    "Set new width": "width",
    "Load existing todos.json": "load",
    "Show path to .json-file": "file",
    "Toogle language": "lang",
}

actionsDE = {
    # --------------------------------------
    "Neues Todo [n title]": "n",
    "todo.title editieren": "e",
    "Su/Ers in todo.title [alt|neu]": "er",
    "Kommentar hinzufügen": "c",
    "Tag hinzufügen": "t",
    "Erinnerung hinzufügen [rem#]": "rem",
    "Erinnerung löschen [rem# del]": "",
    "todo beenden [f#]": "f",
    "Toggle zeige beendete todos": "f",
    "Toggle zeige offene todos": "o",
    "todo wieder öffnen": "r",
    "Zeige alle todo": "l",
    "Zeige tags": "lt",
    "Zeige diese Liste": "a",
    "ALLES resetten": "resetall",
    "Filter todos nach Datum": "<2019-01-01",
    "Neue Breite": "width",
    "Lade existierendes todos.json": "load",
    "Zeige Pfad zu .json-Datei": "file",
    "Toogle Sprache": "lang",
    "Beenden": "y",
}


def toggle_language():
    todos["langEN"] = not todos["langEN"]
    print(f"Language set to: {'EN' if todos['langEN'] else 'DE'}")
    sleep(0.5)


def list_actions():
    length = 41
    print("-" * (length + 1))
    a = [actionsDE, actions]
    for action, command in a[todos["langEN"]].items():
        len_action = len(action)
        len_command = len(command)
        x = length - len_action - len_command - 4

        print(
            "|",
            Fore.YELLOW + f"{action}",
            " " * x,
            "[",
            Fore.YELLOW + f"{command}",
            "]",
            " |",
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
        "#" * ((width_overall // 2) - 6),
        Fore.YELLOW + " USED TAGS ",
        "#" * ((width_overall // 2) - 10),
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
    # groups = re.search(r'(?P<title>.*)$\n.*Highlight on Page (?P<page>\d+).*Added on (?P<dts>.*)$\n\n(?P<text>.*)$', entry, re.MULTILINE)
    # assert groups is not None, "Couldn't match regex!"

    if inp[0] == "*":
        return "*", None, None, None
    if inp[0] == "?":
        return "a", None, None, None

    try:
        action, todo_id, text = re.match(r"([a-zA-Z]+) ?(\d*) ?(.*]*)", inp).groups()
    except AttributeError:
        return None, None, None, None

    # Action
    if action not in actions.values():
        action = None

    # Tags
    if action in ["n", "t"]:
        tags = [x.strip(" ") for x in text.split("*")[1:]]
        text = text.split("*")[0].strip(" ")
    else:
        tags = [""]

    return action, todo_id, text, tags


def print_params(
    bToggle_open_todos,
    bToggle_finished_todos,
    bToggle_comments,
    bToggle_tags,
    comments_id,
    bToggle_actions,
    tag,
    date_,
):
    color_open_todos = (
        Fore.GREEN + f"{'open' if todos['langEN'] else 'offen'}"
        if bToggle_open_todos
        else Fore.RED + f"{'open' if todos['langEN'] else 'offen'}"
    )
    color_finished_todos = (
        Fore.GREEN + f"{'finished' if todos['langEN'] else 'abgeschlossene'}"
        if bToggle_finished_todos
        else Fore.RED + f"{'finished' if todos['langEN'] else 'abgeschlossene'}"
    )

    if comments_id:
        # color_comments = Fore.RED + "comments " + Fore.GREEN + f"(only {comments_id})"
        color_comments = (Fore.RED + f"{'comments' if todos['langEN'] else 'Kommentare'}"
            + Fore.GREEN
            + f"{f'(only {comments_id})' if todos['langEN'] else f'(nur {comments_id})'})"
        )
    else:
        color_comments = (
            Fore.GREEN + "comments" if bToggle_comments else Fore.RED + "comments"
        )

    color_actions = (
        Fore.GREEN + f"{'actions' if todos['langEN'] else 'Befehle'}"
        if bToggle_actions
        else Fore.RED + f"{'actions' if todos['langEN'] else 'Befehle'}"
    )
    color_tags = Fore.GREEN + "Tags: " if bToggle_tags else Fore.RED + "Tags: "
    date = Fore.YELLOW + f"{date_} " if date_ else ""

    print(
        color_open_todos,
        color_finished_todos,
        color_comments,
        color_actions,
        color_tags + Fore.YELLOW + f"{tag}",
        date,
        sep=" | ",
    )


def get_num_of_todos(status):
    num = 0
    for _, todo in todos_classes.items():
        if todo.status == status:
            num += 1
    return num


def print_todos(status, tag, bShow_comments, bShow_tags, date_str, show_this_id):
    inum_todos = get_num_of_todos(status)
    len_inum_todos = len(str(inum_todos))
    tag_ = ""
    if status == "open":
        len_tag = len(tag) + 2
        tag_ = Fore.YELLOW + f" {tag.upper() } "
    elif status == "finished":
        len_tag = 0

    x = width_overall - len(status) - len_tag - len_inum_todos - 15
    print(
        "\n## ",
        Fore.BLUE + f"{status}",
        " ##",
        tag_,
        f"## {inum_todos} Todos ",
        "#" * x,
        "\n",
        sep="",
    )

    has_no_comments, lto_remind = list_todos(
        status, tag, bShow_comments, bShow_tags, date_str, show_this_id
    )

    print("\n", "#" * (width_overall + 1), sep="")
    return has_no_comments, lto_remind


def set_reminder(todo_id, text):
    if re.match(r"\d{4}-\d{2}-\d{2} \d+", text):
        rem_time = datetime.datetime.strptime(text + ":00:00", "%Y-%m-%d %H:%M:%S")
    elif re.match(r"\d{4}-\d{2}-\d{2}", text):
        rem_time = datetime.datetime.strptime(text + " 12:00:00", "%Y-%m-%d %H:%M:%S")
    elif text[0] == "t":  # tomorrow at this time
        rem_time = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    else:
        try:
            stime, sunit = re.match(r"(\d*)\s*(hour|day|week|del)", text).groups()
            if sunit == "del":
                rem_time = ""
            else:
                itime = int(stime)
                if sunit == "hour":

                    rem_time = (
                        datetime.datetime.now() + datetime.timedelta(hours=itime)
                    ).strftime("%Y-%m-%d %H:%M:%S")

                elif sunit == "day":

                    rem_time = (
                        datetime.datetime.now() + datetime.timedelta(days=itime)
                    ).strftime("%Y-%m-%d %H:%M:%S")

                elif sunit == "week":

                    rem_time = (
                        datetime.datetime.now() + datetime.timedelta(weeks=itime)
                    ).strftime("%Y-%m-%d %H:%M:%S")

        except AttributeError as e:
            print(f"Error: {e}")
            sys.exit()

    todos_classes[todo_id].rem_time = rem_time


def print_lto_remind(list_in):
    print(f"{len(list_in)} {'upcoming' if todos['langEN'] else 'kommende'} todos:")
    for r in list_in:
        print(Fore.RED + f"{r[0]}", Fore.YELLOW + f"{r[1]}", r[2])


def run(todos):
    global width_overall
    bList_finished_todos = False
    bList_open_todos = True
    bList_actions = False
    bShow_comments = False
    bShow_tags = False
    bList_tags = False
    date_str = False
    show_this_id = None
    b_rem_explain = False
    tag = "all"

    create_instances(todos)

    while True:
        today = str(datetime.date.today())
        # clear screen
        os.system("cls")

        print(
            "#" * ((width_overall // 2) - 4),
            Fore.YELLOW + " ToDoS ",
            "#" * ((width_overall // 2) - 4),
        )

        if bList_tags:
            list_tags("open")
            bList_tags = False
            input(">>  continue... ")
        else:
            if bList_finished_todos:
                has_no_comment, lto_remind = print_todos(
                    "finished", tag, bShow_comments, bShow_tags, date_str, show_this_id
                )

            if bList_open_todos:
                has_no_comment, lto_remind = print_todos(
                    "open", tag, bShow_comments, bShow_tags, date_str, show_this_id
                )

            print_params(
                bList_open_todos,
                bList_finished_todos,
                bShow_comments,
                bShow_tags,
                show_this_id,
                bList_actions,
                tag,
                date_str,
            )
            print()

            if lto_remind:
                print_lto_remind(lto_remind)
            print()

            if has_no_comment:
                print(f"Todo {show_this_id} has no comments!")

            if b_rem_explain:
                # print("Set reminder:")
                # print("Delete reminder from id: rem[id] del")
                # print("Set reminder in x hours: rem[id] xhours")
                # print("Set reminder in x days: rem[id] xdays")
                # print("Set reminder in x weeks: rem[id] xweeks")
                # print("Set reminder on date 12o'clock: rem[id] 2020-12-31")
                # print("Set reminder on date and xo'clock: rem[id] 2020-12-31 x")
                # print()

                print(
                    """Set reminder:
    Delete reminder from id: 'rem[id] del'
    Set reminder in x hours: 'rem[id] xhours'
    Set reminder in x days: 'rem[id] xdays'
    Set reminder in x weeks: 'rem[id] xweeks'
    Set reminder on date 12o'clock: 'rem[id] 2020-12-31'
    Set reminder on date and xo'clock: 'rem[id] 2020-12-31 x'"""
                )

                print()
                b_rem_explain = False

            show_this_id = None  # Which ID shows comments - RESET
            date_str = False  # Reset date to show

            if bList_actions:
                list_actions()
                bList_actions = False

            action_input = input(">>  ") or 0
            now = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            if action_input == "resetall":

                sure = input(">>  SURE? Delete ALL?\t('yes'/'y'):  ")
                if sure.lower() in ["yes", "y"]:
                    todos["ids"] = 0
                    todos["todos"] = {}

                    dump_todo_list_to_json()
                continue
            elif action_input == "width":
                width_overall = int(
                    input(">>  New width (" + str(width_overall) + "):  ")
                )
                continue

            if action_input:
                # continue if missing id ("e4")
                if action_input in ["r", "e"]:
                    print("Missing #")
                    sleep(2)
                    continue

                # *TAG_TO_FILTER "*992" - Default "all"
                if action_input[0] == "*":
                    if re.match(r"^(\*)(.)+$", action_input):
                        tag = action_input[1:]
                        continue
                    else:
                        tag = "all"
                        continue

                # Filter by date
                elif re.match(r"^[<>]\d{4}-\d{2}-\d{2}", action_input):
                    date_str = action_input
                    continue

                action, todo_id, text, tags = extract_input(action_input)

                if action == "a":  # List all available actions
                    bList_actions = not bList_actions
                elif action == "c":
                    if todo_id:  # Add comment
                        if text:
                            if len(todos_classes[todo_id].comments[0]) == 0:
                                todos_classes[todo_id].comments = [[text, today]]
                            else:
                                todos_classes[todo_id].comments.append([text, today])
                        else:
                            bShow_comments = False
                        show_this_id = todo_id
                    else:
                        bShow_comments = not bShow_comments  # Toggle show comments
                elif action == "e":  # Edit existing todo.title
                    todos_classes[todo_id].title = text
                elif action == "er":  # Replace string in todo.title
                    if len(text.split("|")) == 2:
                        old, new = text.split("|")
                        new_title = todos_classes[todo_id].title.replace(old, new)
                        print("#", new_title, "#")
                        ok = input("Apply changes?:['y']\t")
                        if ok.lower() in ["y", "yes"]:
                            todos_classes[todo_id].title = new_title
                    else:
                        print("old_string|new_string")
                        sleep(3)
                elif action == "f":  # Set status to FINISH
                    if todo_id:
                        todos_classes[todo_id].status = "finished"
                        todos_classes[todo_id].result = [text, today]
                    else:

                        bList_finished_todos = (
                            not bList_finished_todos
                        )  # Show ONLY finished todos

                        # bList_open_todos = not bList_open_todos
                elif action == "file":
                    print(path_to_js)
                    sleep(5)
                elif action == "l":
                    bList_finished_todos = (
                        not bList_finished_todos
                    )  # Toggle show finished todos
                    # bList_open_todos = True
                elif action == "lang":  # Toggle language
                    toggle_language()
                elif action == "load":  # Show list of used tags
                    path_to_js, todos = load_json(text)
                    if todos:
                        create_instances(todos)

                elif action == "lt":  # Show list of used tags
                    bList_tags = not bList_tags
                elif action == "n":  # New entry
                    todo_id = get_id()
                    # (todo_id, title, status, comments, tags, result, date_added)

                    todos_classes[todo_id] = Todo(
                        todo_id, text, "open", [""], tags, "", today, ""
                    )

                elif action == "o":  # Toggle show opened
                    bList_open_todos = not bList_open_todos
                elif action == "r":  # Set status to OPEN
                    todos_classes[todo_id].status = "open"
                elif action == "rem":  # add tags
                    if text:
                        set_reminder(todo_id, text)
                    else:
                        b_rem_explain = True
                elif action == "t":  # add tags
                    if todo_id:
                        if len(todos_classes[todo_id].tags) == 0:
                            todos_classes[todo_id].tags = tags
                        else:
                            for new_tag in tags:
                                if new_tag not in todos_classes[todo_id].tags:
                                    todos_classes[todo_id].tags.append(new_tag)
                    else:
                        bShow_tags = not bShow_tags
                elif action == "y":  # Cancel program

                    break

                dump_todo_list_to_json()
                # sleep(30)


def main():
    run(todos)


if __name__ == "__main__":
    main()
