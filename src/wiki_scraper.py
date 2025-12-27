from args_parser import Parser
from scraper import Scraper
from file_manager import FileManager

class Main:

    @staticmethod
    def summary(args):
        filepath = Scraper.get_article(args["article"])
        paragraph = Scraper.get_paragraph(filepath)
        print(paragraph.text)
        FileManager.remove_file(filepath)

    @staticmethod
    def table(args):
        html_filepath = Scraper.get_article(args["article"])
        table_text = Scraper.get_table(html_filepath, args["num"])
        FileManager.remove_file(html_filepath)
        FileManager.save_csv(args["article"], table_text, args["header"])

    @staticmethod
    def count(args):
        filepath = Scraper.get_article(args["article"])
        word_list = Scraper.get_article_alpha_wordlist(filepath)
        word_counter = {}
        for word in word_list:
            if word in word_counter:
                word_counter[word] += 1
            else:
                word_counter.update({word: 1})
        json_filepath = FileManager.save_json(args["article"], word_counter)
        return json_filepath
        
    @staticmethod
    def crawl(args):
        pass 

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


    
    

