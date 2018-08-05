import re
import sys
import json
import requests
#import urlparse
from pprint import pprint
from requests.auth import HTTPBasicAuth
search_string = 'aws access key id'
token = ""
cmdargs = str(sys.argv)
url = "https://api.github.com/search/code?q={0}+in:file+user:{1}+&per_page=100".format(search_string,config["GitHub"]["org"])
#print url
resp= requests.get(url, auth=HTTPBasicAuth(config['GitHub']['username'], config['GitHub']['password']), verify=False)
#print "json1:", resp.json()
#print resp.status_code
#print resp.text
print (resp.json())
with open('aws-key.json', 'w') as f:
	json.dump(resp.json(), f) 
with open('aws-key.json') as data:
	data_file = json.load(data)
#new_urls are the refined ones based on application stack(ex: java project, ruby on rails etc., )	
with open('new-aws-urls', 'w') as e:	
#"\git_test\htmls"	are the urls with false positives
	with open('aws-urls', 'w') as d:
		for i in data_file['items']:
  		#print i["html_url"]
  			
  			name = i['repository']['name']
  			name2 =""
   			#print name
  			d.write(name+'\n')
  			d.write(i["html_url"]+'\n'+'\n')
  				#re.search is looking for specific files with urls having cleartext passwords on the files with extensions xml, yml, netrc, config, rb 
  			if(re.search('\.(?:(?:yml$)|(?:json)|(?:env$)|(?:properties))', i["html_url"])):
  				#print i["html_url"]
  				e.write(name + "\n")
  				e.write(i["html_url"]+'\n'+'\n')
  				
  		    	
  		    	#print i["html_url"]
  			  	#name2 = i['repository']['name']
  		    	#print name2  								
  		    	
  			
  			#print i["html_url"]