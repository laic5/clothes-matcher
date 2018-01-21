import requests
import requests_cache
import urllib.request

requests_cache.install_cache('clothes_images')

count = 0

with open('image_links', 'r') as inF:
    for line in inF:
        line = line[1:-1]
        urllib.request.urlretrieve(line, 'images/image' + str(count) + '.jpg')
        count += 1
