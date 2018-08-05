#!/usr/bin/python
import re
import sys
import json
import requests
import urlparse
from pprint import pprint
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPBasicAuth
from datetime import datetime 
from email.mime.text import MIMEText
from email.mime.message import MIMEMessage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import boto.ses
import os
import sys
from operator import itemgetter
from datetime import datetime
today = datetime.now()
import configparser
config = configparser.ConfigParser()
config.read('GHG')
print config.sections()
conn = boto.ses.connect_to_region(config['AWS-SES']['region'], aws_access_key_id=config['AWS-SES']['aws_access_key_id'], aws_secret_access_key=config['AWS-SES']['aws_secret_access_key'])

print conn.list_verified_email_addresses()

msg = MIMEMultipart()
msg['From'] = "DILEP<Dileep.Gukada@company.com>"
msg['Subject'] = 'Github access removal -{0}'.format(today)
log_file ="/migration/OutsideCollaboratorsCheck_log_{0}.txt".format(today.strftime('%Y%m%d'))
url1 ='https://api.github.com/orgs/{0}/outside_collaborators?page=1&per_page=100'.format(config["GitHub"]["org"])
respo1= requests.get(url1, auth=HTTPBasicAuth(config['GitHub']['username'], config['GitHub']['password']),verify = False)
link = respo1.headers.get('link', None)
#print [i.split('rel="next"') for i in link]
print link
print respo1.json()
exc_mlist=[]
ff=[]
for ig in respo1.json():
	print ig["login"]
	if ig["login"] not in exc_mlist:
		#print ig["login"]
		ff.append(ig["login"])
		url12 = "https://api.github.com/orgs/{0}/outside_collaborators/{1}".format(config["GitHub"]["org"],ig["login"])
		requests.delete(url12, auth= HTTPBasicAuth(config['GitHub']['username'], config['GitHub']['password']),verify = False)	
with open(log_file,"a") as l:
	l.write(str(ff)+"\t"+str(today)+"\n")

if ff:
	
	with open(log_file,"r") as t:
		part1 = t.read()


	part = 'This email has outside collaborators removed today-{0}'.format(today)
	part2 = part + "\n" + "\n" +part1
	part2 = MIMEText(part2)  
	#print part2
	#part3.add_header('Content-Disposition', 'attachment', filename='new_urls')
	msg.attach(part2)
	#msg['Subject'] = 'Howdy! -- Please find the outside collaborators removed today-{0}'.format(today)
	
	msg['To'] = 'Dikep.gukada@company.com'
	msg['Cc'] = 'Dikep.Gukada@company.com'
	msg['body'] = 'Howdy! -- Please find the outside collaborators removed today-{0}'.format(today)
	result = conn.send_raw_email(msg.as_string(), source=msg['From'] , destinations=[msg['To'],msg['Cc']])
	print result
