import pandas as pd
import wordfreq
import numpy
from functools import reduce
from file_manager import FileManager  

class Analyser:

    @staticmethod
    def normalise_data(filename="count-words.json"):
        words = FileManager.load_json(filename)
        count = words["total"]
        words_df = pd.Series(words["list"]).to_frame("count")
        words_df = words_df.sort_values(by='count',ascending=False)
        words_df['count'] /= count
        words_df['count'] = numpy.log10(words_df['count']) + 9 
        return words_df

    @staticmethod
    def prepare_lang_n_df(num, language):
        all_words = wordfreq.top_n_list(language, num)
        zipf_values = [wordfreq.zipf_frequency(w, language) for w in all_words]
        lang_df = pd.DataFrame(data={"Language Frequency": zipf_values}, index=pd.Index(all_words, name='word'))
        return lang_df
        
    @staticmethod
    def getChartDf(article_data, num=24, mode='article', lang='en'):

        article_data.columns = ['Article Frequency']
        if mode == 'article':
            article_data = article_data.head(num) 
            words = article_data.index
            english_wordfreq = [wordfreq.zipf_frequency(word, lang) for word in words]
            english_df = pd.DataFrame(data={'Language Frequency': english_wordfreq}, index=words)
            combined_df = article_data.join(english_df, how='left')
            combined_df = combined_df.fillna(0)
            combined_df = combined_df.sort_values(by='Article Frequency', ascending=True)
        elif mode == 'language':
            english_df = Analyser.prepare_lang_n_df(num, lang)
            combined_df = english_df.join(article_data, how='left')
            combined_df = combined_df.fillna(0)
            combined_df = combined_df.sort_values(by='Language Frequency', ascending=True)
        else:
            raise Exception("Invalid mode argument - must be either 'article' or 'language'")
        
        return combined_df

FOLDER = "json"
LANGS = ["en","de"]
K_VALS = [3, 10, 100, 1000, 10000]

class LanguageAnalyzer:

    @staticmethod
    def perform_tests():

        result = []
        for lang in LANGS:
            resultslang = []
            for filepath in FileManager.get_all_filepaths(FOLDER):
                for k in K_VALS:
                    lwwf = Analyser.prepare_lang_n_df(k, lang)
                    resultslang.append({"k": k,
                                    f"{lang} score": LanguageAnalyzer.lang_confidence_score(filepath, lwwf),
                                    "file": FileManager.get_article_name(filepath)})
            result.append(resultslang)

        
        dfs = [pd.DataFrame(inner_list) for inner_list in result]
        df_final = reduce(lambda left, right: pd.merge(left, right, on=['k','file'], how='outer'), dfs)
        print(df_final.to_string())
        return df_final
        

    # Assume that word_counts is just a loaded count-words.json with word counts and a "totals" field 
    @staticmethod
    def lang_confidence_score(word_counts, language_words_with_frequency):
        words_df = Analyser.normalise_data(word_counts)
        words_df.columns = ["Data Frequency"]
        combined_df = words_df.join(language_words_with_frequency, how='left')

        # RMS calculation
        score = combined_df["Data Frequency"].sub(language_words_with_frequency["Language Frequency"], fill_value=0)
        score = score ** 2
        total_score = numpy.sum(score)/len(score)
        return total_score

