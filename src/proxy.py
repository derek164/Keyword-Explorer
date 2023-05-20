import random
import time

import requests
from fp.fp import FreeProxy


class ProxySource:
    """
    More sources can be found @https://github.com/topics/free-proxy
    Consider OTS solution @https://github.com/idandaniel/ballyregan/
    """

    # @property
    # def jetkai_https(self):
    #     """https://github.com/jetkai/proxy-list"""
    #     url = "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt"
    #     page = requests.get(url)
    #     return page.text.split("\n")

    # @property
    # def jetkai_http(self):
    #     """https://github.com/jetkai/proxy-list"""
    #     url = "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt"
    #     page = requests.get(url)
    #     return page.text.split("\n")

    @property
    def speedx_http(self):
        """https://github.com/TheSpeedX/PROXY-List"""
        url = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
        page = requests.get(url)
        return page.text.split("\n")

    @property
    def murongpig_http(self):
        """https://github.com/MuRongPIG/Proxy-Master"""
        url = "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt"
        page = requests.get(url)
        return page.text.split("\n")

    @property
    def prxchk_http(self):
        """https://github.com/prxchk/proxy-list"""
        url = "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt"
        page = requests.get(url)
        return page.text.split("\n")

    @property
    def lionkings_http(self):
        """https://github.com/saisuiu/Lionkings-Http-Proxys-Proxies"""
        url = "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/free.txt"
        page = requests.get(url)
        return page.text.split("\n")

    @property
    def hyperbeats_http(self):
        """https://github.com/HyperBeats/proxy-list"""
        url = "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt"
        page = requests.get(url)
        return page.text.split("\n")

    @property
    def hyperbeats_https(self):
        """https://github.com/HyperBeats/proxy-list"""
        url = "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/https.txt"
        page = requests.get(url)
        return page.text.split("\n")

    @property
    def jih4dhoss4in_http(self):
        """https://github.com/JIH4DHoss4in/PROXY-List"""
        url = "https://raw.githubusercontent.com/JIH4DHoss4in/PROXY-List/main/http.txt"
        page = requests.get(url)
        return page.text.split("\n")

    @property
    def caliphdev_http(self):
        """https://github.com/caliphdev/Proxy-List"""
        url = "https://raw.githubusercontent.com/caliphdev/Proxy-List/master/http.txt"
        page = requests.get(url)
        return page.text.split("\n")

    @property
    def uptimerbot_http(self):
        """https://github.com/UptimerBot/proxy-list"""
        url = "https://raw.githubusercontent.com/UptimerBot/proxy-list/master/proxies/http.txt"
        page = requests.get(url)
        return page.text.split("\n")

    @property
    def freeproxy_ssl(self):
        return FreeProxy(timeout=1).get_proxy_list(repeat=True)

    @property
    def freeproxy_us(self):
        return FreeProxy(country_id=["US"], timeout=1).get_proxy_list(repeat=False)

    @property
    def freeproxy_gb(self):
        return FreeProxy(country_id=["GB"], timeout=1).get_proxy_list(repeat=False)


class ProxyProvider(ProxySource):
    def __init__(self, schema, timeout):
        self.schema = schema
        self.timeout = timeout
        self.proxies = self.load()

    @property
    def num_proxies(self):
        return len(self.proxies)

    def load(self):
        proxies = []
        for attr in dir(ProxySource):
            if isinstance(getattr(ProxySource, attr), property):
                proxies.extend(getattr(self, attr))

        proxies = list(set(proxies))
        print(len(proxies))
        return proxies

    def remove(self, proxy):
        self.proxies.remove(proxy)
        if (self.num_proxies % 1000) == 0:
            print(f"Remaining proxies: {self.num_proxies}")

    def shuffle(self):
        random.shuffle(self.proxies)

    def refresh(self):
        self.proxies = self.load()

    def test_proxy(self, proxy_address):
        try:
            response = requests.get(
                url=f"https://httpbin.org/ip",
                proxies={"http": proxy_address},
                timeout=self.timeout,
            )
            if response.status_code == 200:
                return proxy_address
        except:
            return


class ProxyPool(ProxyProvider):
    def __init__(self, schema="http", timeout=1):
        super().__init__(schema, timeout)
        self.pool = {}

    @property
    def size(self):
        return len(self.pool)

    def put(self, proxy):
        if proxy not in self.pool:
            print(f"Adding proxy to pool: {self.size} proxies queued")
            self.pool[proxy] = time.time()

    def get(self):
        """Serve working proxy or test new proxy.

        The proxy pool is a strictly ordered queue.
        Each proxy is guaranteed to wait in the queue for 30 seconds,
        which is the maximum duration of a request, to avoid collisions.
        """

        if (self.size > 50) and (random.random() < 0.4):
            proxy, time_added = next(iter(self.pool.items()))
            if (time.time() - time_added) > 30:
                self.pool.pop(proxy)
                print(f"Serving proxy from pool: {proxy}")
                return proxy
        while True:
            proxy = random.choice(self.proxies)
            if proxy not in self.pool:
                return proxy

    def clear(self):
        self.pool = []


def test_crossref(proxy_url):
    print("Testing proxy: %s" % proxy_url)
    response = requests.get(
        "https://api.crossref.org/works",
        proxies={"http": proxy_url},
        params={
            "rows": 1,
            "select": "URL,score",
            "query.author": "lance waller ph.d.",
            "query.bibliographic": "Exploratory Spatial Analysis in Disease Ecology",
            "mailto": "derekz3@illinois.edu",
        },
    )
    if response.status_code == 200:
        print("Found working proxy: %s" % proxy_url)
        print(response.json())
    else:
        print((response.status_code, proxy_url))


if __name__ == "__main__":
    proxy_pool = ProxyPool()
    print(proxy_pool.num_proxies)
    proxy_url = proxy_pool.get()
    test_crossref(proxy_url)
