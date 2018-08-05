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
from email.mime.text import MIMEText
from email.mime.message import MIMEMessage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import boto.ses
import os
import sys
from itertools import islice
from datetime import datetime
today = datetime.now()
#print conn.list_verified_email_addresses()
import configparser
config = configparser.ConfigParser()
#path to GHG config file
config.read('GHG')
print config.sections()
conn = boto.ses.connect_to_region(config['AWS-SES']['region'], aws_access_key_id=config['AWS-SES']['aws_access_key_id'], aws_secret_access_key=config['AWS-SES']['aws_secret_access_key'])
msg = MIMEMultipart()
#provide from address
msg['From'] = "DILEP<Dilep.Gurakada@company.com>"
msg['Subject'] = 'Github access removal -{0}'.format(today)
log_file ="MFACheck_log_{0}.txt".format(today.strftime('%Y%m%d'))
url = "https://api.github.com/orgs/{0}/members?filter=2fa_disabled&page=1&per_page=100".format(config["GitHub"]["org"])
respo= requests.get(url, auth=HTTPBasicAuth(config['GitHub']['username'], config['GitHub']['password']),verify = False)
#print respo.json()
#mtlist=[]
mlist=[]
link = respo.headers.get('link', None)
mtlist=[]
#print [i.split('rel="next"') for i in link]

for ig in respo.json():
	#print ig["login"]
	if ig["login"] not in mtlist:
		url = "https://api.github.com/orgs/{0}/members/{1}".format(config["GitHub"]["org"],ig["login"])
		requests.delete(url, auth=HTTPBasicAuth(config['GitHub']['username'], config['GitHub']['password']),verify = False)
		mlist.append(ig["login"])
	
# test for email:mlist.append()
if mlist:
	for i in mlist:
		#print i
		url12 = "https://api.github.com/users/{0}".format(i)
		respo12= requests.get(url12, auth=HTTPBasicAuth(config['GitHub']['username'], config['GitHub']['password']),verify = False)
		#print respo12.json()
		
		j = [respo12.json()]
		for i in j:
			#print i['email']
			part = "You have been removed from GHG organization for not having MFA Enabled-(Duo). Please ensure MFA is enabled to your account."
			part1= 'Please follow this wiki page for our GitHub security requirements to be added back and remain part of GHG organization in GitHub: github security requirements'
			part3= "Thanks,"+"\n" + "IT-Security-team,"+"\n"+"gg."
			part2 = part +"\n"+"\n"+part1+"\n"+"\n"+part3
			part2 = MIMEText(part2)  
			#print part2
			#part3.add_header('Content-Disposition', 'attachment', filename='new_urls')
			msg.attach(part2)
			
			
			msg['To'] = i['email']
			#provide any CC to the email sent out to the users
			msg['Cc'] = 'Dikep.Gukada@company.com'
			msg['body'] = 'Please follow the github requirements to be added back to our GitHub organization'
			result = conn.send_raw_email(msg.as_string(), source=msg['From'] , destinations=[msg['To'],msg['Cc']])
			print result
with open(log_file,"a") as l:
	l.write(str(mlist)+"\t"+str(today)+"\n")

