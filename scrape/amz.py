import urllib2
import lxml
from lxml.html import parse

USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
BASE_URL="http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="
keywords = []

def getOpener():
	h = urllib2.HTTPHandler(debuglevel=1)
	opener = urllib2.build_opener(h)	
	return opener

def getTagValue(el, path):
	print "tag value"

def readKeywords(filename):
	print "reading keywords file"
	with open(filename) as fp:
		for line in fp.readlines():
			keywords.append(line.strip())

def main():
	print "scraping"
	for terms in keywords:
		request = urllib2.Request(BASE_URL+terms)
		request.add_header('User-Agent', USER_AGENT)
		fd = getOpener.open(request)
		doc = parse(fd).getroot()
		product_row = lxml.etree.XPath("//div[@id=$clname]")
		for count in range(0,20):
			div_name = "result_" + str(count)
			for el in product_row(doc, clname = div_name):
				print "processing row is {}".format(count)
				title= el.xpath(".//h3[@class='newaps']/a/span[@class='lrg bold']")[0]
				bestseller=el.xpath(".//span[@class='left bsbSprite']/span[@class='rank']/span")[0]
				print title.text
				print bestseller.text
				print "+++++++++++++++++++++++++++++++++++++++"

readKeywords("keywords.txt")
print keywords

	#//*[@id="result_0"]/ul[2]/li[2]/div/a/span[1]/span[1]/span[3]/text()[2]