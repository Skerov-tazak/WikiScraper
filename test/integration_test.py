"""Performs the intergartion test between the analyzer and the parts of 
the scraper that parse data and count words. Requires full html of the 
Randall Munore arcticle version from 17.02.2026 in test folder, with 
file structure as follows: WikiScraper/whatever/file_manager.py, 
WikiScraper/test/*Randall*"""""

from wikiscraper import analyzer
from wikiscraper import scraper
from wikiscraper import wiki_scraper
from wikiscraper import file_manager

TEST_FOLDER = "test"

def test_integration_analyser_with_html_parsing():
    """Integration Test"""
    article = "Randall_Munroe"
    filepath = file_manager.get_target_dir(TEST_FOLDER) / str(article + ".html")

    word_list = scraper.get_article_alpha_wordlist(filepath)

    word_counter = wiki_scraper.count_helper(word_list)

    handle = file_manager.save_json(article, word_counter)
    mode='article'
    article += ".json"
    num=39
    combined_df = analyzer.get_chart_df(analyzer.calculate_zipf_values(article),num, mode)
    combined_df = combined_df.nlargest(3, ['Article Frequency'])
    print(combined_df)

    file_manager.remove_file(handle)
    assert combined_df.index[1] == "Randall"
    assert combined_df.index[0] == "the"
    assert combined_df.index[-1] == "of"
