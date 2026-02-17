"""This module performs and presents the language analysis part of the solution"""
from functools import reduce
import pandas as pd
import numpy
from wikiscraper import file_manager
from wikiscraper import wiki_scraper
from wikiscraper import analyzer
from wikiscraper import chart_engine

def perform_tests(folder, langs, k_vals):
    """Performs the entire analysis and stiches it into one comprehensive table"""
    result = []
    for lang in langs:
        resultslang = []
        for filepath in file_manager.get_all_filepaths(folder):
            for k in k_vals:
                lwwf = analyzer.top_n_words_probability(k, lang)
                resultslang.append({"k": k,
                                f"{lang} score": lang_confidence_score(filepath, lwwf),
                                "file": file_manager.get_article_name(filepath)})
        result.append(resultslang)

    """This masterful contraption takes all the data frames with data for k,
     score and a certain language and then joins all of them to have
     data for each artcile in each language in a single column """
    dfs = [pd.DataFrame(inner_list) for inner_list in result]
    df_final = reduce(lambda left, right: pd.merge(left, right, on=["k","file"], how="outer"), dfs)
    print(df_final.to_string())
    return df_final

# Assume that word_counts is just a loaded count-words.json with word counts and a "totals" field
def lang_confidence_score(word_counts, language_words_with_frequency):
    """Calculates the final lang confidence score"""
    words_df = analyzer.calculate_probablity_values(word_counts)
    words_df.columns = ["Data Frequency"]
    combined_df = words_df.join(language_words_with_frequency, how="right")
    combined_df["Data Frequency"] = combined_df["Data Frequency"].fillna(1e-10)
    combined_df["Language Frequency"] = (combined_df["Language Frequency"] /
                                         combined_df["Language Frequency"].sum())
    # KL Divergence Calculation
    score = numpy.sum(combined_df["Language Frequency"] * numpy.log(
                combined_df["Language Frequency"] /
                combined_df["Data Frequency"]))
    return score


""" DATA USED FOR REFERENCE """ 

LITERATURE = ["Also Sprach Zaratustra", "Uncle Tom's Cabin", "Les Miserables"]

ENGLISH_ARTICLES = ["wiki_scraper_Page", "Randall_Munroe", 
                    "3171:_Geologic_Core_Sample", "3109:_Dehumidifier", "Cueball"]
ENGLISH_SUBFREFIX = "https://www.explainxkcd.com"
ENGLIHS_LOCAL_PREFIX = "/wiki/index.php/"  

GERMAN_ARTICLES = ["PokéWiki:Auskunft", "PokéWiki:Mitmachen","Hauptseite",
                   "PokéWiki:Redakteure#Wiederherstellen","Donarion"]
GERMAN_SUBPREFIX = "https://www.pokewiki.de"
GERMAN_LOCAL_PREFIX = "/"

FRENCH_ARTICLES = ["Portail:Accueil", "Pokémon,_la_série", "Pokémon_Picross", "Gibeon", "Lucius"]
FRENCH_SUBPREFIX = "https://www.pokepedia.fr"
FRENCH_LOCAL_PREFIX = "/"

COMB_ARTICLES = {"en": ENGLISH_ARTICLES,"de": GERMAN_ARTICLES,"fr": FRENCH_ARTICLES}
COMB_SUBPREFIX = {"en": ENGLISH_SUBFREFIX,"de": GERMAN_SUBPREFIX,"fr": FRENCH_SUBPREFIX} 
COMB_LOCAL_PREFIX = {"en": ENGLIHS_LOCAL_PREFIX,"de": GERMAN_LOCAL_PREFIX,"fr": FRENCH_LOCAL_PREFIX}

FOLDER = "json"
LANGS = ["en", "de", "fr"]

"""-- This script below allows you to download the mentioned articles -- 
-- Wikiprefix is SUBPREFIX + LOCAL_WIKI_PREFIX """

def test_word_counting(article_names, wikiprefix, target_dir):
    for article in article_names:
        args = {"article": article}
        wiki_scraper.count(args, 'w', wikiprefix=wikiprefix, target_dir=target_dir)

def download_articles_and_count():
    for lang in LANGS:
        test_word_counting(COMB_ARTICLES[lang], COMB_SUBPREFIX[lang] 
                           + COMB_LOCAL_PREFIX[lang], FOLDER + "/" + str(lang))

"""And this below looks into the txt folder and processes 
the pure txt input into proper format of dictionary"""

def prepare_test_articles(folder="txt"):
    """Counts words in example artciles from txt folder and saves to json files in json/art folder"""
    files = file_manager.get_all_filepaths(folder)
    for file in files:
        filename = file_manager.get_file_name(file)
        list_of_words = file_manager.load_txt(filename)
        dict_result = wiki_scraper.count_helper( list_of_words)
        file_manager.save_json(filename.split(".")[0],dict_result, directory="json/art")

"""FINAL RUN ANALYSIS CODE WHEN ALL ARTICLES AND 
LITERATURE ARE IN JSON DICT FORMAT IN PROPER FOLDERS"""
"""The folders with materials from respective languages 
should be of the form json/fr or json/en etc"""

K_VALS = [3, 10, 100, 1000, 10000]

if __name__ == "__main__":
    
    # Run this if articles not yet in proper folder
    download_articles_and_count()  

    # Run this if txt downloaded from the net but not yet turned into json
    prepare_test_articles() 

    for lang in LANGS:
        lang_folder = FOLDER + "/" + str(lang)
        chart_engine.draw_language_test_bar_chart(
                perform_tests(folder=lang_folder, langs=LANGS, k_vals=K_VALS), lang_folder)
    art_folder = FOLDER + "/art"
    chart_engine.draw_language_test_bar_chart(perform_tests(folder=art_folder, langs=LANGS, k_vals=K_VALS), art_folder)
