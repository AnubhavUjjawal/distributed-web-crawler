import unittest
from utils import Crawler

class TestCrawler(unittest.TestCase):
    crawler = None
    def setUp(self):
        self.crawler = Crawler(seeds=["https://www.google.com", "https://www.wikipedia.org"], mongodb_server_link="", corpus_dir="./corpus")

    def test_links(self):
        self.assertEqual(self.crawler.get_valid_link("../../static/", "http://www.x.com/images/fuck/"), "http://www.x.com/static/")
        self.assertEqual(self.crawler.get_valid_link("../static/", "http://www.x.com/images/fuck/"), "http://www.x.com/images/static/")
        self.assertEqual(self.crawler.get_valid_link("/static/", "http://www.x.com/images/"), "http://www.x.com/images/static/" )
        self.assertEqual(self.crawler.get_valid_link("//pi.wikipedia.org/", "http://www.x.com/images/"), "http://pi.wikipedia.org/" )
        self.assertEqual(self.crawler.get_valid_link("//pi.wikipedia.org", "http://www.x.com/images/"), "http://pi.wikipedia.org/" )
        
if __name__ == '__main__':
    unittest.main()
    