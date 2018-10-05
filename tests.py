import os, unittest, subprocess, rpyc
from crawler import Crawler
from frontier import Crawl_Frontier
from pymongo import MongoClient
from pprint import pprint

# At least a worker on 1 ((addr, port),) is to be run during testing

class TestCrawler(unittest.TestCase):
    @classmethod
    def setUpClass(self):   
        self.crawler = Crawler(
            seeds=["https://www.google.com", "https://www.wikipedia.org"],
            mongodb_server_url="mongodb://localhost:27017", 
            corpus_dir="./corpus")
        self.crawl_frontier = Crawl_Frontier()
        self.crawler.set_username_password("root", "qazwsxedc")

    def test_links(self):
        self.assertEqual(self.crawl_frontier.get_valid_link("../../static/", "http://www.x.com/images/fuck/"), "http://www.x.com/static/")
        self.assertEqual(self.crawl_frontier.get_valid_link("../../static/image.jpg", "http://www.x.com/images/fuck/"), "http://www.x.com/static/image.jpg/")
        self.assertEqual(self.crawl_frontier.get_valid_link("../static/", "http://www.x.com/images/fuck/"), "http://www.x.com/images/static/")
        self.assertEqual(self.crawl_frontier.get_valid_link("/static/", "http://www.x.com/images/"), "http://www.x.com/images/static/" )
        self.assertEqual(self.crawl_frontier.get_valid_link("//pi.wikipedia.org/", "http://www.x.com/images/"), "http://pi.wikipedia.org/" )
        self.assertEqual(self.crawl_frontier.get_valid_link("//pi.wikipedia.org", "http://www.x.com/images/"), "http://pi.wikipedia.org/" )

    # def test_distribute_urls_to_workers(self):

    def test_get_to_be_visited(self):
        self.crawler.crawl()
        self.assertGreaterEqual(len(self.crawler.get_to_be_visited()), 2)
        # pprint(self.crawler.get_to_be_visited())

    def test_start_workers(self):
        workers_list = self.crawler.start_workers()
        self.assertGreaterEqual(workers_list.__len__(), 1)

if __name__ == '__main__':
    unittest.main()
    