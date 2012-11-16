#!/usr/bin/env python

import sys
from xmlutil import get_text, findall, find, tostring
from address import Address

def list_to_ship(sdate, edate):
    import api
    page_number = 1
    total_pages = 1

    addresses = {}
    item_to_address = {}
    item_address_to_quantity = {}

    total_transactions = 0
    total_outstanding = 0
    
    # get items sold
    while page_number <= total_pages:
        print 'getting page', page_number

        response = api.GetSellerTransactions(sdate,edate,page_number)
        total_pages = int(get_text(response, 'TotalNumberOfPages'))

        transactions = findall(response, 'Transaction')
        for i, transaction in enumerate(transactions):
            item_id = get_text(transaction, 'ItemID')
            paid = get_text(transaction, 'PaidTime')
            shipped = get_text(transaction, 'ShippedTime')
            print i, paid, shipped, 'search.ebay.com/%s' % item_id, 
            buyer = find(transaction, 'BuyerInfo')
            shipping = find(buyer, 'ShippingAddress')
            address = Address(shipping)
            if paid and not shipped:
                item_to_address.setdefault(item_id,[]).append(str(address))
                item_address_to_quantity[(item_id, str(address))] = get_text(transaction, 'QuantityPurchased')
                total_outstanding += 1
                print "added"
            else:
                print "not added"
            total_transactions += 1
            
        page_number += 1
    

    # get item titles
    item_responses = api.GetMultipleItems(item_to_address.keys())
    for item_response in item_responses:
        items = findall(item_response, 'Item')
        for item in items:
            item_id = get_text(item, 'ItemID')
            title = get_text(item, 'Title')
            print item_id, title
            addresslist = item_to_address[item_id]
            for address in addresslist:
                quantity = int(item_address_to_quantity[(item_id, address)])
                for x in range(quantity):
                    addresses.setdefault(address, []).append(title)

    """
    # get item titles the slow way
    for i, item_id in enumerate(item_to_address):
        print "looking up item", i
        iresp = api.GetItem(item_id)
        title = get_text(iresp, 'Title')
        address = item_to_address[item_id]
        addresses.setdefault(address, []).append(title)
    """

    #item_response = api.VerifyRelistItem(190172364325)
    #items = findall(item_response, 'Item')
    #for item in items:
    #      print item
    
    return addresses, total_transactions, total_outstanding

        
if __name__ == "__main__":
    print len(list_to_ship('2008-01-25', '2008-02-14'))

    
