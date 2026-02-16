"""Contains the bulk of the methods that perform the analysis"""
import wordfreq
import pandas as pd
import numpy
import file_manager

def calculate_zipf_values(filename="count-words.json"):
    """Loads a json dictionary with two fields: "total": and "list": 
    Total contains sum of all counts (a single value) and list contains
    A list of word-value pairs with each word having its own count assigned
    the word list with the number of times each word occured in the text
    The function then turns this into a data frame with zipf frequency assigned"""

    words = file_manager.load_json(filename)
    count = words["total"]
    words_df = pd.Series(words["list"]).to_frame("count")
    words_df = words_df.sort_values(by="count",ascending=False)
    words_df["count"] /= count
    words_df["count"] = numpy.log10(words_df["count"]) + 9
    words_df.columns = ["Article Frequency"]
    return words_df

def calculate_probablity_values(filename="count-words.json"):
    """The same as above but probability values"""
    words = file_manager.load_json(filename)
    count = words["total"]
    words_df = pd.Series(words["list"]).to_frame("count")
    words_df = words_df.sort_values(by="count",ascending=False)
    words_df["count"] /= count
    words_df.columns = ["Article Frequency"]
    return words_df

def top_n_words_zipf(n, language):
    """ Returns a data frame with top n words from a specified 
    language and their calculated zipf values """
    all_words = wordfreq.top_n_list(language, n)
    zipf_values = \
            [wordfreq.zipf_frequency(w, language) for w in all_words]

    lang_df = pd.DataFrame(data={"Language Frequency": zipf_values},
                           index=pd.Index(all_words, name="word"))
    return lang_df

def top_n_words_probability(n, language):
    """The same as above but with probability"""
    all_words = wordfreq.top_n_list(language, n)
    probability_values = [wordfreq.word_frequency(w, language) for w in all_words]
    lang_df = pd.DataFrame(data={"Language Frequency": probability_values},
                           index=pd.Index(all_words, name="word"))
    return lang_df

def get_chart_df(article_data, num=24, mode="article", lang="en"):
    """Returns the data frame of frequencies necessary for drawing the requested chart"""
    article_data.columns = ["Article Frequency"]
    if mode == "article":
        article_data = article_data.head(num)
        words = article_data.index
        english_wordfreq = [wordfreq.zipf_frequency(word, lang) for word in words]
        english_df = pd.DataFrame(data={"Language Frequency": english_wordfreq}, index=words)
        combined_df = article_data.join(english_df, how="left")
        combined_df = combined_df.fillna(0)
        combined_df = combined_df.sort_values(by="Article Frequency", ascending=True)
    elif mode == "language":
        english_df = top_n_words_zipf(num, lang)
        combined_df = english_df.join(article_data, how="left")
        combined_df = combined_df.fillna(0)
        combined_df = combined_df.sort_values(by="Language Frequency", ascending=True)
    else:
        raise Exception("Invalid mode argument - must be either 'article' or 'language'")

    return combined_df
