#!/usr/bin/python

import re
import sys
import json
import requests
import urlparse
from pprint import pprint
from requests.auth import HTTPBasicAuth
from operator import itemgetter
from datetime import datetime
import configparser
config = configparser.ConfigParser()
config.read('GHG')
print config.sections()

today = datetime.now()
log_file ="D:\GHG\PrivateRepoCheck\PrivateRepoCheck_log_{0}.txt".format(today.strftime('%Y%m%d'))
url1 ='https://api.github.com/orgs/{0}/repos?page=1&per_page=100'.format(config["GitHub"]["org"])
respo1= requests.get(url1, auth=HTTPBasicAuth(config['GitHub']['username'], config['GitHub']['password']),verify = False)
print respo1
link = respo1.headers.get('link', None)
if link:
	f = re.findall('<(.+?)>', link)
	for ij in f:
		print ij
		par = urlparse.parse_qs(urlparse.urlparse(ij).query)
	n=par['page']
else:
	n=0
#print respo.json()
mylist=[]
mydates=[]
exclusion_list = []
data='{"private": "true"}'
#data_file = json.load(respo.json())
if n!=0:
	for ig in range(1,int(n[0])+1):
		print int(n[0])
		url = 'https://api.github.com/orgs/{0}/repos?page={1}&per_page=100'.format(config["GitHub"]["org"],ig)
		response = requests.get(url, auth=HTTPBasicAuth(config['GitHub']['username'], config['GitHub']['password']),verify = False)
		print "public repos:"
		for i in  response.json():
			if i["name"] not in exclusion_list:
				if (i['private'] ==False):
					print i['name']
					url1 ='https://api.github.com/repos/{0}/{1}'.format(config["GitHub"]["org"],i['name'])
					respo1= requests.patch(url1, data=data, auth = HTTPBasicAuth(config['GitHub']['username'], config['GitHub']['password']))
					print respo1
					mylist.append(i['name'])
else:
	url = 'https://api.github.com/orgs/{0}/repos?page={1}&per_page=100'.format(config["GitHub"]["org"],n)
        response = requests.get(url, auth=HTTPBasicAuth(config['GitHub']['username'], config['GitHub']['password']),verify = False)
        print "public repos:"
        for i in  response.json():
		if i["name"] not in exclusion_list:
	                if (i['private'] ==False):
						print i['name']
						url1 ='https://api.github.com/repos/{0}/{1}'.format(config["GitHub"]["org"],i['name'])
						respo1= requests.patch(url1, data=data, auth = HTTPBasicAuth(config['GitHub']['username'], config['GitHub']['password']))
						print respo1
                    	mylist.append(i['name'])
print mylist			
with open(log_file,"a") as l:
	l.write(str(mylist)+"\t"+str(today)+"\n")
