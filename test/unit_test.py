"""Contains all unit tests. Requires full html of the Randall Munroe 
arcticle version from 17.02.2026 from explainxkcd
to be present in test folder, where the file structre should be:
WikiScraper/whatever/file_manager.py, WikiScraper/test/*Randall*"""""
from wikiscraper import file_manager
from wikiscraper import scraper

TEST_FOLDER = "test"

def test_get_paragraph():
    """Tests getting the first paragraph of an article form an html"""
    filepath = file_manager.get_target_dir(TEST_FOLDER) / "Randall_Munroe.html"
    data = scraper.get_paragraph(filepath)
    assert data is not None
    data_words = data.text.split(" ")
    assert data_words[0] == "Randall"
    assert data_words[1] == "Munroe"
    assert data_words[-2] == "and"
    print("SCRAPER::GET_PARAGRAPH UNIT TEST PASSED...")

def test_get_alpha_wordlist():
    """Tests getting all alpha words from an html"""
    filepath = file_manager.get_target_dir(TEST_FOLDER) / "Randall_Munroe.html"
    data = scraper.get_article_alpha_wordlist(filepath)
    assert data is not None
    assert data[0] == "Randall"
    assert data[1] == "Munroe"
    assert data[-1] == "Randall"
    print("SCRAPER::GET_ALPHA_WORDLIST UNIT TEST PASSED...")

def test_get_wikilinks():
    """Tests extracting inner wikilinks from an html"""
    filepath = file_manager.get_target_dir(TEST_FOLDER) / "Randall_Munroe.html"
    data = scraper.get_wikilinks(filepath)
    assert data is not None
    assert data[0] == 'https://www.explainxkcd.com/wiki/index.php/xkcd'
    assert data[-1] == 'https://www.explainxkcd.com/wiki/index.php/explain_xkcd:General_disclaimer'
    print("SCRAPER::GET_WIKILINKS UNIT TEST PASSED...")

def test_get_all_filepaths():
    """Tests the file manager's 'get_all_filepaths', which should returns all 
    possible filepaths to files inside a folder"""
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
