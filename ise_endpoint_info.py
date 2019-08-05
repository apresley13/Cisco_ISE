#!/usr/bin/env python
#Andrew test
import requests
import json
import pprint 
import warnings
import re
warnings.filterwarnings("ignore")
endpoint=[]
endpointinfo=[]
r=requests.get('https://ise-test-tc.x.edu:9060/ers/config/endpoint?size=100',\
               auth=('x','x'),\
               headers={'Accept':'application/json'},\
               verify=False)

result_e=(r.content)
endpoint_r=json.loads(result_e)
num_pages = endpoint_r['SearchResult']['total']
#print (num_pages)

for j in endpoint_r['SearchResult']['resources']:
    endpoint.append(j['id'])
for page in range (2, num_pages/100+2):
#    print page
    rtwo=requests.get('https://ise-test-tc.x.edu:9060/ers/config/endpoint?size=100&page='+ str(page) ,\
        auth=('x','x'),\
        headers={'Accept':'application/json'},\
        verify=False)
    result_re=(rtwo.content)
    endpoint_re=json.loads(result_re)
    for x in endpoint_re['SearchResult']['resources']:
        endpoint.append(x['id'])
for i in endpoint:
    rthree=requests.get('https://ise-test-tc.x.edu:9060/ers/config/endpoint/'+str(i) ,\
        auth=('x','x'),\
        headers={'Accept':'application/json'},\
        verify=False)
    result_out=(rthree.content)
    outputr=json.loads(result_out)
    endpointmacid=(outputr['ERSEndPoint']['mac'], outputr['ERSEndPoint']['groupId'])
    endpointinfo.append(endpointmacid)
for y in endpointinfo:
    print y