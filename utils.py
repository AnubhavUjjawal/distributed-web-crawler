import os, requests, itertools, re
from bs4 import BeautifulSoup

class Pages:
    """
        A Web Page data structure.
    """
    _link = ""
    _indegree = 1

    def __init__(self, link, indegree):
        self._link = link
    
    def get_link(self):
        return self._link
    
    def increment_indegree(self):
        self._indegree += 1
    
    def get_indegree(self):
        return self._indegree

    # to be implemented
    def get_outdegree(self):
        return None



class Crawl_Frontier:
    """
        Crawl Frontier for maintaing the list of urls to visit.
        Uses MongoDB to maintain priority queues.
        It is a worker used to crawl the systems
    """
    urls_to_visit = list()

    def __init__(self, urls_to_visit):
        pass
    
    def add_to_visit(self, urls_to_visit):
        pass   
    
    def return_links(self):
        pass

class Crawler:
    # initial list of websites to visit
    _seeds = list()
    _mongodb_server_link = ""
    _corpus_dir = ""
    _workers = 1

    def __init__(self, seeds, mongodb_server_link, corpus_dir="./corpus", workers=1):
        # Each seed must have a priority value of 10
        self._seeds = seeds
        self._mongodb_server_link = mongodb_server_link
        self._corpus_dir = corpus_dir
        if not os.path.exists(corpus_dir):
            os.makedirs(corpus_dir)
        self._workers = workers
    
    def parse_get(self, url):
        res = requests.get(url)
        return {
            "content": BeautifulSoup(res.text, "html.parser"),
            "url": url
        }

    def get_valid_link(self, a, url):
        # url is the url of webpage from which a link is obtained
        # make sure a and url has / in the end
        if not a.endswith("/"):
            a =  "".join((a, "/"))
        if not url.endswith("/"):
            url =  "".join((url, "/"))
        if a.startswith("//"):
            return "".join(["http:", a])
        if a.startswith("/"):
            return url + a[1:]
        if a.startswith("../"):
            path = a.split("../")
            back = path.count("")
            # print(back)
            return "/".join(url.split("/")[:-1*(back+1)] + path[back:])
        return a

    def extract_anchor_links(self, doc):
        return list(map(lambda a: self.get_valid_link(a.get("href"), doc["url"]), doc["content"].find_all('a')))

    def print_list(self, items):
        print("\n".join(items))

    def crawl(self):
        returned_docs = list(map(lambda url: self.parse_get(url), self._seeds))
        links_set = set(itertools.chain.from_iterable(list(map(lambda doc: self.extract_anchor_links(doc), returned_docs))))
        self.print_list(links_set)
        

