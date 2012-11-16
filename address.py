from xmlutil import get_text

class Address:
    def __init__(self, shipping):
        self.to = get_text(shipping, 'Name')
        self.street1 = get_text(shipping, 'Street1')
        self.street2 = get_text(shipping, 'Street2')
        self.city = get_text(shipping, 'CityName')
        self.province = get_text(shipping, 'StateOrProvince')
        self.postalcode = get_text(shipping, 'PostalCode')
        self.country = get_text(shipping, 'CountryName')

    def html(self):
        return str(self).replace('\n','<br>')

    def __str__(self):
        args = self.__dict__
        address = "%(to)s"
        if self.street1:
            address += "\n%(street1)s"
        if self.street2:
            address += "\n%(street2)s"
        address += "\n%(city)s,%(province)s  %(postalcode)s"
        if self.country:
            address += "\n%(country)s"
        return address % args
