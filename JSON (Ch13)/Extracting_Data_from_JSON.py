#http://py4e-data.dr-chuck.net/comments_42.json
#http://py4e-data.dr-chuck.net/comments_1263664.json

import urllib.request, urllib.parse, urllib.error
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    url = input('Enter location: ')
    if len(url) < 1:
        break

    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)

    data = uh.read()
    print('Retrieved', len(data), 'characters')

    info = json.loads(data)
    print('Count:', len(info['comments']))

    sum = 0
    for item in info['comments']:
        sum += int(item['count'])

    print('Sum:', sum)
