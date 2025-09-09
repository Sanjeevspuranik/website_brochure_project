from bs4 import BeautifulSoup
import requests
from pprint import pprint
from langchain.text_splitter import RecursiveCharacterTextSplitter


class WebScraper():
    """
    A simple web scraper that fetches and parses webpage content.
    class: WebScraper
    """

    def __init__(self, url):
        self.url = url

    def fetch_content(self, heaeders=None, timeout=10):
        """
        Fetches the content of the webpage.
        Raises:
            Exception: _if request fails

        Returns:
            str: _webpage content as string
        """
        try:
            response = requests.get(
                self.url, headers=heaeders, timeout=timeout)
            if response.status_code == 200:
                return response.text
            else:
                print(
                    f"[WARN] Failed to fetch {self.url} - Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Exception while fetching {self.url}: {e}")
            return None

    def parse_content(self, html_content):
        """_summary_

        Args:
            html_content (_type_): _description_

        Returns:
            str: 
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.title.string if soup.title else 'No title found'

    def scrape(self):
        """
        Scrapes the webpage and returns the title.
        Returns:
            str: returns the title of the webpage
        """
        html_content = self.fetch_content()
        title = self.parse_content(html_content)
        return title

    def get_body(self):
        """
        Extracts and returns the body text of the webpage.
        Returns:
            str: returns the body text of the webpage
        """
        html_content = self.fetch_content()
        if html_content is None:
            return 'Failed to retrieve content'
        soup = BeautifulSoup(html_content, 'html.parser')
        body = soup.body
        return body.get_text(separator='\n', strip=True) if body else 'No body found'

    def chunk_web_content(self, chunk_size=500, chunk_overlap=50):
        """ 
        converts web content into chunks using langchain's RecursiveCharacterTextSplitter
        Returns:
            List[str]: A list of text chunks from the web content.
        """
        raw_text = self.fetch_content()
        if raw_text is None:
            return []
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_text(raw_text)
        return chunks

    def chunk_body_content(self, chunk_size=500, chunk_overlap=50):
        """ 
        converts web body content into chunks using langchain's RecursiveCharacterTextSplitter
        Returns:
            List[str]: A list of text chunks from the web content.
        """
        raw_text = self.get_body()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_text(raw_text)
        return chunks

    def get_all_links(self):
        """
        Extracts and returns all hyperlinks from the webpage.
        Returns:
            List[str]: A list of all hyperlinks found on the webpage.
        """
        html_content = self.fetch_content()
        if html_content is None:
            return "Failed to retrieve content"
        soup = BeautifulSoup(html_content, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return links

    def __repr__(self):
        """
        String representation of the WebScraper instance.
        Returns:
            str: _string representation of the WebScraper instance
        """
        return f"WebScraper(url='{self.url}')"
