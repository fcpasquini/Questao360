from lxml import etree
import requests

class Parser:
    '''
    The parser classes of the Ethical Trust project requires the webpage data in a etree format, to be able to process them using 
    xpath and extract the exact information we are searching for
    '''    
    def parse_main_page(self, soup):
        '''
        The function receives the information of the webpage in a etree format to use xpath and them returns a dictionary with 
        all the headlines and its links, so the project is able to reiterate over the links to extract the information 
        from child pages
        '''
        dict_headlines = {}
        dom = etree.HTML(str(soup))

        # This is the parser of headlines using the /h3 format
        headlines = dom.xpath(r'//*/h3')

        for i in range(len(headlines)):
            try:

                headline_text = headlines[i].text.strip()
                
                # Iterate through parent elements until we find the 'a' tag
                headline_iter = headlines[i].getparent()

                while headline_iter is not None and headline_iter.tag != 'a':
                    headline_iter = headline_iter.getparent()

                headline_link = headline_iter.get('href')

                if r"https://www.nytimes.com/" not in headline_link:
                    headline_link = r"https://www.nytimes.com/" + headline_link

                dict_headlines.update({headline_text:headline_link})
            except Exception as e:
                print(e)
    
        return dict_headlines
    
    def parse_child_pages(self, page_name, url, soup, source_id):
        '''
        The function receives the information of the child webpage in a etree format to use xpath and them returns a dictionary with 
        the data of the page in a text format and stores it in a gzip file
        '''

        dom = etree.HTML(str(soup))

        # This is the parser of the headline
        try:
            title = dom.xpath(r'//*/h1')[0].text
        except:
            title = ''
        
        body = r"\n".join([soup.find_all('p')[body].text for body in range(len(soup.find_all('p')))])
        return ((title, page_name, url, source_id), body)
    
    def fetch_api(self, api_key):

        # Set the section (e.g., 'home' for the homepage)
        section = 'home'

        # Construct the API URL
        url = f'https://api.nytimes.com/svc/topstories/v2/{section}.json?api-key={api_key}'

        # Send a GET request to the API endpoint
        response = requests.get(url)

        # Check the response status code
        if response.status_code == 200:
            # The request was successful
            data = response.json()

            # Access the articles in the response data
            articles = data['results']
            return articles, response.status_code

        else:
            # There was an error
            articles = ''            
        return articles, response.status_code