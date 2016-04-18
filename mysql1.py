#!/usr/bin/python3.4
import pymysql
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='master', db='scraping')
cur = conn.cursor()


cur.execute("USE scraping")
cur.execute("SELECT * FROM pages WHERE id=1")
print(cur.fetchone())
cur.close()
conn.close()