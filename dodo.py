from pathlib import Path # To wrap around filepaths
from doit.tools import run_once

#task_dep exits too

# --- Set a custom title for all doit tasks ---

def show_cmd(task):
    return "executing... %s" % task.name

def task_clear_data_output():
    action_path = Path("src/data_preparation/clear_data_output.py")
    return {
        "actions": ["python {}".format(action_path)],
        "uptodate": [run_once],
        "title": show_cmd,
    }

def task_clear_viz_output():
    action_path = Path("src/data_preparation/clear_viz_output.py")
    return {
        "actions": ["python {}".format(action_path)],
        "uptodate": [run_once],
        "title": show_cmd,
    }

def task_run_book_data_data_quality_tests():
    action_path = Path("src/tests/data_quality_tests/test_book_data_data_quality.py")
    return {
        "file_dep": [Path("data/external/book_data.xlsx")],
        "actions": ["python pytest {}".format(action_path)],
        "title": show_cmd
    }


def task_scrape_goodreads_reviews():
    action_path = Path("src/data_preparation/scrape_goodreads_reviews.py")
    return {
        "file_dep": [Path("data/external/book_data.xlsx")],
        "task_dep": ["run_book_data_data_quality_tests"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/raw/reviews_raw.csv")],
        "title": show_cmd,
    }