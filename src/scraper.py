from bs4 import BeautifulSoup
from file_manager import FileManager
import requests
DEFAULT_WIKI = "https://www.explainxkcd.com/wiki/index.php/"

class Scraper:

    @staticmethod
    def get_article(article_name, wikiprefix=DEFAULT_WIKI) -> str:    
        content = requests.get(wikiprefix + article_name)
        return FileManager.save_html(article_name, content)

    # Returns a list of all elements of a specified type and/or ID      
    @staticmethod
    def get_elements(filename, element_type=None, id=None):  
        list_elem = [] 
        with open(filename, 'r') as file:
           soup = BeautifulSoup(file.read(), 'html.parser')
           if element_type and id:
               return soup.find_all(element_type, {"id": id})
           elif element_type:
               list_tag = soup.find_all(element_type)
           elif id:
               return soup.find_all(id=id)
           else:
               return soup
           if list_tag:
                for elem in list_tag:
                    list_elem.append(elem)
        return list_elem 

    @staticmethod
    def get_paragraph(filename, number=1):
        paragraphs = Scraper.get_elements(filename, 'p')
        if paragraphs == None or len(paragraphs) < number:
            raise Exception(f"{number} paragraph on this website don't exist!")
        return paragraphs[number - 1] # Number idexes from 1 as in problem statement 

    @staticmethod
    def get_table(filename, number=1):
        tables = Scraper.get_elements(filename, 'table')
        if tables == None or len(tables) < number:
            raise Exception(f"{number} tables on this website don't exist!")
        return tables[number - 1] 

    # CHECK IF WORKS
    @staticmethod
    def get_wikilinks(filename, wikiprefix=DEFAULT_WIKI):
        links = Scraper.get_elements(filename, 'a')
        wiki_link_list = []
        if links == None:
            raise Exception("Page Loading Error")
        for link_obj in links:
            if link_obj:
                if link_obj.href.startswith(wikiprefix):
                    wiki_link_list.append(link_obj.href)
        return wiki_link_list

    # CHECK IF WORKS
    @staticmethod
    def get_article_alpha_wordlist(filename, content_id='content'):
        clean_list = []
        article_content = Scraper.get_elements(filename, id=content_id)
        if article_content:
            article_content = article_content[0]
            text = article_content.get_text(separator=" ", strip=True)
            word_list = text.split()
            for word in word_list:
                if word.isalpha():
                    clean_list.append(word)
        return clean_list    
        
        
                

