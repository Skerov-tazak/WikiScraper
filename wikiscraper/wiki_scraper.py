import time
from io import StringIO
from collections import deque
import pandas
from wikiscraper import scraper
from wikiscraper import analyzer
from wikiscraper import chart_engine
from wikiscraper import args_parser
from wikiscraper import file_manager

def summary(args):
    """ Performs --summary functionality """
    article = args["article"]

    filepath = scraper.get_article(article)
    paragraph = scraper.get_paragraph(filepath)
    if paragraph:
        print(paragraph.text)
    file_manager.remove_file(filepath)

def table(args):
    """ Performs --table functionality """
    article = args["article"]
    num = args["num"]
    isheader = args["header"]

    html_filepath = scraper.get_article(article)
    table_text = scraper.get_table(html_filepath, num)
    file_manager.remove_file(html_filepath)
    data_frame = pandas.read_html(StringIO(table_text.prettify()), flavor="bs4")[0]

    word_list = data_frame.stack().tolist()
    word_counter = count_helper( word_list)
    print(pandas.Series(word_counter["list"]).to_frame())
    file_manager.save_csv(article, data_frame, isheader)

def count_helper(word_list, word_counter = None): 
    """ Counts all words from a word list and saves to a dictionary """
    if word_counter is None:
        word_counter = {"total": 0, "list": {}}

    for word in word_list:
        word_counter["total"] += 1
        if word in word_counter["list"]:
            word_counter["list"][word] += 1
        else:
            word_counter["list"].update({word: 1})
    return word_counter

def count(args, mode='a', wikiprefix=scraper.DEFAULT_SUBPREFIX + scraper.LOCAL_WIKI_PREFIX, target_dir="json"):
    """ Performs --count-words functionality """
    if mode not in ('w', 'a'):
        raise Exception("Count must work in either write or append mode!")
    article = args["article"]

    filepath = scraper.get_article(article, wikiprefix=wikiprefix)
    word_list = scraper.get_article_alpha_wordlist(filepath)

    word_counter = count_helper(word_list)

    if mode == "w":
        file_manager.save_json(article, word_counter, directory=target_dir)
    else:
        file_manager.save_json("count_words", word_counter, mode='a', directory=target_dir)

def crawl(args, mode='a', subprefix=scraper.DEFAULT_SUBPREFIX,
          localprefix=scraper.LOCAL_WIKI_PREFIX):
    """ Performs --auto-count-words functionality """
    wikiprefix = subprefix + localprefix
    depth = args["depth"]
    article_ori = args["article"]
    wait = args["wait"]

    word_counter = {"total": 0, "list": {}}
    bfs = deque()
    visited = {}
    n = 0
    num_articles = 0
    bfs.appendleft([article_ori, n])

    while len(bfs) > 0:
        num_articles += 1
        current = bfs.pop()
        n = current[1]
        if current[0] in visited:
            continue
        if n > depth:
            break
        print(current)
        article_name = current[0]
        cur_filepath = scraper.get_article(article_name, wikiprefix=wikiprefix)
        candidates = scraper.get_linked_articles(cur_filepath, subprefix=subprefix,
                                                 localprefix=localprefix)

        for article in candidates:
            bfs.appendleft([article, n + 1])
        word_list = scraper.get_article_alpha_wordlist(cur_filepath)
        word_counter = count_helper( word_list, word_counter=word_counter)
        time.sleep(wait)
        visited.update({current[0]: True})
        file_manager.remove_file(cur_filepath)

    if mode == "w":
        file_manager.save_json("Word_freq_" + article_ori + "_depth_" +
                              str(depth) + "_articles_" + str(num_articles), word_counter)
    else:
        file_manager.save_json("count_words", word_counter, mode='a')

def analyse(args):
    """ Performs --Analyze-relative-word-frequency functionality """
    mode = args["mode"]
    cnt = args["count"]
    chartfilepath = args["chart"]
    combined_df = analyzer.get_chart_df(analyzer.calculate_zipf_values("count_words.json"),
                                      cnt, mode)
    print(combined_df.to_string())
    chart_engine.draw_freq_bar_chart(combined_df, count, mode, chartfilepath=chartfilepath)

# Dictionary for functions
execute_dict = {
        "summary": summary,
        "crawl": crawl,
        "table": table,
        "count": count,
        "analyse": analyse
        }

# Code that passes arguments from the parser and chooses the correct functions to run
if __name__ == '__main__':
    features = args_parser.return_features()
    for key, options in features.items():
        if options["set"] is True:
            execute_dict[key](options)
