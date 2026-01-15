import pandas as pd
import wordfreq
import numpy
import matplotlib.pyplot as plt
from file_manager import FileManager  

class Analyser:

    @staticmethod
    def normalise_data(filename="count-words.json"):
        
        words = FileManager.load_json(filename)
        count = words["total"]
        print(count)
        words_df = pd.Series(words["list"]).to_frame("count")
        words_df = words_df.sort_values(by='count',ascending=False)
        words_df['count'] /= count
        words_df['count'] = numpy.log10(words_df['count']) + 9 
        Analyser.drawBarArticleChart(words_df)
        return words_df
        
    @staticmethod
    def drawBarArticleChart(article_data, num=24):

        top_n_words = article_data.head(num) 
        top_n_words.columns = ['Article Count']
        english_wordfreq = {}
        for row in top_n_words.itertuples():
            english_wordfreq.update({row.Index: wordfreq.zipf_frequency(str(row.Index),"en")})

        english_df = pd.Series(english_wordfreq).to_frame('English Count')

        combined_df = top_n_words.join(english_df, how='outer')
        combined_df = combined_df.fillna(0)
        combined_df = combined_df.sort_values(by='Article Count', ascending=True)
        print(combined_df.to_string())

        combined_df.plot(kind='bar', legend=False, color=['red','coral'])
        plt.title('Top 15 Most Frequent words')
        plt.xlabel('Zipf Score')
        plt.ylabel('Word')
        plt.xticks(rotation=45) 
        plt.tight_layout()      
        plt.show()
            
