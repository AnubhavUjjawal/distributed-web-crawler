import rpyc, requests
from bs4 import BeautifulSoup
from pprint import pprint
from rpyc.utils.server import ThreadedServer

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


class FrontierService(rpyc.Service):
    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        pass

    def exposed_get_answer(self): # this is an exposed method
        return 42

    exposed_the_real_answer_though = 43     # an exposed attribute

    def get_question(self):  # while this method is not exposed
        return "what is the airspeed velocity of an unladen swallow?"
    
    def exposed_start(self):
        t = ThreadedServer(FrontierService, port=8000, auto_register=True)
        t.start()

if __name__ == "__main__":
    t = ThreadedServer(FrontierService, port=8000, auto_register=True)
    t.start()