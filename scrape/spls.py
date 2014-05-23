import mechanize
import cookielib
import urllib
import lxml
from lxml.html import parse
import re
import traceback

PRODUCT_ROW_CLASS=lxml.etree.XPath("//*[@id=\"productDetail\"]/li[@class=\"prd\"]")
pathForPageNameMeta="//meta[@name=\"PageName\"]"
pathForItemNumber=".//div[@class=\"item\"]/text()"
pathForModelNumber=".//div[@class=\"model\"]/text()"
pathForProductName=".//div[@class=\"name\"]/h3/a/text()"
BASE_URL="http://3day.staples.com/"
keywords=[]

def getBrowser():

	br=mechanize.Browser()
	# Cookie Jar
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)
	ck = cookielib.Cookie(version=0, name='zipcode', value='02421', port=None, port_specified=False, domain='3day.staples.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
	cj.set_cookie(ck)

	# Browser options
	br.set_handle_equiv(True)
	#br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)

	# Follows refresh 0 but not hangs on refresh > 0
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

	return br


def getTagValue(el, path):
	try:
		tag_value = el.xpath(path)[0]
	except:
		tag_value ="N/A"
	return tag_value

def readKeywords(filename):
	print "reading keywords file"
	with open(filename) as fp:
		for line in fp.readlines():
			keywords.append(line.strip())

def searchTerm(term):
    term=urllib.quote(term, safe='"~()*.')
    term=term.replace("%25", "%2525")
    term=term.replace("%2F", "%252F")
    term=term.replace("(", "%2528")
    term=term.replace(")", "%2529")
    term=term.replace("%2B", "%252B")
    term=term.replace("%20", "+")
    return term

def searchKey(term):
    searchKey = re.sub(r'[^a-zA-Z0-9]+', '+', term)
    if searchKey[0]=="+": searchKey= searchKey[1:]
    lastPos=len(searchKey)-1
    if searchKey[lastPos]=="+": searchKey = searchKey[0:-1]
    return searchKey
	
def main():
	print "scraping"
	readKeywords("Autocomplete.txt")
	br=getBrowser()
	with open("Autocomplete_results.txt", "a") as out:
		for terms in keywords:
			print terms
			try:
				sKey=sTerm=terms
				query_param=searchKey(sKey) + "/directory_" + searchTerm(sTerm)
				resp=br.open(BASE_URL+query_param)
				body=parse(resp)
				page_name=getTagValue(body, pathForPageNameMeta)
				if ( page_name == "N/A"):
					out.write(terms)
					out.write("|")
					out.write("Unknown page")
					out.write("\n")
				elif ( page_name.get('content') == "searchnoresults"):
					out.write(terms)
					out.write("|")
					out.write("no results")
					out.write("\n")
				elif ( page_name.get('content') == "searchresults"):
					for el in PRODUCT_ROW_CLASS(body):
						item=getTagValue(el, pathForItemNumber).replace("Item ", "")
						model=getTagValue(el, pathForModelNumber).replace("Model ", "")
						out.write(terms)
						out.write("|")
						out.write(item)
						out.write("|")
						out.write(model)
						out.write("|")
						out.write(getTagValue(el, pathForProductName).encode('UTF-8'))
						out.write("\n")
				else:
					out.write(terms)
					out.write("|")
					out.write(page_name.get('content'))
					out.write("\n")
			except Exception, e:
				print "exception"
				print traceback.format_exc()
				out.write(terms)
				out.write("|")
				out.write("errored")
				out.write("\n")
			
#readKeywords("keywords.txt")
#print keywords
main()
