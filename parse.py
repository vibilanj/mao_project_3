from constants import EMPTY_NAME


class ScheduleParser:
    def __init__(self, filename):
        self.filename = filename
        self.activities = set([EMPTY_NAME])
        self.events = []
        self.tasks = []


    def clean_lines(self, lines):
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if line != ""]
        lines = [line for line in lines if line[0] != "#"]
        return lines


    def check_name(self, name):
        if name == "EMPTY_NAME":
            raise Exception(f"Name cannot be {EMPTY_NAME}")


    def check_day(self, day):
        if day not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
            raise Exception(f"Day should be Monday, Tuesday, Wednesday, Thursday, or Friday, got {day}")


    def check_time(self, time):
        hours, minutes = time.split(":")
        if int(hours) < 9 or int(hours) > 19:
            raise Exception(f"Hours should be between 09 and 19, got {hours}")
        if minutes not in ["00", "30"]:
            raise Exception(f"Minutes should be 00 or 30, got {minutes}")


    def check_hours_required(self, hours):
        if hours < 0 or hours > 50:
            raise Exception(f"Hours required should be between 0 and 8, got {hours}")


    def handle_event(self, name, day, start_time, end_time):
        # Input validation
        self.check_name(name)
        self.check_day(day)
        self.check_time(start_time)
        self.check_time(end_time)

        self.activities.add(name)
        add_event_args = (name, (day, start_time), (day, end_time))
        self.events.append(add_event_args)


    def handle_task(self, name, hours_required, start_day, start_time, deadline_day, deadline_time):
        # Input validation
        self.check_name(name)
        hours_required = int(hours_required)
        self.check_hours_required(hours_required)
        self.check_day(start_day)
        self.check_time(start_time)
        self.check_day(deadline_day)
        self.check_time(deadline_time)

        self.activities.add(name)
        add_task_args = (name, hours_required, (start_day, start_time), (deadline_day, deadline_time))
        self.tasks.append(add_task_args)


    def parse_schedule(self):
        f = open(self.filename, "r")
        lines = f.readlines()
        for line in self.clean_lines(lines):
            split_line = line.split(" ")
            keyword = split_line[0]
            if keyword == "EVENT":
                args = split_line[1:]
                args = [arg for arg in args if arg != ""]
                if len(args) != 4:
                    raise Exception(f"EVENT keyword should have 4 arguments, got {len(args)}")
                self.handle_event(*args)

            elif keyword == "TASK":
                args = split_line[1:]
                args = [arg for arg in args if arg != ""]
                if len(args) != 6:
                    raise Exception(f"TASK keyword should have 6 arguments, got {len(args)}")
                self.handle_task(*args)

            else:
                raise Exception(f"Keyword should be EVENT or TASK, got {keyword}")
            
        return list(self.activities), self.events, self.tasks
