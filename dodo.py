from pathlib import Path # To wrap around filepaths
from doit.tools import run_once

#task_dep exits too

# --- Set a custom title for all doit tasks ---

def show_cmd(task):
    return "executing... %s" % task.name

def task_clear_data_output():
    action_path = Path("src/utility_scripts/clear_data_output.py")
    return {
        "actions": ["python {}".format(action_path)],
        "uptodate": [run_once],
        "title": show_cmd,
    }

def task_clear_viz_output():
    action_path = Path("src/utility_scripts/clear_viz_output.py")
    return {
        "actions": ["python {}".format(action_path)],
        "uptodate": [run_once],
        "title": show_cmd,
    }

def task_run_book_data_external_data_quality_tests():
    action_path = Path("tests/data_quality_tests/test_book_data_external_data_quality.py")
    return {
        "file_dep": [Path("data/external/book_data_external.xlsx")],
        "actions": ["pytest {}".format(action_path)],
        "title": show_cmd
    }


def task_scrape_goodreads_reviews():
    action_path = Path("src/data_processing/scrape_goodreads_reviews.py")
    return {
        "file_dep": [Path("data/external/book_data_external.xlsx")],
        "task_dep": ["run_book_data_external_data_quality_tests"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/raw/goodreads_reviews_raw.csv")],
        "title": show_cmd,
    }

def task_clean_goodreads_reviews_raw():
    action_path = Path("src/data_cleaning/clean_goodreads_reviews_raw.py")
    return {
        "file_dep": [Path("data/raw/goodreads_reviews_raw.csv")],
        "task_dep": ["scrape_goodreads_reviews"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/cleaned/goodreads_reviews_cleaned.csv")],
        "title": show_cmd,

    }

def task_run_goodreads_reviews_cleaned_data_quality_tests():
    action_path = Path("tests/data_quality_tests/test_goodreads_reviews_cleaned_data_quality.py")
    return {
        "file_dep": [Path("data/cleaned/goodreads_reviews_cleaned.csv")],
        "task_dep": ["clean_goodreads_reviews"],
        "actions": ["pytest {}".format(action_path)],
        "title": show_cmd
    }