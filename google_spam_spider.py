class GoogleSpamSpider:
    def __init__(
        self,
        url: str,
        direct_spam_logs: str,
        external_spam_logs: str
    ) -> None:
        self.direct_spam_logs = direct_spam_logs
        self.external_spam_logs = external_spam_logs
        self.unchecked_urls = [url]
        self.checked_urls = []
        self.crawl()

    def crawl(self) -> None:
        """Crawl as long as there are unchecked urls."""
        while self.unchecked_urls:
            url = self.unchecked_urls.pop()
            self.checked_urls.append(url)
            print(url)
            html = self.download(url)
            if html:
                if self.is_direct_spam(html):
                    self.log(self.direct_spam_logs, url)
                    self.parse(html)
                else:
                    self.log(self.external_spam_logs, url)
            else:
                print('Failed to download:', url)

    def download(self, url: str) -> None:
        import requests
        try:
            response = requests.get(url, timeout=1)
            return response.text
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def parse(self, html: str) -> None:
        from bs4 import BeautifulSoup
        dom = BeautifulSoup(html, features='html.parser')
        urls = dom.find_all('a')
        # print(urls)
        for url in urls:
            href = url.get('href')
            if href not in self.unchecked_urls + self.checked_urls:
                self.unchecked_urls.append(href)

    def is_direct_spam(self, html: str) -> bool:
        spam = '<html prefix="content:   dc:   foaf:   og: #  rdfs: #  schema:   sioc: #  sioct: #  skos: #  xsd: # " dir="ltr" lang="en">'
        return spam in html

    def log(self, path: str, url: str) -> None:
        with open(path, 'a') as f:
            f.write(url + '\n')
