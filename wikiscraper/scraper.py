"""Scrapes the wiki webpage and operates on the scraped material"""
import requests
from bs4 import BeautifulSoup
from wikiscraper import file_manager
DEFAULT_SUBPREFIX = "https://www.explainxkcd.com"
LOCAL_WIKI_PREFIX = "/wiki/index.php/"

def get_article(article_name, wikiprefix=DEFAULT_SUBPREFIX+LOCAL_WIKI_PREFIX, fold="html") -> str:
    """Saves article html based on its name and the wiki it comes from"""
    content = requests.get(wikiprefix + article_name)
    return file_manager.save_html(article_name, content, directory=fold)

def get_article_from_link(article_link, fold="html"):
    """Saves artcile html based on its link"""
    content = requests.get(article_link)
    return file_manager.save_html(article_link, content, directory=fold)

def get_elements(filepath, element_type=None, html_id=None):
    """Returns specified elements from an html file of a specified type and/or ID"""
    with open(filepath, "r", encoding="utf=8") as file:
        soup = BeautifulSoup(file.read(), "html.parser")
        if element_type and html_id:
            list_tag = soup.find_all(element_type, {"id": html_id})
        elif element_type:
            list_tag = soup.find_all(element_type)
        elif html_id:
            list_tag = soup.find_all(id=html_id)
        else:
            list_tag = soup.text

        if list_tag:
            return list(list_tag)

        raise Exception("Błąd podczas czytania strony!")

def get_paragraph(filepath, number=1):
    """Returns the nth paragraph from specified file"""
    paragraphs = get_elements(filepath, "p")
    if paragraphs is None or len(paragraphs) < number:
        raise Exception(f"{number} paragraph on this website don't exist!")
    return paragraphs[number - 1] # Number idexes from 1 as in problem statement

def get_table(filepath, number=1):
    """Returns the nth table from html file"""
    tables = get_elements(filepath, "table")
    if tables is None or len(tables) < number:
        raise Exception(f"{number} tables on this website don't exist!")
    return tables[number - 1]

def get_wikilinks(filepath, wikiprefix=LOCAL_WIKI_PREFIX, subprefix=DEFAULT_SUBPREFIX):
    """Returns a list of all internal links from some wiki page in an html file"""
    links = get_elements(filepath, "a")
    wiki_link_list = []
    if links is None:
        raise Exception("Page Loading Error")
    for link_obj in links:
        if link_obj:
            if link_obj.get("href") and str(link_obj.get("href")).startswith(wikiprefix):
                wiki_link_list.append(subprefix + str(link_obj.get("href")))
    return wiki_link_list

def get_linked_articles(filepath, localprefix=LOCAL_WIKI_PREFIX, subprefix=DEFAULT_SUBPREFIX):
    """Based on a list of wikilinks returns a list of article names"""
    wikiprefix = localprefix + subprefix
    links = get_wikilinks(filepath, wikiprefix=localprefix, subprefix=subprefix)
    article_names = []
    for link in links:
        article_names.append(link.removeprefix(wikiprefix))
    return article_names

def get_article_alpha_wordlist(filepath, content_id="content"):
    """Returns a list of all the alpha words from an html file with repetitions"""
    clean_list = []
    article_content = get_elements(filepath, html_id=content_id)
    if article_content:
        article_content = article_content[0]
        text = article_content.get_text(separator=" ", strip=True)
        word_list = text.split()
        for word in word_list:
            if word.isalpha():
                clean_list.append(word)
    return clean_list
