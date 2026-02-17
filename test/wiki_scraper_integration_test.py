from wikiscraper import analyzer
from wikiscraper import file_manager
from wikiscraper import chart_engine
from wikiscraper import scraper
from wikiscraper import language_analysis
from wikiscraper import wiki_scraper

# Integration test for the analyzer
def integration_test_analyser():
    article = "Randall_Munroe"
    wiki_scraper.count({"article": article}, mode='w')
    mode='article'
    article += ".json"
    num=39
    combined_df = analyzer.get_chart_df(analyzer.calculate_zipf_values(article),num, mode)
    combined_df = combined_df.nlargest(3, ['Article Frequency'])
    
    assert combined_df.index[-1] == "Randall"
    assert combined_df.index[0] == "the"
    assert combined_df.index[1] == "of"


""""""
TEST_FOLDER = "test"

def unit_test_get_paragraph():
    filepath = file_manager.get_target_dir(TEST_FOLDER) / "Randall_Munroe.html"
    data = scraper.get_paragraph(filepath)
    assert data is not None 
    data_words = data.text.split(" ")
    assert data_words[0] == "Randall"
    assert data_words[1] == "Munroe"
    assert data_words[-2] == "and"
    print("SCRAPER::GET_PARAGRAPH UNIT TEST PASSED...")

def unit_test_get_alpha_wordlist():
    filepath = file_manager.get_target_dir(TEST_FOLDER) / "Randall_Munroe.html"
    data = scraper.get_article_alpha_wordlist(filepath)
    assert data != None 
    assert data[0] == "Randall"
    assert data[1] == "Munroe"
    assert data[-1] == "Randall"
    print("SCRAPER::GET_ALPHA_WORDLIST UNIT TEST PASSED...")

def unit_test_get_wikilinks():
    filepath = file_manager.get_target_dir(TEST_FOLDER) / "Randall_Munroe.html"
    data = scraper.get_wikilinks(filepath)
    assert data != None 
    assert data[0] == 'https://www.explainxkcd.com/wiki/index.php/xkcd' 
    assert data[-1] == 'https://www.explainxkcd.com/wiki/index.php/explain_xkcd:General_disclaimer'
    
    print("SCRAPER::GET_WIKILINKS UNIT TEST PASSED...")

def unit_test_get_all_filepaths():
    file_manager.save_json("bigie", {}, TEST_FOLDER, ".par")
    file_manager.save_json("smalie", {}, TEST_FOLDER, ".par")
    file_manager.save_json("funie", {}, TEST_FOLDER, ".par")

    filepaths = file_manager.get_all_filepaths(TEST_FOLDER)
    names = [file_manager.get_article_name(f) for f in filepaths]
    assert "bigie" in names 
    assert "smalie" in names 
    assert "funie" in names
    assert "portal" not in names

    file_manager.remove_file(file_manager.get_target_dir(TEST_FOLDER) / "bigie.par")
    file_manager.remove_file(file_manager.get_target_dir(TEST_FOLDER) / "funie.par")
    file_manager.remove_file(file_manager.get_target_dir(TEST_FOLDER) / "smalie.par")
    
    print("FILEMANAGER::GET_ALL_FILEPATHS UNIT TEST PASSED...")


unit_test_get_paragraph()
unit_test_get_wikilinks()
unit_test_get_alpha_wordlist()
unit_test_get_all_filepaths()
integration_test_analyser()
