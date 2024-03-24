# Modelling and Optimization Project 3

## Introduction

This project is a scheduling tool that helps students plan their weekly schedules efficiently. The tool takes into account various constraints such as class timings, assignment openings, and assignment deadlines to generate an optimized schedule. The core functionality of the program involves formulating the scheduling problem as an integer programming model, where classes and assignments are represented as decision variables. Constraints are defined and the objective function is designed to maximize free time.

## Implementation Details

The project is implemented in Python. Initially, I was planning to use the `pyomo` library to model and solve the integer programming problem. However, I found that the `pulp` library is more user-friendly and easier to work with for this project. Therefore, I decided to use the `pulp` library to model and solve the scheduling problem.

Another change I made was to read the schedule requirements from a text file instead of taking user input directly. This makes it easier for the user to input complex schedules and constraints without having to interact with the program through a command line interface. The program reads the schedule requirements from the file and generates an optimized schedule based on the constraints and preferences provided.

Here are the descriptions of the five Python files and the input file. Furthermore, the code in each file is documented with comments to explain each part in greater detail.

### `constants.py`

### `parse.py`

### `scheduler.py`

### `formatting.py`

### `main.py`

### `schedule.txt`

## Further Improvements

## Notes:
1. Activity names must be provided first before adding events and tasks as they are required to create the binary variables for the problem. This is one of the reasons why it is better to read the schedule from a file.
2. The program doesn't check if the schedule is possible to be optimized, or whether the provided solution meets all the constraints.
3. The program might break when too many tasks and events are added. Other solvers are available within PuLP, but they are not as user-friendly as the default solver. They would have to be installed by the user and linked to the program. However, these solvers might be better at handling large problems.

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
