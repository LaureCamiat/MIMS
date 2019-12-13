import requests
from lxml import html
from urllib.parse import urljoin
import threading
import time
import re

def updateImagesWithThread(url, lvl, nb_thread, images, extensions, threads):
    images.update(getImages(url,lvl, nb_thread, extensions, threads))    


def getImages(url, lvl, nb_thread, extensions, threads):
    """
        The function getImages returns images matching the extensions found in the given url 
    """
    res = set()

    try:
        response = requests.get(url)
    except Exception as e:
        print("An error occured with url '%s': %s" % (url,type(e))) 
        return []

    if not response:
        print("An error occurred with url '%s'. Code status: %s" % (url,response))
        return []

    tree = html.fromstring(response.content)    
    tree.make_links_absolute(url)

    urls = tree.xpath("//a/@href")
    images = tree.xpath("//img/@src")

    sorted_images = [item for item in images if item.endswith(extensions, re.I)]     
    res.update(sorted_images)

    if lvl < 2:
        lvl += 1           
        inner_crawl(urls,lvl,nb_thread,extensions,threads,res)                
                
    return res



def inner_crawl(urls,lvl,nb_thread,extensions,threads,res):
    """
        The function inner_crawl manages the launch of threads
    """
    for inner_url in urls:

        if nb_thread > 0:
            nb_thread -= 1
                
            t = threading.Thread(target=updateImagesWithThread, args=(inner_url,lvl,nb_thread,res,extensions,threads))
            t.start()
            threads.append(t)
        else:
            res.update(getImages(inner_url,lvl,nb_thread,extensions,threads))
 


def crawl(nb_thread, urls):
    """
        The function crawl recursively gathers images from given urls using nb_thread threads
    """
    start_time = time.time()
    extensions = ('.png','.gif','.jpg')
    threads = list()
    res = set()
    verrou = threading.Lock();
    
    nb_url = len(urls)
    print("Crawling %s urls with %s threads in progress..." %(nb_url, nb_thread))  

    with verrou:
        inner_crawl(urls,1,nb_thread,extensions,threads,res)

    for t in threads:
        t.join()

    print("--- Execution time: %s seconds" % (time.time() - start_time))
    print("--- %s images" % (len(res)))

    return res


        
        



