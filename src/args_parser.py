"""Takes care of all argument parsing logic"""
from typing import Dict, Any
import argparse

def get_args():
    """Creates all the arguments"""
    parser = argparse.ArgumentParser()
    # Options for printing a summary
    parser.add_argument("--summary",type=str, default=None, nargs="?",
                        help="Prints a short summary of the article specified")
    # Options for printing the nth table
    parser.add_argument("--table",type=str, default=None, nargs="?",
                        help="Saves a table from specified article to a csv file - \
                                Please use --number to specify which table to save")

    parser.add_argument("--number",type=int, default=1, nargs="?",
                        help="The number of the table to print")

    parser.add_argument("--first-row-is-header", action="store_const", const=True, default=False,
                        help="Treats first row of the table as headers")
    # Options for counting words
    parser.add_argument("--count-words",type=str, default=None, nargs="?",
                        help="Adds the number of occurances of words \
                                in specified article to word-counts.json")
    # Options for analysing the frequencies
    parser.add_argument("--analyze-relative-word-frequency", action="store_const",
                        const=True, default=None,
                        help="Compares the frequency of words from word-counts.json \
                                to average frequency in the specified language")

    parser.add_argument("--mode",type=str, default="language", nargs="?",
                        help="language, article : Choose whether to sort the \
                                words based on the specified language or collected data")

    parser.add_argument("--count",type=int, default=1, nargs="?",
                        help="Specifies how many words to compare")

    parser.add_argument("--chart",type=str, default=None, nargs="?",
                        help="Saves a chart of frequencies to a csv file - please provide a path")
    # Options for crawling the Wiki and counting words
    parser.add_argument("--auto-count-words",type=str, default=None, nargs="?",
                        help="Crawl through the wiki starting from the \
                                provided phrase, counting word frequency")

    parser.add_argument("--depth",type=int, default=1, nargs="?",
                        help="Specifies how many links deep the crawler should venture")

    parser.add_argument("--wait",type=float, default=1, nargs="?",
                        help="Specifies how long the crawler should wait \
                                when jumping between articles")
    return parser.parse_args()

def check_features(args):
    """ Returns a dictionary of dictionaries of features, where each has a field
    "set" which tells us whether to activate this feauture module
    Stores as a dictionary each feature. First elemnt in the list is whether
    it is active - the next ones are args """

    print(args)
    features: Dict[str, Dict[str, Any]] = {
            "summary": {"set": False},
            "table": {"set": False},
            "count": {"set": False},
            "analyse": {"set": False},
            "crawl": {"set": False}}
    if args.summary is not None:
        features["summary"].update({"set": True})
        features["summary"].update({"article": args.summary.replace(" ", "_")})
    if args.table is not None:
        features["table"].update({"set": True})
        features["table"].update({"article": args.table.replace(" ", "_")})
        features["table"].update({"num": args.number})
        features["table"].update({"header": args.first_row_is_header})
    if args.count_words is not None:
        features["count"].update({"set": True})
        features["count"].update({"article": args.count_words.replace(" ", "_")})
    if args.analyze_relative_word_frequency is not None:
        features["analyse"].update({"set": True})
        print(args.mode)
        if args.mode not in ("language", "article"):
            features["analyse"].update({"mode": args.mode})
            features["analyse"].update({"count": args.count})
            features["analyse"].update({"chart": args.chart})
        else:
            raise Exception("The --mode option must be either \"language\" or \"article\"")
    if args.auto_count_words is not None:
        features["crawl"].update({"set": True})
        features["crawl"].update({"article": args.auto_count_words.replace(" ","_")})
        features["crawl"].update({"depth": args.depth})
        features["crawl"].update({"wait": args.wait})
    return features

def return_features():
    """Prop function to merge the other two in one neet package"""
    return check_features(get_args())
