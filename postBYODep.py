#!/usr/bin/env python

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element, SubElement
import xml.etree.ElementTree as etree
import requests
import cgi
import cgitb
import time
import pprint
import re


#cgitb.enable(display=0, logdir="/var/log/messages")

#def getvlan(): 
#
#        form = cgi.FieldStorage() 
#        vlanep = form.getvalue('vlan_ep') 
#        return vlanep 

vlanep = 'xxx'

def getlist():

        form = cgi.FieldStorage()
        bulkep = form.getvalue('mac_ep')
	bulkepsplit = bulkep.split('\r\n')
	bulkeplist=[]
	for i in bulkepsplit:
		bulkeplist.append(i)
	subeplist=[]
	submaillist=[]
	subep = [ i.split(',')[0] for i in bulkeplist ] 
	submail = [ p.split(',')[1] for p in bulkeplist ]
	for epx in subep:
		subeplist.append(epx)
	for mail in submail:
		submaillist.append(mail) 
        root=Element('ns4:endpointBulkRequest')
        tree=ElementTree(root)
        root.set('operationType', 'register')
        root.set('resourceMediaType', 'vnd.com.cisco.ise.identity.endpoint.1.0+xml')
        root.set('xmlns:ns6', 'sxp.ers.ise.cisco.com')
        root.set('xmlns:ns5', 'trustsec.ers.ise.cisco.com')
        root.set('xmlns:ns7', 'network.ers.ise.cisco.com')
        root.set('xmlns:xs', 'http://www.w3.org/2001/XMLSchema')
        root.set('xmlns:ns4', 'identity.ers.ise.cisco.com')
        rlist=SubElement(root, 'ns4:resourcesList')
	for t in zip(subeplist):
        	endpoint=SubElement(rlist, 'ns4:endpoint')
#		endpoint.set('description', str(x))
        	groupId=SubElement(endpoint, 'groupId')
        	groupId.text=vlanep
        	mac=SubElement(endpoint, 'mac')
        	mac.text = str(t)
        	staticGroupAssignment=SubElement(endpoint, 'staticGroupAssignment')
        	staticGroupAssignment.text='true'
        	staticProfileAssignment=SubElement(endpoint, 'staticProfileAssignment')
        	staticProfileAssignment.text='false'
        #print etree.tostring(root, encoding="UTF-8")
        mystring=etree.tostring(root, encoding="UTF-8")
        return mystring

xml = getlist()

def putdata():

	url = "https://xxxx:9060/ers/config/endpoint/bulk/submit"

	payload = xml
	headers = {
   	'accept': "application/vnd.com.cisco.ise.identity.endpointbulkrequest.1.0+xml",
    	'content-type': "application/vnd.com.cisco.ise.identity.endpointbulkrequest.1.0+xml",
    	'authorization': "Basic xxxxxx",
    	'cache-control': "no-cache",
    	}

	response = requests.request("PUT", url, data=payload, headers=headers, verify=False, allow_redirects=True)
	bulkid = response.headers.get('Location')
	bulkreg = re.match('.*?([0-9]+)$', bulkid).group(1)
	return bulkreg
	


bulkidfinal = putdata()

def getstatus():

	time.sleep(5) #seconds

	urlone = "https://xxxxx:9060/ers/config/endpoint/bulk/"
	url = urlone + bulkidfinal

	headers = {
   	'content-type': "application/vnd.com.cisco.ise.ers.bulkStatus.1.0+xml",
    	'accept': "application/vnd.com.cisco.ise.identity.bulkStatus.1.0+xml",
    	'authorization': "Basic xxxxxx",
	'cache-control': "no-cache",
	}

	response = requests.request("GET", url, headers=headers, verify=False)
	#return response.text
        tree=etree.fromstring(response.text)
	#return tree
	cause=[]
	for c in tree.getiterator('{ers.ise.cisco.com}resourceStatus'):
		cause.append(c.attrib)
	return cause





msg = getstatus()

print "Content-type:text/html\n"
print ""

print '<html>'
print '<head>'
print '<script>'
print 'function goBack() {'
print '	window.history.back()'
print '}'
print '</script>'
print '</head>'
print '<title>'
print 'Response'
print '</title>'
print '<body>'
print '<h1><p>Server Response:<p></h1>'
print '<pre>'
pprint.pprint(msg)
print '</pre>'
print '<button onclick="goBack()">'
print 'Back'
print '</button>'
print '</body>'
print '</html>'

if __name__ == '__main__':
    list=500
    log=setupLogging(debug=True,quiet=False)
    pp=pprint.PrettyPrinter()
    message=': program starting'
    log.info(message)
    conn=getstatus()
    log.info(conn)
    bulkidsubmit='Submitted BULKID '+putdata()
    log.info(bulkidsubmit)

