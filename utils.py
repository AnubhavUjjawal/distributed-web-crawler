import os, requests, itertools, rpyc
from bs4 import BeautifulSoup
from pprint import pprint
from pymongo import MongoClient

class Crawl_Frontier:
    """
        Crawl Frontier for visiting urls.
        Uses MongoDB to maintain priority queues.
        It is a worker used to crawl the urls
    """
    urls_to_visit = list()

    def __init__(self, urls_to_visit=[]):
        pass
    
    def add_to_visit(self, urls_to_visit):
        pass   
    
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
        
        """
        To convert into valid urls-
            Case 1. //av.wikipedia.org/
            Case 2. /static/
            Case 3. ../../static/
        """
        if a.startswith("//"):
            return "".join(["http:", a])
        if a.startswith("/"):
            return url + a[1:]
        if a.startswith("../"):
            path = a.split("../")
            back = path.count("")
            return "/".join(url.split("/")[:-1*(back+1)] + path[back:])
        return a

    def extract_anchor_links(self, doc):
        # implement filtering a by class or id here
        return list(map(lambda a: self.get_valid_link(a.get("href"), doc["url"]), doc["content"].find_all('a')))

    def print_list(self, items):
        print("\n".join(items))


class Crawler:
    """
        Master. Invokes the workers(crawl frontiers), distributes urls to them.
    """
    # initial list of websites to visit
    _seeds = list()
    _mongodb_server_url = ""
    _mongodb_user = ""
    _mongodb_password = ""
    _corpus_dir = ""
    # _workers is the list of (addr, port) tuples which will be addressed by rpyc.
    _workers = list()

    def __init__(self, seeds, mongodb_server_url, corpus_dir="./corpus", workers=[]):
        # Each seed have a default priority value of 10
        self._seeds = seeds
        self._mongodb_server_url = mongodb_server_url
        self._corpus_dir = corpus_dir
        if not os.path.exists(corpus_dir):
            os.makedirs(corpus_dir)
        self._workers = workers
        
    def check_workers(self):
        unable_to_connect = list()
        for worker in self._workers:
            # ping each worker for availability here
            try:
                rpyc.classic.connect(worker[0], port=worker[1])
            except Exception:
                # print(e)
                unable_to_connect.append(worker)
        return unable_to_connect

    def create_db_connect_url(self):
        if self._mongodb_user is "" or self._mongodb_password is "":
            return self._mongodb_server_url
        username_pass_join = ":".join([self._mongodb_user, self._mongodb_password])
        mongodb, url = self._mongodb_server_url.split("//")
        url_with_auth = "//".join([mongodb, "@".join([username_pass_join, url])])
        return url_with_auth

    def set_username_password(self, mongo_user, mongo_pass):
        self._mongodb_user = mongo_user
        self._mongodb_password = mongo_pass
        url_with_auth = self.create_db_connect_url()
        client = MongoClient(url_with_auth)
        db = client.admin
        serverStatusResult = db.command("serverStatus")
        client.close()
        return serverStatusResult

    def get_to_be_visited(self):
        url_with_auth = self.create_db_connect_url()
        client = MongoClient(url_with_auth)
        db = client.toBeVisited
        toBeVisited = list(db.pagesInfo.find())
        client.close()
        return toBeVisited

    def crawl(self):
        # start with seeds add them to db of to be visited.
        url_with_auth = self.create_db_connect_url()
        client = MongoClient(url_with_auth)
        db = client.toBeVisited
        for seed in self._seeds:
            if db.pagesInfo.find_one({"url": seed}) is  None:
                db.pagesInfo.insert_one({
                    "url": seed,
                    "inDegree": 0,
                    "outDegree": 0,
                    "seed": True,
                    "priority": 10
                })
        client.close()

        # returned_docs = list(map(lambda url: self.parse_get(url), self._seeds))
        # links_set = set(itertools.chain.from_iterable(list(map(lambda doc: self.extract_anchor_links(doc), returned_docs))))
        # self.print_list(links_set)


