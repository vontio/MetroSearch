import urllib2
from multiprocessing.dummy import Pool as ThreadPool

urls = [
    'http://www.python.org',
    'http://www.python.org/about/',
    ""
]


def a(url):
    return 1
# Make the Pool of workers
pool = ThreadPool(4)
# Open the urls in their own threads
# and return the results
results = pool.map(a, urls)
# close the pool and wait for the work to finish
pool.close()
pool.join()
print results
