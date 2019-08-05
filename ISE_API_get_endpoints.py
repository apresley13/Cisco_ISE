#!/usr/bin/env python
import requests
import json
import xml.etree.ElementTree as ET
import pprint 
import warnings
import re
#warnings.filterwarnings("ignore")
total_re=re.compile('total="(\d+)')
r=requests.get('https://ise-test-tc.x.edu:9060/ers/config/endpointgroup?size=100',\
               auth=('xxxxxx','xxxxxx'),\
               headers={'Accept':'application/json'},\
               verify=False)
#print r.content
result_g=(r.content)
#print (result_g)
groups=[]
endpoints=[]
result_grp=json.loads(result_g)
for i in result_grp['SearchResult']['resources']:
    groups.append(i['id'])
#    return groups
#print (groups)
url = "https://ise-test-tc.x.edu:9060/ers/config/endpoint"
for x in groups:
    querystring = {"filter":"groupId.EQ."+str(x)}
    rtwo=requests.get(url,\
                auth=('xxxxx','xxxxxxxx'),\
                headers={'Accept':'application/json'},\
                params=querystring,\
                verify=False)
    results_e=(rtwo.content)
    results_ep=json.loads(results_e)
    for ep in results_ep['SearchResult']['resources']:
        endpoints.append(ep['mac'])
#    endpointstuff=[ep.split(',') for ep in endpoints] 

for i in endpoints:
    print i, endpoints[i]
