import requests
import webcolors
from random import randint
from bs4 import BeautifulSoup
import time
import glob
import json

ZOVI_HTML_LOCATION = "C:\\Users\\unrao\\python\\art\\data\\"

def get_colors(description):
    '''
    Given a description of an item, this would extract the names of colors in the description 
    '''
	colors = webcolors.CSS3_NAMES_TO_HEX
	words = description.split()
	cols =[]
	for word in words:
		if word.lower() in colors:
			cols.append(word.lower())
	#print " ".join(cols)		
	return " ".join(cols)
	
def get_cat_dtls_zovi(li):
    '''
    Using the li element from the html files to extract it's datat
    '''
    dtl={}
    #print li.attrs['data-option']
    # to get prod_id
    #prod_id = li.find("li",{"class":"item ui-draggable"}).attrs['data-option']
    prod_id = li.attrs['data-option']
    # to get image url 
    img_url = "http:"+li.find("img").attrs['data-src']
    # to get description 
    desc = li.find("div",{"class":"pro_title"}).attrs['data-name']
    # get colors 
    color = get_colors(desc)
    
    href = li.find("a").attrs['href']
    print href
    # The below workaround to deal with artifacia AP 
    if(prod_id.startswith("A")):
		prod_id = randint(1000,100000)
        
    dtl['prodid'] = long(prod_id)
    dtl['url'] = img_url
    dtl['href'] =href
    
    dtl['style'] = desc.lower()
    dtl['color']  = color
    
    dtl['brand'] = "Zovi"
    #print dtl
    return dtl
	
details = []	


# Looping through all the html dumps of zovi products
for webpage in glob.glob(ZOVI_HTML_LOCATION+"*.html"):
	print len(details)
	print "Processing "+ webpage
	print webpage.split("\\")[-1].replace(".html","")
	category = webpage.split("\\")[-1].replace(".html","")
	soup = BeautifulSoup(open(webpage))
	catalog = soup.find("div", {"id": "catalog"})
	ul = catalog.find("ul",{"class":"catul"})
	for itm in ul.find_all('li',{"class":"item ui-draggable"}):
	    dtl = get_cat_dtls_zovi(itm)
	    dtl['category'] = category
	    details.append(dtl)
	
print len(details)	
	

# Writing JSON file in format required by artifacia	
data = {}
data['features']=["vr"]  # vr for visual recommendation , cpr for cross product recommendation
data['details'] = details


with open('zovi.json', 'w') as fp:
    json.dump(data, fp)
