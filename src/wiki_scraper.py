from args_parser import Parser
from analyser import Analyser
import pandas
import time
from chart_engine import ChartDrawer
from scraper import DEFAULT_SUBPREFIX, DEFAULT_WIKI, LOCAL_WIKI_PREFIX, Scraper
from file_manager import FileManager
from collections import deque

class Main:

    # Performs --summary functionality
    @staticmethod
    def summary(args):
        article = args["article"]

        filepath = Scraper.get_article(article)
        paragraph = Scraper.get_paragraph(filepath)
        if paragraph:
            print(paragraph.text)
        FileManager.remove_file(filepath)

    # Performs --table functionality
    @staticmethod
    def table(args):
        article = args["article"]
        num = args["num"]
        isheader = args["header"]
        
        html_filepath = Scraper.get_article(article)
        table_text = Scraper.get_table(html_filepath, num)
        FileManager.remove_file(html_filepath)
        data_frame = pandas.read_html(table_text.prettify(), flavor="bs4")[0]
        word_counter = {"total": 0, "list": {}}
        word_list = data_frame.stack().tolist()
        word_counter = Main.count_helper(word_counter, word_list)
        print(pandas.Series(word_counter["list"]).to_frame())

        FileManager.save_csv(article, data_frame, isheader)

    # Counts all words from a word list and saves to a dictionary
    @staticmethod
    def count_helper(word_counter, word_list):
        for word in word_list:
            word_counter["total"] += 1
            if word in word_counter["list"]:
                word_counter["list"][word] += 1
            else:
                word_counter["list"].update({word: 1})
        return word_counter

    # Performs --count-words functionality
    @staticmethod
    def count(args, mode='a', wikiprefix=DEFAULT_WIKI):
        if mode != 'w' and mode != 'a':
            raise Exception("Count must work in either write or append mode!")
        article = args["article"]

        filepath = Scraper.get_article(article, wikiprefix=wikiprefix)
        word_list = Scraper.get_article_alpha_wordlist(filepath)
        word_counter = {"total": 0, "list": {}}
        word_counter = Main.count_helper(word_counter, word_list)

        if mode == "w":
            FileManager.save_json(article, word_counter)
        else:
            FileManager.save_json("count_words", word_counter, mode='a')

    # Performs --auto-count-words functionality
    @staticmethod
    def crawl(args, mode='a', wikiprefix=DEFAULT_WIKI, subprefix=DEFAULT_SUBPREFIX, localprefix=LOCAL_WIKI_PREFIX):
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
            cur_filepath = Scraper.get_article(article_name, wikiprefix=wikiprefix)
            candidates = Scraper.get_linked_articles(cur_filepath, subprefix=subprefix,
                                                     localprefix=localprefix, wikiprefix=wikiprefix)

            for article in candidates:
                bfs.appendleft([article, n + 1])
            word_list = Scraper.get_article_alpha_wordlist(cur_filepath)
            word_counter = Main.count_helper(word_counter, word_list)
            time.sleep(wait)
            visited.update({current[0]: True})
            FileManager.remove_file(cur_filepath)

        if mode == "w":
            FileManager.save_json("Word_freq_" + article_ori + "_depth_" +
                                  str(depth) + "_articles_" + str(num_articles), word_counter)    
        else:
            FileManager.save_json("count_words", word_counter, mode='a')    

    # Performs --Analyze-relative-word-frequency functionality
    @staticmethod
    def analyse(args):
        mode = args["mode"]
        count = args["count"]
        chartfilepath = args["chart"]
        combined_df = Analyser.getChartDf(Analyser.calculate_zipf_values("count_words.json"),
                                          count, mode)
        print(combined_df.to_string())
        ChartDrawer.drawFreqBarChart(combined_df, count, mode, chartfilepath=chartfilepath)
    
    # Dictionary for functions 
    execute_dict = {
            "summary": summary,
            "crawl": crawl,
            "table": table,
            "count": count,
            "analyse": analyse
            }

# Code that passes arguments from the parser and chooses the correct functions to run 
features = Parser.return_features()
for key, options in features.items():
    if options["set"] == True:
        Main.execute_dict[key](options)


    
    

