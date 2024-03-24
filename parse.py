from constants import EMPTY_NAME


activities = set([EMPTY_NAME])
events = []
tasks = []


def clean_lines(lines):
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line != ""]
    lines = [line for line in lines if line[0] != "#"]
    return lines 


def check_name(name):
    if name == "EMPTY_NAME":
        raise Exception(f"Name cannot be {EMPTY_NAME}")


def check_day(day):
    if day not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
        raise Exception(f"Day should be Monday, Tuesday, Wednesday, Thursday, or Friday, got {day}")


def check_time(time):
    hours, minutes = time.split(":")
    if int(hours) < 9 or int(hours) > 19:
        raise Exception(f"Hours should be between 09 and 19, got {hours}")
    if minutes not in ["00", "30"]:
        raise Exception(f"Minutes should be 00 or 30, got {minutes}")


def check_hours_required(hours):
    if hours < 0 or hours > 50:
        raise Exception(f"Hours required should be between 0 and 8, got {hours}")


def handle_event(name, day, start_time, end_time):
    # Input validation
    check_name(name)
    check_day(day)
    check_time(start_time)
    check_time(end_time)

    activities.add(name)
    add_event_args = (name, (day, start_time), (day, end_time))
    events.append(add_event_args)


def handle_task(name, hours_required, start_day, start_time, deadline_day, deadline_time):
    # Input validation
    check_name(name)
    hours_required = int(hours_required)
    check_hours_required(hours_required)
    check_day(start_day)
    check_time(start_time)
    check_day(deadline_day)
    check_time(deadline_time)

    activities.add(name)
    add_task_args = (name, hours_required, (start_day, start_time), (deadline_day, deadline_time))
    tasks.append(add_task_args)


def parse_schedule(filename):
    f = open(filename, "r")
    lines = f.readlines()
    for line in clean_lines(lines):
        split_line = line.split(" ")
        keyword = split_line[0]
        if keyword == "EVENT":
            args = split_line[1:]
            args = [arg for arg in args if arg != ""]
            if len(args) != 4:
                raise Exception(f"EVENT keyword should have 4 arguments, got {len(args)}")
            handle_event(*args)
            
        elif keyword == "TASK":
            args = split_line[1:]
            args = [arg for arg in args if arg != ""]
            if len(args) != 6:
                raise Exception(f"TASK keyword should have 6 arguments, got {len(args)}")
            handle_task(*args)

        else:
            raise Exception(f"Keyword should be EVENT or TASK, got {keyword}")
        
    return list(activities), events, tasks
