import argparse
from formatting import convert_solution_to_schedule, show_schedule
from parse import ScheduleParser
from scheduler import Scheduler


argparser = argparse.ArgumentParser("main")
argparser.add_argument(
    "--schedule",
    type=str,
    default="schedule.txt",
    help="path to the schedule file")
args = argparser.parse_args()

# NOTE: Activity names must be provided first before adding events and tasks as
#   they are required to create the binary variables for the problem > One of
#   the reasons why it is better to read the schedule from a file
activities, event_args, task_args = ScheduleParser(args.schedule).parse_schedule()

scheduler = Scheduler(activities)
for event_args in event_args:
    scheduler.add_event(*event_args)
for task_args in task_args:
    scheduler.add_task(*task_args)
sol = scheduler.solve()

schedule = convert_solution_to_schedule(sol, activities)
show_schedule(schedule)
# NOTE: doesn't check if the schedule is possible to be optimized, or whether
#   all the constraints are met