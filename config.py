import ConfigParser

# open config file
config = ConfigParser.ConfigParser()
config.read("/home/snoe/scripts/ebay/prod.ini")

# specify eBay API dev,app,cert IDs
devID = config.get("Keys", "Developer")
appID = config.get("Keys", "Application")
certID = config.get("Keys", "Certificate")

#get the server details from the config file
serverUrl = config.get("Server", "URL")
serverDir = config.get("Server", "Directory")
shoppingDir = config.get("Server", "ShoppingDir")
shoppingUrl = config.get("Server", "ShoppingURL")

# specify eBay token
# note that eBay requires encrypted storage of user data
userToken = config.get("Authentication", "Token")


#eBay Call Variables
#siteID specifies the eBay international site to associate the call with
#0 = US, 2 = Canada, 3 = UK, ....
siteID = "0"

#The API level that the application conforms to
version = "527"
