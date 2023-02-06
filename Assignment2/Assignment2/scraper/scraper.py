'''
Scraper for: https://www.beeradvocate.com/beer/top-rated/
The below file will output a JSON file with ->
5-6 thousand reviews for various beers
this means we will scrape approximately 24 reviews per 250 beers
'''
import os
import sys
from bs4 import BeautifulSoup
import requests
import json
import re
from requests.models import Response
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# function to print sentiments of the sentence.
def sentiment_score(sentence):

	# Create a SentimentIntensityAnalyzer object.
	sid_obj = SentimentIntensityAnalyzer()

	# polarity_scores method of SentimentIntensityAnalyzer
	# object gives a sentiment dictionary which contains pos, neg, neu, and compound scores.
	sentiment_dict = sid_obj.polarity_scores(sentence)
	
	return sentiment_dict

# scraper object will be the entry point to the scraping functionality

class Scraper:
    def __init__(self, url, numReviews, verbose=False):
        self.url = url
        # approximate number of reviews to pull per beer (may not be exact)
        self.numReviews = numReviews
        self.verbose = verbose
        self.review_df = None
        self._links = []
        self._soup_home = None

    def _makeRequest(self):
        res = requests.get(self.url)
        src = res.content
        self._soup_home = BeautifulSoup(src, 'lxml')
        if self.verbose:
            print('The URL was successfully called')

    def _scrapeReviews(self):
        html_td = self._soup_home.find_all(
            'td', attrs={'align': 'left', 'class': 'hr_bottom_light'})
        count = 0
        for td in html_td:
            if td.a:
                if self.verbose:
                    print(f'Link: {td.a["href"]} added')
                self._links.append(td.a['href'])
                count += 1

        print(f"{count} links collected")

        # scrape for reviews at each link
        # {name: [reviews], name: [reviews]}
        count = 0
        with open('reviews.json', 'w') as out_file:
            data = {}
            s = ' '
            for link in self._links: # for each page 
                res = requests.get('https://www.beeradvocate.com/' + link)
                src = res.content
                indv_soup = BeautifulSoup(src, 'lxml')
                html_divs = indv_soup.find_all(
                    'div', attrs={'id': 'rating_fullview_content_2'})
                beer_name = indv_soup.find(
                    'div', attrs={'class': 'titleBar'}).h1.contents[0]
                
                data_reviews = []
                print(f'getting reviews for: {beer_name}')

                for html_div in html_divs: # for each review
                    full_entry = {}
                    review_text = html_div.contents
                    review_text = list(map((lambda x : str(x).strip()), review_text))
                    
                    # regex to find rating
                    pattern = r'^(<span class="muted">)(.+?(?=</span>))'
                    rating_matches = []
                    for item in review_text:
                        match = re.search(pattern, item)
                        if match:
                            rating_matches.append(match.group(2))
                    # extract rating for beer
                    for m in rating_matches:
                        if 'look' in m:
                            full_entry['rating'] = m
                
                    f = list(filter(lambda x : x.find('<') == -1 and x.find('rDev') == -1, review_text)) # filtering elements and wildcards
                    f = s.join(f)
                    full_entry['review'] = f

                    # perform sentiment analysis on review 
                    full_entry['sentiment'] = sentiment_score(f)

                    data_reviews.append(full_entry)
                
                data[beer_name] = data_reviews
               
            json_dumps = json.dumps(data, indent=4)
            out_file.write(json_dumps)
            print('JSON file was written to (reviews.json)')

    def getReviews(self):
        try:
            self._makeRequest()
        except requests.RequestException as e:
            print('There was a request exception')
            print(e)

        # scrape review _homeobjects
        self._scrapeReviews()

    def getReviewsForSpecificBeer(self, beerName: str):
        #TODO: Would be nice to have a function like this
        pass

if __name__ == "__main__":
    # create a Scraper object and call functions
    url = 'https://www.beeradvocate.com/beer/top-rated/'
    num_rev = 24
    scraper = Scraper(url, numReviews=num_rev, verbose=True)
    scraper.getReviews()
