#http://py4e-data.dr-chuck.net/comments_42.xml
#http://py4e-data.dr-chuck.net/comments_1263663.xml

import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter location: ')

print('Retrieving', url)
uh = urllib.request.urlopen(url, context=ctx)

data = uh.read()
print('Retrieved', len(data), 'characters')
tree = ET.fromstring(data)

counts = tree.findall('comments/comment')
print('Count:', len(counts))

sum = 0
for item in counts:
    sum += int(item.find('count').text)

print('Sum:', sum)
