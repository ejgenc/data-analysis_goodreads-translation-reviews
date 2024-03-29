from pathlib import Path
from doit.tools import run_once

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

# --- !!! ATTENTION !!! ---
# This part of the dodo.py file is commented out by default. The code below triggers
# the scripts that are responsible for the web scraping of the reviews investigated by this analysis.
# Since the analysis file is shared for replication purposes, the intended behavior of the script
# is to re-run the analysis on the dataset as presented by the paper that accompanies this analysis.
# The dataset may be subject to change every time it is scraped. Thus, replicating the scraping part
# is made optional. If the user wants to replicate the scraping part too or target the analysis to a new set
# of Goodreads reviews, s/he should look at the README for a how-to guide.


# def task_run_book_data_external_data_quality_tests():
#     action_path = Path("tests/data_quality_tests/test_book_data_external_data_quality.py")
#     return {
#         "file_dep": [Path("data/external/book_data_external.xlsx")],
#         "actions": ["pytest {}".format(action_path)],
#         "title": show_cmd
#     }

# def task_scrape_goodreads_reviews():
#     action_path = Path("src/data_processing/scrape_goodreads_reviews.py")
#     return {
#         "file_dep": [Path("data/external/book_data_external.xlsx")],
#         "task_dep": ["run_book_data_external_data_quality_tests"],
#         "actions": ["python {}".format(action_path)],
#         "targets": [Path("data/raw/goodreads_reviews_raw.csv")],
#         "title": show_cmd,
#     }

# def task_clean_goodreads_reviews_raw():
#     action_path = Path("src/data_cleaning/clean_goodreads_reviews_raw.py")
#     return {
#         "file_dep": [Path("data/raw/goodreads_reviews_raw.csv")],
#         #"task_dep": ["scrape_goodreads_reviews"],
#         "actions": ["python {}".format(action_path)],
#         "targets": [Path("data/cleaned/goodreads_reviews_cleaned.xlsx")],
#         "title": show_cmd,

#     }

# def task_run_goodreads_reviews_cleaned_data_quality_tests():
#     action_path = Path("tests/data_quality_tests/test_goodreads_reviews_cleaned_data_quality.py")
#     return {
#         "file_dep": [Path("data/cleaned/goodreads_reviews_cleaned.csv")],
#         "task_dep": ["clean_goodreads_reviews_raw"],
#         "actions": ["pytest {}".format(action_path)],
#         "title": show_cmd
#     }

# --- !!! ATTENTION !!! ---

def task_process_goodreads_reviews_cleaned():
    action_path = Path("src/data_processing/process_goodreads_reviews_cleaned.py")
    return {
        "file_dep": [Path("data/cleaned/goodreads_reviews_cleaned.csv")],
        # "task_dep": ["run_goodreads_reviews_cleaned_data_quality_tests"], # --- !!! ATTENTION: Uncomment this along with the snippets above. --- #
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/raw/review_sentences_raw.csv")],
        "title": show_cmd
    }

