#https://www.marketwatch.com/tools/screener/short-interest

import sqlite3
import re
import urllib.error
import ssl
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('shortinterest.sqlite')
cur = conn.cursor()

#Creating SQL tables
cur.execute('''CREATE TABLE IF NOT EXISTS Stocks
    (symbol TEXT UNIQUE, company_name TEXT UNIQUE, price FLOAT,
     perc_change FLOAT, perc_short FLOAT, url TEXT UNIQUE)''')
conn.commit()


count = int(float(input('Enter desired # of most shorted stocks: ')))
url = 'https://www.marketwatch.com/tools/screener/short-interest'


#Attempt to access page info
print('Retrieving the most shorted stocks...')
try:
    document = urlopen(url, context = ctx)
    html = document.read()

    if document.getcode() != 200:
        print("Error on page: ", document.getcode())
    if 'text/html' != document.info().get_content_type() :
        print("Ignoring non-text/html page")

    soup = BeautifulSoup(html, "html.parser")
except:
    print("Unable to retrieve or parse page")

#Get table info
table = soup.find("table", {"class" : "table table--overflow align--right"})
rows = table.tbody.find_all("tr")

new_count = 0
update_count = 0

#Create list of stocks gathered thus far
name_list = list()
cur.execute('SELECT company_name FROM Stocks')
for ele in cur.fetchall():
    name_list.append(ele[0])
#print(name_list)

for row in rows:
    data = row.find_all('td')

    url = data[0].find('a').get('href', None)
    symbol = data[0].find('a').text
    company_name = data[1].find('div').text

    price = data[2].find('bg-quote').text
    price = float(price[1:])

    perc_change = data[3].find('bg-quote').text
    perc_change = float(perc_change.rsplit('%', 1)[0])

    perc_short = data[8].find('div').text
    perc_short = float(perc_short.rsplit('%', 1)[0])

    #print(symbol, company_name, price, perc_change, perc_short, url)

    #If there's a new stock in the top 50, insert
    #Else, update existing details
    if company_name not in name_list:
        new_count += 1
        cur.execute('''INSERT INTO Stocks (symbol, company_name, price,
            perc_change, perc_short, url) VALUES (?, ?, ?, ?, ?, ?)''',
            (symbol, company_name, price, perc_change, perc_short, url, ))
        conn.commit()
        print("NEW STOCK ADDED TO TOP 50:", company_name)
    else:
        cur.execute('SELECT * FROM Stocks WHERE symbol = ?', (symbol, ))
        info = cur.fetchone()
        if ( price != float(info[2][1:]) or
             perc_change != float(info[3].rsplit('%', 1)[0]) or
             perc_short != float(info[4].rsplit('%', 1)[0]) ):
            cur.execute('''UPDATE Stocks
                SET price = ?,
                    perc_change = ?,
                    perc_short = ?
                WHERE symbol = ? ''',
                (price, perc_change, perc_short, symbol, ))
            conn.commit()
            update_count += 1
            print("UPDATED DETAILS FOR", symbol)

#After handling all the data,
#display # of top shorted stocks based on user's initial input
cur.execute('SELECT * FROM Stocks ORDER BY perc_short DESC LIMIT ?', (count, ))
for ele in cur.fetchall():
    print(ele)

cur.close()

print('# of new stocks:', new_count)
print('# of updated stocks:', update_count)
