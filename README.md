# Wikiscraper - a tool for wiki Language Analysis and Scraping

A web scraping and natural language processing tool that analyzes word frequencies across different languages. This project extracts text from Bulbapedia (Pokewiki de/fr) and ExplainXKCD articles (but it easily supports any other wiki-ecosystem with a few changes, forks welcome), processes the data, and applies statistical concepts like Zipf's Law and Kullback-Leibler (KL) Divergence to calculate language confidence scores.

## Key Features

* **Automated Web Crawler:** Implements a Breadth-First Search (BFS) algorithm to navigate and scrape linked articles up to a specified depth.
* **Statistical Text Analysis:** Calculates word probabilities and compares Zipf's Law distributions against scraped data from articles.
* **Language Detection & Scoring:** Compares scraped text frequencies against baseline language models using KL Divergence to accurately identify the text's language.
* **Data Visualization:** Generates comparative bar charts to visualize word frequency distributions and test results using Matplotlib.
* **Modular Architecture:** Clean separation of concerns across scraping, data management, mathematical analysis, and visualization.
* **Procedural Programming:** Allows for better focus on functions and pipelining rather than objects (though OOP forks are welcome)  

## Technologies Used

* **Language:** Python 3
* **Web Scraping:** `requests`, `BeautifulSoup4`
* **Data Manipulation:** `pandas`, `numpy`
* **Natural Language Processing:** `wordfreq`
* **Visualization:** `matplotlib`

## Project Structure

* `language_analysis.py`: The main script that runs the analysis pipeline and joins datasets for final scoring.
* `wiki_scraper.py`: Handles CLI-like execution for scraping, summarizing, and building word counts.
* `scraper.py`: Core web scraping logic, HTML parsing, and DOM traversal.
* `analyzer.py`: Contains calculating probabilities, Zipf values, and formatting DataFrames.
* `chart_engine.py`: Dedicated module for generating and exporting statistical charts.
* `file_manager.py`: Utility for handling all file I/O operations (JSON, CSV, HTML, TXT).
* `unit_test.py` & `integration_test.py`: Automated testing to ensure scraper and analyzer reliability.

## Installation & Setup

### 1. Clone the repository:
   ```bash
   git clone https://github.com/Skerov-tazak/WikiScraper.git
   cd WikiScraper
   ```
### 2. Create a virtual environment:
   ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
### 3. Install the project and dependencies
   ```bash
    pip install . # Use pip install .[dev] if running tests
   ```
## Important note on the statistical method used

Most of the measurements that are shown in the example jupyter notebook and the visualisations that are coded into `draw_language_test_bar_chart()` function in `chart_engine.py`, as well as the choice of articles in `language_analysis.py` is not very scientifically valid. Of course everyone is welcome to modify the folders the analysis tool draws from as well as the content of the charts. The example doesn't try very hard to control for important factors such as topic, length or date. 

The programme unfortunately does not calculate and show averages either. The goal was to create a tool and showcase its use - other interesting or important scientific aspects were sidelined. The most important and useful part of the project is the entire `wikiscraper` package and the `perform_tests()`, `lang_confidence_score()` and `prepare_test_articles()` functions. They allow you to analyse any properly structured json against any language and any number of most popular words. 

## Other used folders 

The project will create a few folders in the main `WikiScraper` folder that it is cloned into when used. Notably: `charts`, `csv`, `json`, `html` and `txt`. The names are quite self-explanatory. The `json` directory is the most important - it contains language folders and the art folder. These folders will contain all the `json` word counts for any article. It is quite simple to change these folder names - but it is not necessary as you can easily manually change their content. The txt file should contain all the txt articles that `language_analysis.py` will turn into word counts and save in `json/art`.

## Future Plans

- [ ] **Modularise analysis with CLI interface:** In its current state analyzing data is not modular or really easy to do. It requires hard-coding the paths, languages and articles. In the future the plan is to create a friendly modular CLI interace, as well as a settings.json file that will contains all parameters for easier use. 
- [ ] **Make the analysis full and comprehensive:** The changes outlined above can be used to create a better graphin and data-collection environement. This will allow for controlled studies of performance between languages and divergence functions.

### With the above mentioned changes the software will be useful for conducting any type of language word frequency research on wiki sites on the net.

**NOTE: SCRAPING WEBSITES IS NOT ALWAYS LEGAL, PLEASE ALWAYS CHECK THE LICENCE. THE AUTHOR OF THIS SOFTWARE DOES NOT CONDONE OR TAKE RESPONSIBILITY FOR ANY ILLEGAL ACTIONS PERPETRATED WITH ITS USE**


