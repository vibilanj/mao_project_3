import argparse
from formatting import convert_solution_to_schedule, show_schedule
from parse import ScheduleParser
from scheduler import Scheduler


# Get the schedule file path from the command line arguments.
argparser = argparse.ArgumentParser("main")
argparser.add_argument(
    "--schedule",
    type=str,
    default="schedule.txt",
    help="path to the schedule file")
args = argparser.parse_args()

# NOTE: Activity names must be provided first before adding events and tasks as
#   they are required to create the binary variables for the problem. This is
#   one of the reasons why it is better to read the schedule from a file.

# Parse the schedule file and get the list of activities, events, and tasks to add.
activities, event_args, task_args = ScheduleParser(args.schedule).parse_schedule()

# Create the scheduler, add the events and tasks and get the optimized solution.
scheduler = Scheduler(activities)
for event_args in event_args:
    scheduler.add_event(*event_args)
for task_args in task_args:
    scheduler.add_task(*task_args)
sol = scheduler.solve()

# NOTE: doesn't check if the schedule is possible to be optimized, or whether
#   all the constraints are met.

# Convert the solution to a human-readable schedule and display it.
schedule = convert_solution_to_schedule(sol, activities)
show_schedule(schedule)
