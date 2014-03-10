import urllib2
import lxml
from lxml.html import parse

USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
BASE_URL="http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="
PRODUCT_ROW_CLASS=lxml.etree.XPath("//div[@class='rslt prod celwidget' or @class='fstRow prod celwidget']")
TITLE_TAG =".//h3[@class='newaps']/a/span[@class='lrg bold']/text()"
OLD_PRICE=".//del[@class='grey']/text()"
NEW_PRICE=".//span[@class='bld lrg red']/text()"
PRIME=".//span[@class='srSprite sprPrime']"
CAT=".//span[@class='bold orng']/text()"
STAR5=".//span[@class='srSprite spr_stars5Active newStars']"
STAR45=".//span[@class='srSprite spr_stars4_5Active newStars']"
STAR4=".//span[@class='srSprite spr_stars4Active newStars']"
STAR35=".//span[@class='srSprite spr_stars3_5Active newStars']"
STAR3=".//span[@class='srSprite spr_stars3Active newStars']"
STAR25=".//span[@class='srSprite spr_stars2_5Active newStars']"
STAR2=".//span[@class='srSprite spr_stars2Active newStars']"
REVIEW_COUNT=".//span[@class='rvwCnt']/a/text()"
keywords = []

def getOpener():
	h = urllib2.HTTPHandler(debuglevel=1)
	opener = urllib2.build_opener(h)	
	return opener

def getTagValue(el, path):
	try:
		tag_value = el.xpath(path)[0]
	except:
		tag_value ="N/A"
	return tag_value

def isTagExists(el, path):
	if el.find(path) is not None:
		return True
	else:
		return False

def ratingsStars(el):
	if isTagExists(el, STAR5):
		return str(5)
	elif isTagExists(el, STAR45):
		return str(4.5)
	elif isTagExists(el, STAR4):
		return str(4)
	elif isTagExists(el, STAR35):
		return str(3.5)
	elif isTagExists(el, STAR3):
		return str(3)
	elif isTagExists(el, STAR25):
		return str(2.5)
	elif isTagExists(el, STAR2):
		return str(2)
	else:
		return str(0)

def readKeywords(filename):
	print "reading keywords file"
	with open(filename) as fp:
		for line in fp.readlines():
			keywords.append(line.strip())

def main():
	print "scraping"
	readKeywords("keywords.txt")
	with open("amz_results.txt", "w") as out:
		for terms in keywords:
			request = urllib2.Request(BASE_URL+terms)
			request.add_header('User-Agent', USER_AGENT)
			fd = getOpener().open(request)
			doc = parse(fd).getroot()
			
			for el in PRODUCT_ROW_CLASS(doc):
				title= getTagValue(el, TITLE_TAG)
				old_price=getTagValue(el, OLD_PRICE)
				new_price=getTagValue(el, NEW_PRICE)
				prime= "Prime" if isTagExists(el, PRIME) else "Non Prime"
				category=getTagValue(el, CAT)[:-1]
				ratingsstars=ratingsStars(el)
				reviewcount=getTagValue(el, REVIEW_COUNT)
				out.write(terms)
				out.write("|")
				out.write(title)
				out.write("|")
				out.write(old_price)
				out.write("|")
				out.write(new_price)
				out.write("|")
				out.write(prime)
				out.write("|")
				out.write(category)
				out.write("|")
				out.write(ratingsstars)
				out.write("|")
				out.write(reviewcount)
				out.write("\n")


#readKeywords("keywords.txt")
#print keywords
main()
