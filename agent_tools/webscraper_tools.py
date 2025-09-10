from bs4 import BeautifulSoup
import requests
from pprint import pprint
from langchain.text_splitter import RecursiveCharacterTextSplitter
from colorama import Fore, Style, init
init(autoreset=True)


class WebScraper():
    """
    A simple web scraper that fetches and parses webpage content.
    class: WebScraper
    """

    def __init__(self, url):
        self.url = url
        self._log("INFO", f"Initialized WebScraper for URL: {self.url}")

    def _log(self, level, message):
        colors = {
            "INFO": Fore.CYAN,
            "WARN": Fore.YELLOW,
            "ERROR": Fore.RED
        }
        color = colors.get(level.upper(), Fore.WHITE)
        print(f"{color}[{level.upper()}]{Style.RESET_ALL} {message}")

    def fetch_content(self, heaeders=None, timeout=10):
        """Fetches the content of the webpage."""
        try:
            self._log("INFO", f"Fetching content from {self.url}")
            response = requests.get(
                self.url, headers=heaeders, timeout=timeout)
            if response.status_code == 200:
                self._log(
                    "INFO", f"Successfully fetched content from {self.url}")
                return response.text
            else:
                self._log(
                    "WARN", f"Failed to fetch {self.url} - Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self._log("ERROR", f"Exception while fetching {self.url}: {e}")
        return None

    def parse_content(self, html_content):
        """Parses the HTML content and returns the title."""
        if not html_content:
            self._log("WARN", "No HTML content provided for parsing.")
            return 'No content to parse'
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.title.string if soup.title else 'No title found'
        self._log("INFO", f"Parsed title: {title}")
        return title

    def scrape(self):
        """Scrapes the webpage and returns the title."""
        self._log("INFO", "Starting scrape process...")
        html_content = self.fetch_content()
        if html_content is None:
            self._log("ERROR", "Scrape failed due to missing content.")
            return 'Scrape failed'
        title = self.parse_content(html_content)
        return title

    def get_body(self):
        """Extracts and returns the body text of the webpage."""
        self._log("INFO", "Extracting body content...")
        html_content = self.fetch_content()
        if html_content is None:
            self._log("ERROR", "Failed to retrieve content for body extraction.")
            return 'Failed to retrieve content'
        soup = BeautifulSoup(html_content, 'html.parser')
        body = soup.body
        if body:
            self._log("INFO", "Successfully extracted body content.")
            return body.get_text(separator='\n', strip=True)
        else:
            self._log("WARN", "No <body> tag found in HTML.")
            return 'No body found'

    def chunk_web_content(self, chunk_size=500, chunk_overlap=50):
        """Chunks raw HTML content using LangChain's text splitter."""
        self._log("INFO", "Chunking raw HTML content...")
        raw_text = self.fetch_content()
        if raw_text is None:
            self._log("ERROR", "No content available for chunking.")
            return []
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_text(raw_text)
        self._log("INFO", f"Generated {len(chunks)} chunks from raw HTML.")
        return chunks

    def chunk_body_content(self, chunk_size=500, chunk_overlap=50):
        """Chunks body text using LangChain's text splitter."""
        self._log("INFO", "Chunking body content...")
        raw_text = self.get_body()
        if not raw_text or raw_text.startswith("Failed"):
            self._log("ERROR", "Body content unavailable for chunking.")
            return []
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_text(raw_text)
        self._log("INFO", f"Generated {len(chunks)} chunks from body content.")
        return chunks

    def get_all_links(self):
        """Extracts and returns all hyperlinks from the webpage."""
        self._log("INFO", "Extracting all hyperlinks...")
        html_content = self.fetch_content()
        if html_content is None:
            self._log("ERROR", "Failed to retrieve content for link extraction.")
            return []
        soup = BeautifulSoup(html_content, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        self._log("INFO", f"Found {len(links)} hyperlinks.")
        return links

    def __repr__(self):
        return f"WebScraper(url='{self.url}')"
