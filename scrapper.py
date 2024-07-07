
from bs4 import BeautifulSoup
import requests,sys,signal
from termcolor import colored


class Scrappe:
    def __init__(self):
        signal.signal(signal.SIGINT,self.exit)
        self.url=input("Github url: ") 
        self.extension="."+input("Extension of file to scrape: ")
        self.repos=[]
    def git_scrape(self):
        request=requests.get(self.url)
        url_parts = self.url.split("/")

        soup=BeautifulSoup(request.content,'html.parser')
        for price in soup.find_all('span', class_="repo"):
            price=price.text.strip()
            self.repos.append(price)
        repository_urls = []
        for repo_element in self.repos:
            repository_urls.append(self.url + "/" + repo_element)

        for repo_url in repository_urls:
            response = requests.get(repo_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            anchor_tags = soup.find_all('a')
            final_url = set()
            for anchor in anchor_tags:
                href = anchor.get("href")
                if url_parts[-1] in href and self.extension in href: 
                    path="https://github.com" + href
                    final_url.add(path)
            
            
            for url in final_url:
                print(colored('[+]','green')+url)    

    def exit(self,sig,frame):
        sys.exit(0)
    
    def run(self):
        try:
            self.git_scrape()
        except Exception as e:
            print(f"error: {e}")

if __name__=="__main__":
    scrapper=Scrappe()
    scrapper.run()
