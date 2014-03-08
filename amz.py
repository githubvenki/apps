import urllib2
import lxml
from lxml.html import parse
URL="http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=paper"
h = urllib2.HTTPHandler(debuglevel=1)
opener = urllib2.build_opener(h)
request = urllib2.Request(URL)
request.add_header('User-Agent',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
fd = opener.open(request)
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
	

	#//*[@id="result_0"]/ul[2]/li[2]/div/a/span[1]/span[1]/span[3]/text()[2]