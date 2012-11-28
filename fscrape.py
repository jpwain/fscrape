# Scrape some info from Fancy

import urllib2
from bs4 import BeautifulSoup

urlist = ['http://www.thefancy.com/things/235842739','http://www.thefancy.com/things/226011919083903237', 'http://www.thefancy.com/things/225361396508920913']

for item in urlist:

	page = urllib2.urlopen(item).read()

	soup = BeautifulSoup(page)

	itemTitle = soup.figcaption.string
	itemImageURL = soup.find(class_='fig-image').img['src']
	itemPrice = soup.find(class_='price').string

	print itemTitle
	print itemImageURL
	print itemPrice

	# missing: use curl/wget to download the image for each item too, using itemImageURL
