from analyser import Analyser
import pandas as pd 
import numpy 
from functools import reduce
from wiki_scraper import Main
from file_manager import FileManager

FOLDER = "json"
LANGS = ["en", "de", "fr"]
K_VALS = [3, 10, 100, 1000, 10000]

class LanguageAnalyzer:
    
    @staticmethod
    def prepare_test_articles(folder="txt"):
        files = FileManager.get_all_filepaths(folder)
        for file in files:
            filename = FileManager.get_file_name(file)
            count_words = {"total": 0, "list": {}}
            list_of_words = FileManager.load_txt(filename) 
            dict_result = Main.count_helper(count_words, list_of_words)
            FileManager.save_json(filename.split(".")[0],dict_result)

        
    @staticmethod
    def perform_tests(folder=FOLDER, langs=LANGS, k_vals=K_VALS):

        result = []
        for lang in langs:
            resultslang = []
            for filepath in FileManager.get_all_filepaths(folder):
                for k in k_vals:
                    lwwf = Analyser.top_n_words_probability(k, lang)
                    resultslang.append({"k": k,
                                    f"{lang} score": LanguageAnalyzer.lang_confidence_score(filepath, lwwf),
                                    "file": FileManager.get_article_name(filepath)})
            result.append(resultslang)

        # This masterful contraption takes all the data frames with data for k, score and a certain language and then joins all of them to have 
        # data for each artcile in each language in a single column 
        dfs = [pd.DataFrame(inner_list) for inner_list in result]
        df_final = reduce(lambda left, right: pd.merge(left, right, on=['k','file'], how='outer'), dfs)
        print(df_final.to_string())
        return df_final
        

    # Assume that word_counts is just a loaded count-words.json with word counts and a "totals" field 
    @staticmethod
    def lang_confidence_score(word_counts, language_words_with_frequency):
        words_df = Analyser.calculate_probablity_values(word_counts)
        words_df.columns = ["Data Frequency"]
        combined_df = words_df.join(language_words_with_frequency, how='right')
        combined_df["Data Frequency"] = combined_df["Data Frequency"].fillna(1e-10)
        combined_df["Data Frequency"] = combined_df["Data Frequency"] / combined_df["Data Frequency"].sum()
        combined_df["Language Frequency"] = combined_df["Language Frequency"] / combined_df["Language Frequency"].sum()
        
        # KL Divergence Calculation
        score = numpy.sum(combined_df["Language Frequency"] * numpy.log(
                    combined_df["Language Frequency"]/  
                    combined_df["Data Frequency"]))

        return score

