from args_parser import Parser
import time
from scraper import Scraper
from file_manager import FileManager
from collections import deque

class Main:

    @staticmethod
    def summary(args):
        filepath = Scraper.get_article(args["article"])
        paragraph = Scraper.get_paragraph(filepath)
        if paragraph:
            print(paragraph.text)
        FileManager.remove_file(filepath)

    @staticmethod
    def table(args):
        html_filepath = Scraper.get_article(args["article"])
        table_text = Scraper.get_table(html_filepath, args["num"])
        FileManager.remove_file(html_filepath)
        FileManager.save_csv(args["article"], table_text, args["header"])

    @staticmethod
    def count_helper(word_counter, word_list):
        for word in word_list:
            if word in word_counter:
                word_counter[word] += 1
            else:
                word_counter.update({word: 1})
        return word_counter

    @staticmethod
    def count(args):
        filepath = Scraper.get_article(args["article"])
        word_list = Scraper.get_article_alpha_wordlist(filepath)
        word_counter = []
        word_counter = Main.count_helper(word_counter, word_list)
        FileManager.save_json(args["article"], word_counter)
        

    @staticmethod
    def crawl(args):
        word_counter = {}
        bfs = deque()
        visited = {}
        n = 0
        bfs.appendleft([args["article"], n])
        while len(bfs) > 0:
            current = bfs.pop()
            n = current[1]
            if current[0] in visited:
                continue
            if n > args["depth"]:
                break
            print(current)
            article_name = current[0]
            cur_filepath = Scraper.get_article(article_name)
            candidates = Scraper.get_linked_articles(cur_filepath)
            for article in candidates:
                bfs.appendleft([article, n + 1])
            word_list = Scraper.get_article_alpha_wordlist(cur_filepath)
            word_counter = Main.count_helper(word_counter, word_list)
            time.sleep(0.05)
            visited.update({current[0]: True})
            FileManager.remove_file(cur_filepath)
           # time.sleep(args["wait"])
        FileManager.save_json("Word_freq_" + args["article"] + "_depth_" + str(args["depth"]), word_counter)    

    @staticmethod
    def analyse(args):
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


    
    

