# Modelling and Optimization Project 3

## Proposal

The project proposes the development of a scheduling tool for college students using integer programming techniques. The tool will assist students in efficiently planning their schedules by considering various constraints such as class timings, assignment deadlines, and dependencies between tasks.

The core functionality of the program involves formulating the scheduling problem as an integer programming model, where classes and assignments are represented as decision variables. Constraints will be defined to ensure that classes do not overlap, assignments are started after relevant classes, and deadlines are met. Additionally, the objective function will be designed to optimize factors such as minimizing the total time spent on campus or maximizing free time between classes.

To demonstrate the process, users will interact with a user-friendly interface where they can input their class schedule, assignment deadlines, and other constraints. The program will then utilize the `pyomo` library to solve the integer programming model, generating an optimized schedule tailored to the user's preferences and constraints.

## Introduction

## Implementation Details

## Further Improvements

## How to Run

### Setting up the environment

1. Ensure that you have a working install of Python 3.11.8.
2. Navigate to the directory containing the project in your terminal.
3. Create a Python virtual environment by running `python3 -m venv .venv`.
4. Use the virtual environment with `source .venv/bin/activate`.
5. Install the necessary packages using `pip install -r requirements.txt`.

### Running the program

1. Navigate to the project directory.
2. Make sure that the virtual environment is activated. If it is not, use `source .venv/bin/activate`.
3. Run the program using `python main.py` and pass in any optional arguments.
    - You can use the `-h` flag to see the help message and the available arguments.
4. By default, the program will read the schedule requirements from the `schedule.txt` file.
    - You can instead  provide a different file by using the `--schedule` argument.
    - An example command would be `python main.py --schedule my_schedule.txt`. This would read the schedule requirements from the `my_schedule.txt` file.
4. View the schedule created by the integer programming solver in the terminal output.

## Notes:
1. Activity names must be provided first before adding events and tasks as they are required to create the binary variables for the problem. This is one of the reasons why it is better to read the schedule from a file.
2. The program doesn't check if the schedule is possible to be optimized, or whether the provided solution meets all the constraints.
3. The program might break when too many tasks and events are added. Other solvers are available within PuLP, but they are not as user-friendly as the default solver. They would have to be installed by the user and linked to the program. However, these solvers might be better at handling large problems.
