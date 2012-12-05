#!/usr/bin/env python

# Scrape some info from Fancy

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

# Process each item, downloading image
templateVariables = {}
for i, item in enumerate(items):
    itemName = 'item%d' % (i + 1)  # Start names at 1 instead of zero
    templateVariables[itemName] = item
    print 'Downloading image %s...' % item['imageUrl'],
    webImage = urllib2.urlopen(item['imageUrl'])
    # TODO: confirm that webImage.info().getmaintype() is 'image'
    extension = webImage.info().getsubtype()
    imageFilename = '%s.%s' % (itemName, extension)
    item['imageFilename'] = imageFilename
    imageFile = file('images/%s' % imageFilename, 'w+b')
    imageFile.write(webImage.read())
    print 'done.'
    imageFile.close()

output = template.render(items=items, **templateVariables)
file(options.output, 'w').write(output)
