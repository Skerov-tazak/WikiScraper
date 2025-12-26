from bs4 import BeautifulSoup
import requests

class Scraper:

    @staticmethod
    def get_article(article_name) -> str:    
        filename = article_name + ".html"
        with open(filename, 'w') as file:
            content = requests.get('https://www.explainxkcd.com/wiki/index.php/' + article_name)
            file.write(content.text)
        return filename 
            
    @staticmethod
    def get_paragraph(filename) -> str:  
        paragraph = ""
        with open(filename, 'r') as file:
           soup = BeautifulSoup(file.read(), 'html.parser')
           paragraph_tag = soup.find('p')
           if paragraph_tag:
               paragraph = paragraph_tag.text
        return paragraph 

    @staticmethod
    def get_table(filename, table_num): 
        table = ""
        with open(filename, 'r') as file:
           soup = BeautifulSoup(file.read(), 'html.parser')
           tables = soup.find_all('table')
           if tables == None or len(tables) <= table_num:
               raise Exception(f"The {table_num}th table doesn't exist on this site! (Numbered from 1)")
           table = tables[table_num]
        return table.prettify()
        
                

