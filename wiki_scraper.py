from args_parser import Parser
from scraper import Scraper
from data_analyser import Analyzer

class Main:

    @staticmethod
    def summary(args):
        filename = Scraper.get_article(args["article"])
        paragraph = Scraper.get_paragraph(filename)
        print(paragraph)

    @staticmethod
    def table(args):
        filename = Scraper.get_article(args["article"])
        table_text = Scraper.get_table(filename, args["num"])
        Analyzer.save_table(args["article"], table_text, args["header"])

    @staticmethod
    def count(args):
        pass

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


    
    

