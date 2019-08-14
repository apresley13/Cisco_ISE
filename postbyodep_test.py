#!/usr/bin/env python
##test BYOD tool to add Endpoints to BYOD endpoint group

import requests
import cgi
import cgitb
import json
import pprint 
import warnings
import re
from netaddr import *
#warnings.filterwarnings("ignore")

form = cgi.FieldStorage()
webinputep = form.getvalue('mac_ep')
webinputsplit = webinputep.split('\r\n')
webinputlist=[]
for w in webinputsplit:
    webinputlist.append(w)
vlanep = 'xxxxx'
print 'Content-type:text/html'
for webinput in webinputlist:
    if ',' in webinput:
        pass
    else:
        print ""

        print '<html>'
        print '<head>'
        print '</head>'
        print '<title>'
        print 'Response'
        print '</title>'
        print '<body>'
        print '<pre>'
        print'FAILED', 'Please make sure the data is comma seperated.'
        print '</pre>'
        print '</body>'
        print '</html>'
        break
subeplist=[]
submaillist=[]
endpoints=[]
endpointid=[]
subep = [ i.split(',')[0] for i in webinputlist ]
submail = [ p.split(',')[1] for p in webinputlist ]
for epx in subep:
	subeplist.append(epx)
for mail in submail:
    submaillist.append(mail)
#for mac in subeplist:
#    mac.dialect = netaddr.mac_unix_expanded
for t, x in zip(subeplist,submaillist):
    jdata = {"ERSEndPoint":{ "description": str(x), "mac": str(t), "staticGroupAssignment": True } }
    jdata_out = json.dumps(jdata, sort_keys=True, indent=True)
    payload = jdata_out
    url = "https://ise-test.blah.blah:9060/ers/config/endpoint/register"
    rheader = {
        'accept':"application/json",
        'content-type': "application/json",
        'authorization': "Basic xxxxxxxxxxxxxxx",
        'cache-control': "no-cache"
        }
    r = requests.request("PUT", url, data=payload, headers=rheader, verify=False)
    result_e=(r)
    if r.status_code == 204:
        pass
#        print('Success!')
    elif r.status_code == 500:
        print ""

        print '<html>'
        print '<head>'
        print '</head>'
        print '<title>'
        print 'Response'
        print '</title>'
        print '<body>'
        print '<pre>'
        print'FAILED', (result_e), 'please Check Data Format could be incorrect MAC address or EMAIL', str(t)
        print '</pre>'
        print '</body>'
        print '</html>'
    elif r.status_code == 400:
        print ""

        print '<html>'
        print '<head>'
        print '</head>'
        print '<title>'
        print 'Response'
        print '</title>'
        print '<body>'
        print '<pre>'
        print'FAILED', (result_e), 'please Check Data Format could be incorrect MAC address or EMAIL', str(t)
        print '</pre>'
        print '</body>'
        print '</html>'           
    else:
        print ""

        print '<html>'
        print '<head>'
        print '</head>'
        print '<title>'
        print 'Response'
        print '</title>'
        print '<body>'
        print '<pre>'
        print'FAILED', (result_e), str(t), 'please open ticket with Networking on call'
        print '</pre>'
        print '</body>'
        print '</html>'
    urlone = "https://ise-test.blah.blah:9060/ers/config/endpoint"
    querystring = {"filter":"mac.EQ."+str(t)}
    roneheader = {
        'Accept':'application/json',
        'Authorization': "Basic xxxxxxxxxxxxxxxxxxxxxxxx",
        'Cache-Control': "no-cache"
        }
    rone = requests.request("GET", urlone, headers=roneheader, params=querystring, verify=False)
    result_out=(rone.content)
    outputr=json.loads(result_out)
    for item in outputr['SearchResult']['resources']:
        endpointmacid=(item['id'])
        endpointid.append(endpointmacid)
for y in endpointid:
#    print y
    jupdate = {"ERSEndPoint":{ "groupId": vlanep, "staticGroupAssignment": True } }
    jupdate_out = json.dumps(jupdate, sort_keys=True, indent=True)
    payloadtwo = jupdate_out
    url = "https://ise-test.blah.blah:9060/ers/config/endpoint/"+str(y)
    rtwoheader = {
        'accept':"application/json",
        'content-type': "application/json",
        'authorization': "Basic xxxxxxxxxxxxxxxxxx",
        'cache-control': "no-cache"
        }
    rthree = requests.request("PUT", url, data=payloadtwo, headers=rtwoheader, verify=False)
#    result_ep=(rthree)
#    print (result_update)
    if rthree.status_code == 200:
        print ""

        print '<html>'
        print '<head>'
        print '</head>'
        print '<title>'
        print 'Response'
        print '</title>'
        print '<body>'
        print '<pre>'
        print'Success!', 'ENDPOINT ID', str(y)
        print '</pre>'
        print '</body>'
        print '</html>'
    else:
        print ""

        print '<html>'
        print '<head>'
        print '</head>'
        print '<title>'
        print 'Response'
        print '</title>'
        print '<body>'
        print '<pre>'
        print'FAILED!', (result_e), 'ENDPOINT ID', str(y), 'please open ticket with Networking on call'
        print '</pre>'
        print '</body>'
        print '</html>'