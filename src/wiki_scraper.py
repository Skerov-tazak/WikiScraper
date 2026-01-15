from args_parser import Parser
from analyser import Analyser
import time
from scraper import Scraper
from file_manager import FileManager
from collections import deque

class Main:

    @staticmethod
    def summary(args):
        article = args["article"]

        filepath = Scraper.get_article(article)
        paragraph = Scraper.get_paragraph(filepath)
        if paragraph:
            print(paragraph.text)
        FileManager.remove_file(filepath)

    @staticmethod
    def table(args):
        article = args["article"]
        num = args["num"]
        isheader = args["header"]

        html_filepath = Scraper.get_article(article)
        table_text = Scraper.get_table(html_filepath, num)
        FileManager.remove_file(html_filepath)
        FileManager.save_csv(article, table_text, isheader)

    @staticmethod
    def count_helper(word_counter, word_list):
        for word in word_list:
            word_counter["total"] += 1
            if word in word_counter["list"]:
                word_counter["list"][word] += 1
            else:
                word_counter["list"].update({word: 1})
        return word_counter

    @staticmethod
    def count(args):
        article = args["article"]

        filepath = Scraper.get_article(article)
        word_list = Scraper.get_article_alpha_wordlist(filepath)
        word_counter = {"total": 0, "list": {}}
        word_counter = Main.count_helper(word_counter, word_list)
        FileManager.save_json(article, word_counter)
        

    @staticmethod
    def crawl(args):
        depth = args["depth"]
        article_ori = args["article"]
        wait = args["wait"]

        word_counter = {"total": 0, "list": {}}
        bfs = deque()
        visited = {}
        n = 0
        bfs.appendleft([article_ori, n])

        while len(bfs) > 0:
            current = bfs.pop()
            n = current[1]
            if current[0] in visited:
                continue
            if n > depth:
                break
            print(current)
            article_name = current[0]
            cur_filepath = Scraper.get_article(article_name)
            candidates = Scraper.get_linked_articles(cur_filepath)

            for article in candidates:
                bfs.appendleft([article, n + 1])
            word_list = Scraper.get_article_alpha_wordlist(cur_filepath)
            word_counter = Main.count_helper(word_counter, word_list)
            time.sleep(wait)
            visited.update({current[0]: True})
            FileManager.remove_file(cur_filepath)
           # time.sleep(args["wait"])
        FileManager.save_json("Word_freq_" + article_ori + "_depth_" + str(depth), word_counter)    

    @staticmethod
    def analyse(args):
        mode = args["mode"]
        count = args["count"]
        chartfilepath = args["chart"]
        Analyser.normalise_data("Word_freq_Randall_Munroe_depth_1.json")
        pass

    execute_dict = {
            "summary": summary,
            "crawl": crawl,
            "table": table,
            "count": count,
            "analyse": analyse
            }

features = Parser.return_features()
for key, options in features.items():
    if options["set"] == True:
        Main.execute_dict[key](options)


    
    

