#!/usr/bin/env python

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element, SubElement
import xml.etree.ElementTree as etree
import requests
import cgi
import cgitb
import time
import re

#cgitb.enable(display=0, logdir="/var/log/messages")


def getvlan(): 

        form = cgi.FieldStorage() 
        vlanep = form.getvalue('vlan_ep') 
        return vlanep 

vlanep = getvlan()

def getlist():

        form = cgi.FieldStorage()
        bulkep = form.getvalue('mac_ep')
	bulkepsplit = bulkep.split('\r\n')
	bulkeplist=[]
	for i in bulkepsplit:
		bulkeplist.append(i)
        root=Element('ns4:endpointBulkRequest')
        tree=ElementTree(root)
        root.set('operationType', 'create')
        root.set('resourceMediaType', 'vnd.com.cisco.ise.identity.endpoint.1.0+xml')
        root.set('xmlns:ns6', 'sxp.ers.ise.cisco.com')
        root.set('xmlns:ns5', 'trustsec.ers.ise.cisco.com')
        root.set('xmlns:ns7', 'network.ers.ise.cisco.com')
        root.set('xmlns:xs', 'http://www.w3.org/2001/XMLSchema')
        root.set('xmlns:ns4', 'identity.ers.ise.cisco.com')
        rlist=SubElement(root, 'ns4:resourcesList')
	for x in bulkeplist:
        	endpoint=SubElement(rlist, 'ns4:endpoint')
        	groupId=SubElement(endpoint, 'groupId')
        	groupId.text=vlanep
        	mac=SubElement(endpoint, 'mac')
        	mac.text=str(x)
        	staticGroupAssignment=SubElement(endpoint, 'staticGroupAssignment')
        	staticGroupAssignment.text='true'
        	staticProfileAssignment=SubElement(endpoint, 'staticProfileAssignment')
        	staticProfileAssignment.text='false'
        #print etree.tostring(root, encoding="UTF-8")
        mystring=etree.tostring(root, encoding="UTF-8")
        return mystring

xml = getlist()

def putdata():

	url = "https://ise-admin-tc.xxxx.edu:9060/ers/config/endpoint/bulk/submit"

	payload = xml
	headers = {
   	'accept': "application/vnd.com.cisco.ise.identity.endpointbulkrequest.1.0+xml",
    	'content-type': "application/vnd.com.cisco.ise.identity.endpointbulkrequest.1.0+xml",
    	'authorization': "Basic aG9zcGl0YWxhZG1pbjpMZXRzMjAxMndhKw==",
    	'cache-control': "no-cache",
    	}

	response = requests.request("PUT", url, data=payload, headers=headers, verify=False, allow_redirects=True)
	bulkid = response.headers.get('Location')
	bulkreg = re.match('.*?([0-9]+)$', bulkid).group(1)
	return bulkreg
	


bulkidfinal = putdata()

def getstatus():

	time.sleep(10) #seconds

	urlone = "https://ise-admin-tc.xxxxx.edu:9060/ers/config/endpoint/bulk/"
	url = urlone + bulkidfinal

	headers = {
   	'content-type': "application/vnd.com.cisco.ise.ers.bulkStatus.1.0+xml",
    	'accept': "application/vnd.com.cisco.ise.identity.bulkStatus.1.0+xml",
    	'authorization': "Basic aG9zcGl0YWxhZG1pbjpMZXRzMjAxMndhKw==",
	'cache-control': "no-cache",
	}

	response = requests.request("GET", url, headers=headers, verify=False)
	#return response.text
        tree=etree.fromstring(response.text)
	for c in tree.findall('{ers.ise.cisco.com}resourcesStatus/{ers.ise.cisco.com}resourceStatus'):
		cause = c.get('rootCause')
		status = c.get('status')
		return cause,status	




msg = getstatus()

print "Content-type:text/html\n"
print ""

print '<html>'
print '<title>'
print 'Response'
print '</title>'
print '<body>'
print '<h1><p>Server Response:<p></h1>'
print '<pre>'
print (msg)
print '</pre>'
print '</body>'
print '</html>'

