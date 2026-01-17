from file_manager import FileManager
from scraper import Scraper
from analyser import Analyser 
from language_analysis import LanguageAnalyzer
from wiki_scraper import Main
from chart_engine import ChartDrawer

ARTICLE_NAMES = ["Main_Page", "Randall_Munroe", "3171:_Geologic_Core_Sample", "3109:_Dehumidifier", "Cueball"]

GERMAN_PREFIX = "https://www.pokewiki.de/"
GERMAN_SUBPREFIX = "https://www.pokewiki.de"
GERMAN_LOCAL_PREFIX = "/"
GERMAN_ARTICLES = ["PokéWiki:Auskunft", "PokéWiki:Mitmachen","Hauptseite","PokéWiki:Redakteure#Wiederherstellen","Donarion"]

FRENCH_PREFIX = "https://www.pokepedia.fr/"
FRENCH_ARTICLES = ["Portail:Accueil", "Pokémon,_la_série", "Pokémon_Picross", "Gibeon", "Lucius"]
FRENCH_SUBPREFIX = "https://www.pokepedia.fr"
FRENCH_LOCAL_PREFIX = "/"

def test_analyser():
    article = "Randall_Munroe.json"
    mode='article'
    num=39
    combined_df = Analyser.getChartDf(Analyser.calculate_zipf_values(article),num, mode)
    print(combined_df.to_string())
    ChartDrawer.drawFreqBarChart(combined_df, num, mode)

def test_lang_analyser():
    ChartDrawer.drawLanguageTestBarChart(LanguageAnalyzer.perform_tests(folder="json/fr"), "json/fr")

def test_word_counting():
    for article in ARTICLE_NAMES:
        args = {"article": article}
        Main.count(args, 'w')

def test_german_word_counting():
    for article in GERMAN_ARTICLES:
        args = {"article": article}
        Main.count(args, 'w', wikiprefix=GERMAN_PREFIX)

def test_french_word_counting():
    for article in FRENCH_ARTICLES:
        args = {"article": article}
        Main.count(args, 'w', wikiprefix=FRENCH_PREFIX)

def test_auto_german_word_counting():
    args = {"depth": 1, "wait": 0.05}
    for article in GERMAN_ARTICLES:
        args.update({"article": article})
        Main.crawl(args, 'w', wikiprefix=GERMAN_PREFIX, localprefix=GERMAN_LOCAL_PREFIX, subprefix=GERMAN_PREFIX)

def test_auto_word_counting():
    args = {"depth": 1, "wait": 0.05}
    for article in ARTICLE_NAMES:
        args.update({"article": article})
        Main.crawl(args, 'w')

def test_count_words_file():
    for article in ARTICLE_NAMES:
        args = {"article": article} 
        Main.count(args, 'a')

TEST_FOLDER = "test"
Scraper.get_article("Randall_Munroe", dir=TEST_FOLDER)

def unit_test_get_paragraph():
    filepath = FileManager.get_target_dir(TEST_FOLDER) / "Randall_Munroe.html"
    data = Scraper.get_paragraph(filepath)
    assert data != None 
    data_words = data.text.split(" ")
    assert data_words[0] == "Randall"
    assert data_words[1] == "Munroe"
    assert data_words[-2] == "and"
    print("SCRAPER::GET_PARAGRAPH UNIT TEST PASSED...")

def unit_test_get_alpha_wordlist():
    filepath = FileManager.get_target_dir(TEST_FOLDER) / "Randall_Munroe.html"
    data = Scraper.get_article_alpha_wordlist(filepath)
    assert data != None 
    assert data[0] == "Randall"
    assert data[1] == "Munroe"
    assert data[-1] == "Randall"
    print("SCRAPER::GET_ALPHA_WORDLIST UNIT TEST PASSED...")

def unit_test_get_wikilinks():
    filepath = FileManager.get_target_dir(TEST_FOLDER) / "Randall_Munroe.html"
    data = Scraper.get_wikilinks(filepath)
    assert data != None 
    assert data[0] == 'https://www.explainxkcd.com/wiki/index.php/xkcd' 
    assert data[-1] == 'https://www.explainxkcd.com/wiki/index.php/explain_xkcd:General_disclaimer'
    
    print("SCRAPER::GET_WIKILINKS UNIT TEST PASSED...")

def unit_test_get_all_filepaths():
    FileManager.save_json("bigie", {}, TEST_FOLDER, ".par")
    FileManager.save_json("smalie", {}, TEST_FOLDER, ".par")
    FileManager.save_json("funie", {}, TEST_FOLDER, ".par")

    filepaths = FileManager.get_all_filepaths(TEST_FOLDER)
    names = [FileManager.get_article_name(f) for f in filepaths]
    assert "bigie" in names 
    assert "smalie" in names 
    assert "funie" in names
    assert "portal" not in names

    FileManager.remove_file(FileManager.get_target_dir(TEST_FOLDER) / "bigie.par")
    FileManager.remove_file(FileManager.get_target_dir(TEST_FOLDER) / "funie.par")
    FileManager.remove_file(FileManager.get_target_dir(TEST_FOLDER) / "smalie.par")
    
    print("FILEMANAGER::GET_ALL_FILEPATHS UNIT TEST PASSED...")


unit_test_get_paragraph()
unit_test_get_wikilinks()
unit_test_get_alpha_wordlist()
unit_test_get_all_filepaths()