def task_clean_review_sentences_raw():
    action_path = Path("src/data_cleaning/clean_review_sentences_raw.py")
    return {
        "file_dep": [Path("data/raw/review_sentences_raw.csv")],
        "task_dep": ["process_goodreads_reviews_cleaned"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/cleaned/review_sentences_cleaned.csv")],
        "title": show_cmd
    }

def task_run_review_sentences_cleaned_data_quality_tests():
    action_path = Path("tests/data_quality_tests/test_review_sentences_cleaned_data_quality.py")
    return {
        "file_dep": [Path("data/cleaned/review_sentences_cleaned.csv")],
        "task_dep": ["clean_review_sentences_raw"],
        "actions": ["pytest {}".format(action_path)],
        "title": show_cmd
    }

def task_analyze_review_sentences_cleaned():
    action_path = Path("src/data_analysis/analyze_review_sentences_cleaned.py")
    return {
        "file_dep": [Path("data/cleaned/review_sentences_cleaned.csv")],
        "task_dep": ["run_review_sentences_cleaned_data_quality_tests"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/analysis_results/review_sentences_analyzed.csv")],
        "title": show_cmd
    }

def task_run_review_sentences_analyzed_data_quality_tests():
    action_path = Path("tests/data_quality_tests/test_review_sentences_analyzed_data_quality.py")
    return {
        "file_dep": [Path("data/analysis_results/review_sentences_analyzed.csv")],
        "task_dep": ["analyze_review_sentences_cleaned"],
        "actions": ["pytest {}".format(action_path)],
        "title": show_cmd
    }

def task_process_review_sentences_cleaned():
    action_path = Path("src/data_processing/process_review_sentences_cleaned.py")
    return {
        "file_dep": [Path("data/cleaned/review_sentences_cleaned.csv")],
        "task_dep": ["run_review_sentences_cleaned_data_quality_tests"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/raw/tokens_and_dependencies_raw.csv")],
        "title": show_cmd
    }

def task_clean_token_and_dependencies_raw():
    action_path = Path("src/data_cleaning/clean_tokens_and_dependencies_raw.py")
    return {
        "file_dep": [Path("data/raw/tokens_and_dependencies_raw.csv")],
        "task_dep": ["process_review_sentences_cleaned"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/cleaned/tokens_and_dependencies_cleaned.csv")],
        "title": show_cmd
    }

def task_run_tokens_and_dependencies_cleaned_data_quality_tests():
    action_path = Path("tests/data_quality_tests/test_tokens_and_dependencies_cleaned_data_quality.py")
    return {
        "file_dep": [Path("data/cleaned/tokens_and_dependencies_cleaned.csv")],
        "task_dep": ["clean_token_and_dependencies_raw"],
        "actions": ["pytest {}".format(action_path)],
        "title": show_cmd
    }

def task_process_tokens_and_dependencies_cleaned():
    action_path = Path("src/data_processing/process_tokens_and_dependencies_cleaned.py")
    return {
        "file_dep": [Path("data/cleaned/tokens_and_dependencies_cleaned.csv")],
        "task_dep": ["run_tokens_and_dependencies_cleaned_data_quality_tests"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/raw/modifiers_raw.csv")],
        "title": show_cmd
    }

def task_clean_modifiers_raw():
    action_path = Path("src/data_cleaning/clean_modifiers_raw.py")
    return {
        "file_dep": [Path("data/raw/modifiers_raw.csv")],
        "task_dep": ["process_tokens_and_dependencies_cleaned"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/cleaned/modifiers_cleaned.csv")],
        "title": show_cmd
    }

def task_run_modifiers_cleaned_data_quality_tests():
    action_path = Path("tests/data_quality_tests/test_modifiers_cleaned_data_quality.py")
    return {
        "file_dep": [Path("data/cleaned/modifiers_cleaned.csv")],
        "task_dep": ["clean_modifiers_raw"],
        "actions": ["pytest {}".format(action_path)],
        "title": show_cmd
    }

def task_analyze_modifiers_cleaned():
    action_path = Path("src/data_analysis/analyze_modifiers_cleaned.py")
    return {
        "file_dep": [Path("data/cleaned/modifiers_cleaned.csv")],
        "task_dep": ["run_modifiers_cleaned_data_quality_tests"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/analysis_results/total_modifiers_per_unique_modified.csv"),
                    Path("data/analysis_results/total_modifiers_per_modified_group.csv")],
        "title": show_cmd
    }

def task_analyze_goodreads_reviews_cleaned():
    action_path = Path("src/data_analysis/analyze_goodreads_reviews_cleaned.py")
    return {
        "file_dep": [Path("data/cleaned/goodreads_reviews_cleaned.csv"),
                    Path("data/analysis_results/review_sentences_analyzed.csv")], 
        "task_dep": ["run_review_sentences_analyzed_data_quality_tests"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/analysis_results/goodreads_reviews_analyzed.csv")],
        "title": show_cmd
    }

def task_run_goodreads_reviews_analyzed_data_quality_tests():
    action_path = Path("tests/data_quality_tests/test_goodreads_reviews_analyzed_data_quality.py")
    return {
        "file_dep": [Path("data/analysis_results/goodreads_reviews_analyzed.csv")],
        "task_dep": ["analyze_goodreads_reviews_cleaned"],
        "actions": ["pytest {}".format(action_path)],
        "title": show_cmd
    }

# --- !!! ATTENTION - Uncomment the code below if you wish to extend the analysis !!! ---
# def task_gather_book_level_statistics():
#     action_path = Path("src/data_analysis/gather_book_level_statistics.py")
#     return {
#         "file_dep": [Path("data/external/book_data_external.xlsx"),
#                     Path("data/raw/goodreads_reviews_raw.csv"),
#                     Path("data/cleaned/goodreads_reviews_cleaned.csv"),
#                     Path("data/analysis_results/goodreads_reviews_analyzed.csv")],
#         "task_dep": ["run_goodreads_reviews_analyzed_data_quality_tests"],
#         "actions": ["python {}".format(action_path)],
#         "targets": [Path("data/analysis_results/book_level_statistics.csv")],
#         "title": show_cmd
#     }

# def task_run_book_level_statistics_data_quality_tests():
#     action_path = Path("tests/data_quality_tests/test_book_level_statistics_data_quality.py")
#     return {
#         "file_dep": [Path("data/analysis_results/book_level_statistics.csv")],
#         "task_dep": ["gather_book_level_statistics"],
#         "actions": ["pytest {}".format(action_path)],
#         "title": show_cmd
#     }

def task_visualize_top_twenty_modifiers():
    action_path = Path("src/data_visualization/visualize_top_twenty_modifiers.py")
    return {
        "file_dep": [Path("data/analysis_results/total_modifiers_per_unique_modified.csv"),
                    Path("data/analysis_results/total_modifiers_per_modified_group.csv")],
        # "task_dep": ["run_book_level_statistics_data_quality_tests"], # --- !!! ATTENTION: Uncomment this along with the snippets above. --- #
        "actions": ["python {}".format(action_path)],
        "targets": [Path("media/figures/raw/visualize_top_twenty_modifiers")],
        "title": show_cmd
    }

def task_visualize_top_twenty_modifiers_valence_ratio():
    action_path = Path("src/data_visualization/visualize_top_twenty_modifiers_valence_ratio.py")
    return {
        "file_dep": [Path("data/analysis_results/total_modifiers_per_unique_modified.csv"),
                    Path("data/analysis_results/total_modifiers_per_modified_group.csv")],
        # "task_dep": ["run_book_level_statistics_data_quality_tests"], # --- !!! ATTENTION: Uncomment this along with the snippets above. --- #
        "actions": ["python {}".format(action_path)],
        "targets": [Path("media/figures/raw/visualize_top_twenty_modifiers_valence_ratio")],
        "title": show_cmd
    }

def task_visualize_bookcount_per_author():
    action_path = Path("src/data_visualization/visualize_bookcount_per_author.py")
    return {
        "file_dep": [Path("data/analysis_results/book_level_statistics.csv")],
        # "task_dep": ["run_book_level_statistics_data_quality_tests"], # --- !!! ATTENTION: Uncomment this along with the snippets above. --- #
        "actions": ["python {}".format(action_path)],
        "targets": [Path("media/figures/raw/visualize_bookcount_per_author")],
        "title": show_cmd
    }
    
def task_visualize_scraping_loss_per_book():
    action_path = Path("src/data_visualization/visualize_scraping_loss_per_book.py")
    return {
        "file_dep": [Path("data/analysis_results/book_level_statistics.csv")],
        # "task_dep": ["run_book_level_statistics_data_quality_tests"], # --- !!! ATTENTION: Uncomment this along with the snippets above. --- #
        "actions": ["python {}".format(action_path)],
        "targets": [Path("media/figures/raw/visualize_scraping_loss_per_book")],
        "title": show_cmd
    }

def task_visualize_review_length():
    action_path = Path("src/data_visualization/visualize_review_length.py")
    return {
        "file_dep": [Path("data/analysis_results/goodreads_reviews_analyzed.csv")],
        "task_dep": ["run_goodreads_reviews_analyzed_data_quality_tests"], 
        "actions": ["python {}".format(action_path)],
        "targets": [Path("media/figures/raw/visualize_review_length")],
        "title": show_cmd
    }