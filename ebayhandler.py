from mod_python import apache
from mod_python import util
from datetime import datetime
from datetime import timedelta

import listsold

form = '''
<form method="get">
<table><tr>
  <td>Start Date (YYYY-MM-DD):</td>
  <td><input type="text" name="startdate" value="%s"></input></td>
  </tr><tr>
  <td>End Date (YYYY-MM-DD):</td>
  <td><input type="text" name="enddate" value="%s"></input></td>
</tr></table>
<input type="submit" name="submit" value="submit"/>
</form>
<hr>
Total transactions: %s<br>
Outstanding transactions: %s
<hr>
'''

def handler(req):
    req.content_type = 'text/html'
    df = "%Y-%m-%d"
    today = datetime.now().strftime(df)
    yesterday = (datetime.now() - timedelta(days=2)).strftime(df)

    fields = util.FieldStorage(req)
    sdatestr = fields.getfirst('startdate', yesterday).strip()
    #sdate = datetime.strptime(sdatestr, df)

    edatestr = fields.getfirst('enddate', today).strip()
    #edate = datetime.strptime(edatestr, df)

    # get the listings
    addresses, total, outstanding = listsold.list_to_ship(sdatestr,edatestr)


    req.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8">')
    
    req.write(form % (sdatestr, edatestr, total, outstanding))

    req.write('<table border="1">')
    for key in addresses:
        req.write('<tr><td><pre>')
        req.write(str(key))
        req.write('</pre></td><td>')
        for i, a in enumerate(addresses[key]):
            req.write("%s. %s" % (i+1,a))
            req.write('<br>')
        req.write('</td></tr>')
    req.write('</table>')
    return apache.OK
