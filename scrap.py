from bs4 import BeautifulSoup
import re,urllib2,sys
import MySQLdb as mdb


page = urllib2.urlopen("https://www.cia.gov/library/publications/the-world-factbook/index.html")

soup = BeautifulSoup(page)

ul_tag = soup.find_all('ul',class_="af")

ul_tag = ul_tag[0]

a_tag = ul_tag.find_all('a')

con = mdb.connect(host='localhost',user='root',passwd='wtf',db='factbook',unix_socket='/opt/lampp/var/mysql/mysql.sock')
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS SHITDATA")

sql = """CREATE TABLE SHITDATA (ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	     country_id TEXT,
	     country TEXT ,
	     data LONGTEXT) """

cur.execute(sql)
for tag in a_tag:
    tag = str(tag)
    soup2 = BeautifulSoup(tag)
    if soup2.a.string != 'World':
        country=str(soup2.a.string)
    else:
        continue
    url = "https://www.cia.gov/library/publications/the-world-factbook/"+soup2.a['href']
    page2 = urllib2.urlopen(url)
    soup3 = BeautifulSoup(page2)
    # priunt soup3.title
    data1 = soup3.find_all('div',class_='CollapsiblePanel')
    final = ""
    content = ""
    for d in data1 :
        head = "<div class=\"head\">"+d.span.contents[0].string + d.span.contents[1].string+"</div>"
        table_tag = d.find_all('table',class_='CollapsiblePanelContent')
        class_name = table_tag[0].tr.find('tr')['class'][0]
        tr1 = table_tag[0].find_all('tr',class_="%s"%class_name)
        div = table_tag[0].find_all('td',id="data")
        for t1,t2 in zip(tr1,div):
            content =str(content)+ "<div class=\"subhead\">"+str(t1.div.a.contents[0].string)+"</div>"+str(t2)
        final =str(final) + str(head)+str(content)
    sql = "INSERT INTO SHITDATA(country_id, country,data) values(%s,%s,%s)"
    cur.execute(sql,(url,country,final))

    con.commit()
   
            
