import os, requests, itertools, rpyc
from bs4 import BeautifulSoup
from pprint import pprint
from pymongo import MongoClient

def equal_weights_url_priority_policy(urls):
        # this method assigns equal weights to each url i.e, 10
        pass

def simple_distribution_policy(a, n):
        # a is the array, n is the number of chunks in which the array is to be divided
        k, m = divmod(len(a), n)
        return list(a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

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

    def __init__(self, seeds, mongodb_server_url, corpus_dir="./corpus"):
        # workers can be found on runnning rpyc.discover("FRONTIER")
        # Each seed have a default priority value of 10
        self._seeds = seeds
        self._mongodb_server_url = mongodb_server_url
        self._corpus_dir = corpus_dir
        if not os.path.exists(corpus_dir):
            os.makedirs(corpus_dir)

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

    def get_to_be_visited(self, limit=0):
        url_with_auth = self.create_db_connect_url()
        client = MongoClient(url_with_auth)
        
        # this collection in mongoDB contains all the links to be visited
        # return the urls on the basis of their priority
        db = client.toBeVisited
        toBeVisited = list(db.pagesInfo.find().sort([("url", 1), ("priority", 1)]).limit(limit))
        client.close()
        return toBeVisited

    def get_workers(self):
        # discovers and returns the tuple of (addr, port) values of workers
        return rpyc.discover("FRONTIER")
    
    def distribute_urls_to_workers(self, distribution_policy):
        workers = self.get_workers()
        to_be_visited = self.get_to_be_visited()
        chunkified_to_be_visited = distribution_policy(to_be_visited, workers.__len__())
        pprint(chunkified_to_be_visited)

    def start_workers(self):
        # call get_workers to get all active workers
        # distribute each seed url randomly to active reachable workers.
        workers = self.get_workers()
        return workers

    def crawl(self, distribution_policy=simple_distribution_policy, url_priority_policy=equal_weights_url_priority_policy):
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
        self.distribute_urls_to_workers(distribution_policy=distribution_policy)
        self.start_workers()
        # we have to check if worker is alive or not every N seconds.
        # keep alive is in rpyc_registry.py

        # returned_docs = list(map(lambda url: self.parse_get(url), self._seeds))
        # links_set = set(itertools.chain.from_iterable(list(map(lambda doc: self.extract_anchor_links(doc), returned_docs))))
        # self.print_list(links_set)


