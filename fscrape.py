#!/usr/bin/env python

# Scrape some info from Fancy

import hashlib
import urllib2
import os.path
import optparse
from bs4 import BeautifulSoup
from jinja2 import Template

# Define command-line options
parser = optparse.OptionParser()
parser.add_option('-t', '--template', dest='template', default='template.html',
                  help='Template file to use')
parser.add_option('-o', '--output', dest='output', default='index.html',
                  help='Output file to use')
(options, args) = parser.parse_args()

# Load and compile template
template = Template(file(options.template).read())

# Make sure images/ dir exists
imagesDir = 'images'
if not os.path.exists('images'):
    os.mkdir('images')

# Process pages to populate items list
items = []
for url in file('urls.txt'):
    url = url.strip()
    print 'Processing page at %s' % url
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)

    items.append({
        'url': url,
        'title': soup.figcaption.string,
        'imageUrl': soup.find(class_='fig-image').img['src'],
        'price': soup.find(class_='price').string,
    })

# For each item, download image
for item in items:
    filename = hashlib.md5(item['imageUrl']).hexdigest()
    imagePath = 'images/%s' % filename
    item['imageFilename'] = filename
    if not os.path.exists(imagePath):
        webImage = urllib2.urlopen(item['imageUrl'])
        print 'Downloading image %s' % item['imageUrl']
        imageFile = file(imagePath, 'w+b')
        imageFile.write(webImage.read())
        imageFile.close()
    else:
        print 'Using previously saved image for %s' % item['imageUrl']

templateVariables = dict([('item%d' % (i + 1), item) for (i, item) in enumerate(items)])
output = template.render(items=items, **templateVariables)
file(options.output, 'w').write(output)
