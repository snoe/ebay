import httplib
import xml.etree.ElementTree as ET
from xmlutil import findall, find, get_text
import config

def buildHttpHeaders(action):
    httpHeaders = {"X-EBAY-API-COMPATIBILITY-LEVEL": config.version,	
               "X-EBAY-API-DEV-NAME": config.devID,
               "X-EBAY-API-APP-NAME": config.appID,
               "X-EBAY-API-CERT-NAME": config.certID,
               "X-EBAY-API-CALL-NAME": action,
               "X-EBAY-API-SITEID": config.siteID,
               "X-EBAY-API-VERSION": config.version,
               "Content-Type": "text/xml"}
    return httpHeaders

def buildShoppingHttpHeaders(action):
    httpHeaders = {
               "X-EBAY-API-CALL-NAME": action,
               "X-EBAY-API-APP-ID": config.appID,
               "X-EBAY-API-VERSION": config.version,
               "X-EBAY-API-SITE-ID": config.siteID,
               "X-EBAY-API-REQUEST-ENCODING": "XML",
               "Content-Type": "text/xml"}
    return httpHeaders

def GetSellerTransactions(sdate,edate,page_number="1"):
    action = "GetSellerTransactions"
    headers = buildHttpHeaders(action)
    body = """<?xml version='1.0' encoding='utf-8'?>
    <%s xmlns=\"urn:ebay:apis:eBLBaseComponents\">
    <RequesterCredentials><eBayAuthToken>%s</eBayAuthToken></RequesterCredentials>
    <ModTimeFrom>%s</ModTimeFrom>
    <ModTimeTo>%s</ModTimeTo>
    <Pagination>
        <EntriesPerPage>200</EntriesPerPage>
        <PageNumber>%s</PageNumber>
    </Pagination>
    </%s>""" % (action, config.userToken, sdate, edate, page_number, action)
    
    return send_request(headers, body)

def GetItem(item_id):
    action = "GetItem"
    headers = buildHttpHeaders(action)
    body = """<?xml version='1.0' encoding='utf-8'?>
    <%s xmlns=\"urn:ebay:apis:eBLBaseComponents\">
    <RequesterCredentials><eBayAuthToken>%s</eBayAuthToken></RequesterCredentials>
    <ItemID>%s</ItemID>
    </%s>""" % (action, config.userToken, item_id, action)

    return send_request(headers, body)

def VerifyRelistItem(item_id):
    item = GetItem(item_id)
    print item

def GetMultipleItems(item_ids):
    responses = []
    for i in range(0, len(item_ids), 10):
        subset = item_ids[i:i+10]
        action = "GetMultipleItems"
        headers = buildShoppingHttpHeaders(action)
        body = """<?xml version='1.0' encoding='utf-8'?>
        <%s xmlns=\"urn:ebay:apis:eBLBaseComponents\">""" % (action)

        for item_id in subset:
            body += "<ItemID>%s</ItemID>\n" % item_id 

        body += "</%s>" % (action)

        root = send_request(headers, body, config.shoppingUrl, config.shoppingDir)
        responses.append(root)
    return responses


def send_request(headers, body, rurl=config.serverUrl, rdir=config.serverDir):
    # specify the connection to the eBay Sandbox environment
    if rurl.startswith('open'):
        connection = httplib.HTTPConnection(rurl)
    else:
        connection = httplib.HTTPSConnection(rurl)

    # specify a POST with the results of generateHeaders and generateRequest
    connection.request("POST", rdir, body, headers)
    response = connection.getresponse()

    # if response was unsuccessful, output message
    data = response.read()
    if response.status != 200:
        raise Exception("%s %s %s: %s %s" % (rurl, rdir, response.status, response.reason, data))

    # store the response data and close the connection
    connection.close()

    # check for any Errors
    root = ET.fromstring(data)
    errors = findall(root, 'Errors')
    error_list = []
    for error in errors:
        d = ApiErrorData(error)
        error_list.append("%s: %s\n\t%s" % (d.code, d.short, d.detail))
        
    if error_list:
        raise Exception("\n".join(error_list))

    if not rurl.startswith('open'):
        try:
            f = open('out.txt','wb')
            f.write(data)
            f.close()
        except IOError:
            pass
            
    
    return root

class ApiErrorData(object):
    def __init__(self, node):
        self.code = get_text(node, "ErrorCode")
        self.short = get_text(node, "ShortMessage")
        self.detail = get_text(node, "LongMessage")
