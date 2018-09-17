import os, unittest, subprocess, signal
from utils import Crawler, Crawl_Frontier
from pymongo import MongoClient
from pprint import pprint

class TestCrawler(unittest.TestCase):
    @classmethod
    def setUpClass(self):               
        self.crawler = Crawler(
            seeds=["https://www.google.com", "https://www.wikipedia.org"],
            mongodb_server_url="mongodb://localhost:27017", 
            corpus_dir="./corpus",
            workers=[
                ("localhost", "8000"),
                ("localhost", "8001"),
                ("localhost", "8002"),
                ("localhost", "56477"), #this entry is for checking test_workers() returns error because no rpyc is running on this (host, port) pair value
            ])
        self.crawl_frontier = Crawl_Frontier()
        self.crawler.set_username_password("root", "qazwsxedc")

    def test_links(self):
        self.assertEqual(self.crawl_frontier.get_valid_link("../../static/", "http://www.x.com/images/fuck/"), "http://www.x.com/static/")
        self.assertEqual(self.crawl_frontier.get_valid_link("../../static/image.jpg", "http://www.x.com/images/fuck/"), "http://www.x.com/static/image.jpg/")
        self.assertEqual(self.crawl_frontier.get_valid_link("../static/", "http://www.x.com/images/fuck/"), "http://www.x.com/images/static/")
        self.assertEqual(self.crawl_frontier.get_valid_link("/static/", "http://www.x.com/images/"), "http://www.x.com/images/static/" )
        self.assertEqual(self.crawl_frontier.get_valid_link("//pi.wikipedia.org/", "http://www.x.com/images/"), "http://pi.wikipedia.org/" )
        self.assertEqual(self.crawl_frontier.get_valid_link("//pi.wikipedia.org", "http://www.x.com/images/"), "http://pi.wikipedia.org/" )

    def test_get_to_be_visited(self):
        self.crawler.crawl()
        self.assertGreaterEqual(len(self.crawler.get_to_be_visited()), 2)
        # pprint(self.crawler.get_to_be_visited())

    def test_workers(self):
        # make sure rpyc is running on localhost on ports 8000, 8001, 8002
        self.assertEqual(self.crawler.check_workers(), [("localhost", "56477"),])
        
if __name__ == '__main__':
    unittest.main()
    