import xml.etree.ElementTree as ET

_NS = "urn:ebay:apis:eBLBaseComponents"
def ns(value):
    return ".//{%s}%s" % (_NS, value)

def findall(node, value):
    return node.findall(ns(value))

def find(node, value):
    return node.find(ns(value))

def get_text(node, value):
    if node:
        x = node.find(ns(value))
        if x != None and x.text != None and x.text != 'None':
            return x.text.encode('utf8')

    return None

def tostring(node):
    return ET.tostring(node)
