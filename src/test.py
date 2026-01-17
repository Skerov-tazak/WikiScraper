from analyser import Analyser, LanguageAnalyzer
from wiki_scraper import Main
from chart_engine import ChartDrawer

ARTICLE_NAMES = ["Main_Page", "Randall_Munroe"]
GERMAN_PREFIX = "https://www.pokewiki.de/"
GERMAN_SUBPREFIX = "https://www.pokewiki.de"
GERMAN_LOCAL_PREFIX = "/"
GERMAN_ARTICLES = ["Hauptseite"]

def test_analyser():
    article = "Word_freq_Main_Page_depth_1_articles_62.json"
    mode='article'
    num=39
    combined_df = Analyser.getChartDf(Analyser.normalise_data(article),num, mode)
    print(combined_df.to_string())
    ChartDrawer.drawFreqBarChart(combined_df, num, mode)

def test_lang_analyser():
    ChartDrawer.drawLanguageTestBarChart(LanguageAnalyzer.perform_tests())

def test_word_counting():
    for article in ARTICLE_NAMES:
        args = {"article": article}
        Main.count(args, 'w')

def test_german_word_counting():
    for article in GERMAN_ARTICLES:
        args = {"article": article}
        Main.count(args, 'w', wikiprefix=GERMAN_PREFIX)

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


test_lang_analyser()
