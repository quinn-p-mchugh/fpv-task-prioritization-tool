# RESOURCES:
# Final Version Perfected (FVP): https://www.lesswrong.com/posts/xfcKYznQ6B9yuxB28
# * Original article: http://archive.constantcontact.com/fs004/1100358239599/archive/1109511856508.html#LETTER.BLOCK4
# Binary priorization: https://en.wikipedia.org/wiki/Binary_prioritization
# A human-driven sort algorithm (MonkeySort): https://leonid.shevtsov.me/post/a-human-driven-sort-algorithm-monkeysort/


from typing import TextIO
from pathlib import Path
import atexit
from configparser import ConfigParser
import pandas as pd


def get_task_list(file_path: Path):
    """Gets the task list from a plain text file and returns a list of tasks."""


def at_exit(tasks_file: TextIO):
    tasks_file.close()


def is_preferred(task, preferred_task):
    """Returns whether or not the user prefers the another task more than the current preferred task."""
    print(
        f"WHICH IS HIGHER PRIORITY?\n[1] {preferred_task}\n[2] {task}\nEnter '1' or '2'."
    )
    valid_responses = ["1", "2"]
    while True:
        response = input()
        if response.strip() in valid_responses:
            break
        else:
            print("Not a valid response.")
            erase_prev_lines(1)
    return False if response == "1" else True


def get_most_preferred(df):
    return df[df["pref_count"] == 1].iloc[-1]


def erase_prev_lines(num_lines: int):
    for i in range(num_lines):
        print("\033[1A")
        print("\033[K")


def main():
    config = ConfigParser()
    config.read((Path(__file__).parents[0] / "config.ini"))

    tasks_df = load_tasks_from_file(Path(config["FilePaths"]["TODOFile"]))

    tasks_df = shuffle_df(tasks_df)

    tasks_df = prioritize_tasks(tasks_df)
    highest_priority_task = get_most_preferred(tasks_df)
    print(
        f"Sorting complete. YOUR NEXT TASK IS:\n{highest_priority_task.task_desc}"
    )
    input(f"Press 'Enter' to continue prioritizing...")


def shuffle_df(df: pd.DataFrame):
    """Shuffles the rows of a specified DataFrame."""
    return df.sample(frac=1).reset_index(drop=True)


def load_tasks_from_file(path_to_file: Path) -> pd.DataFrame:
    """Loads tasks from file into a new pandas DataFrame.

    Args:
        path_to_file (Path): The path of the the plain text file containing a list of tasks to prioritize, each on a new line.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the list of tasks to prioritize.
    """
    todo_file = open(path_to_file.as_posix())
    atexit.register(at_exit, todo_file)

    tasks = [line.strip() for line in todo_file.readlines()]
    tasks_df = pd.DataFrame(
        {"task_desc": tasks, "pref_count": 0, "priority": None}
    )
    tasks_df.insert(0, "id", tasks_df.index)
    return tasks_df


def prioritize_tasks(tasks_df):
    tasks_df.at[0, "pref_count"] = 1
    preferred_task = tasks_df.at[0, "task_desc"]
    for i in range(2, len(tasks_df)):  # Skip first task
        
        print(f"({i}/{len(tasks_df.index)})", end=" ")
        task = tasks_df.at[i, "task_desc"]
        if is_preferred(task, preferred_task):
            tasks_df.at[i, "pref_count"] += 1
            preferred_task_index = i
            preferred_task = tasks_df.at[preferred_task_index, "task_desc"]
        erase_prev_lines(6)
    return tasks_df


if __name__ == "__main__":
    main()
