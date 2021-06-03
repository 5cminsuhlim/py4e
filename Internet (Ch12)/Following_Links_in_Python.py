#http://py4e-data.dr-chuck.net/known_by_Fikret.html
#http://py4e-data.dr-chuck.net/known_by_Fion.html

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter URL: ')
count = int(input('Enter count: '))
pos = int(input('Enter position: '))

while count >= 0:
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")
    tags = soup('a')
    #print initial input
    print(url)
    url = tags[pos - 1].get('href', None)
    count -= 1
