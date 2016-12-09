# -*- coding: utf-8 -*-
import sys
import random 
import mysql.connector
from mysql.connector import MySQLConnection

def formTables(region):
	tables = ["addresses_%s" % region]
	if(region == "ru" or region == "by"):
		tables.append("first_names_%s_girls" % region)
		tables.append("first_names_%s_men" % region)
		tables.append("last_names_%s_girls" % region)
		tables.append("last_names_%s_men" % region)
	else:
		tables.append("first_names_%s" % region)
		tables.append("last_names_%s" % region)
	tables.append("phones_%s" % region)
	return tables
def makeError(user,eps,symbols):
	new_user = ""
	while(eps!=0):
		eps-=1
		tmp = random.randint(0,2)
		tmp1 = random.randint(0,len(user)-1)
		if(tmp == 0):
			user = user[:tmp1] + user[(tmp1+1):]
		elif(tmp == 1):			
			user = user[:tmp1] + str(symbols[random.randint(0,len(symbols)-1)]) + user[tmp1:]
		else:
			tmp1 = random.randint(0,len(user)-2)
			user = user[:tmp1] + user[tmp1 + 1] + user[tmp1] + user[(tmp1 + 2):]
	return user
def generateByRu(cursor,tables,count):
	cursor.execute("SELECT * FROM %s" % tables[0])
	addresses = cursor.fetchall()
	cursor.execute("SELECT * FROM %s" % tables[1])
	girl_names = cursor.fetchall()
	cursor.execute("SELECT * FROM %s" % tables[2])
	men_names = cursor.fetchall()
	cursor.execute("SELECT * FROM %s" % tables[3])
	girl_surnames = cursor.fetchall()
	cursor.execute("SELECT * FROM %s" % tables[4])
	men_surnames = cursor.fetchall()
	cursor.execute("SELECT * FROM %s" % tables[5])
	phones = cursor.fetchall()
	users = []
	while(count!=0):
		count-=1
		sex = random.randint(0,1)
		user = ""
		if(sex==1):
			user += (men_names[random.randint(0,len(men_names)-1)][1]+
				" " + men_surnames[random.randint(0,len(men_surnames)-1)][1]+";")
		else:
			user += (girl_names[random.randint(0,len(girl_names)-1)][1]+
				" " + girl_surnames[random.randint(0,len(girl_surnames)-1)][1]+";")
		tmp = random.randint(0,len(addresses)-1)
		user+=(addresses[tmp][5]+";")
		tmp1 = random.randint(0,100)
		if(tmp1 == 0):
			flet = ""
		else:
			flet = u" кв." + str(tmp1)
		user+=(addresses[tmp][6]+" "+addresses[tmp][4]+" "+
			addresses[tmp][1]+u" дом "+str(random.randint(0,200))+flet+";")
		user+=phones[random.randint(0,len(phones)-1)][1]
		users.append(user)	
	return users
def generateUSA(cursor,tables,count):
	cursor.execute("SELECT * FROM %s" % tables[0])
	addresses = cursor.fetchall()
	cursor.execute("SELECT * FROM %s" % tables[1])
	names = cursor.fetchall()
	cursor.execute("SELECT * FROM %s" % tables[2])
	surnames = cursor.fetchall()
	cursor.execute("SELECT * FROM %s" % tables[3])
	phones = cursor.fetchall()
	users = []
	while(count!=0):
		count-=1
		user = ""
		user += (names[random.randint(0,len(names)-1)][1]+
			" " + surnames[random.randint(0,len(surnames)-1)][1]+";")
		tmp = random.randint(0,len(addresses)-1)
		user+=(addresses[tmp][4]+";")
		user+=(addresses[tmp][5]+" "+addresses[tmp][3]+" "+
			addresses[tmp][2]+" "+addresses[tmp][1]+";")
		user+=phones[random.randint(0,len(phones)-1)][1]
		users.append(user)	
	return users
region = sys.argv[1]
eps = int(sys.argv[3])
db = MySQLConnection(host='localhost', user='root', passwd='1773002153904il', db='task1')
cursor = db.cursor()
tables = formTables(region)
symbols = []
for i in range(32,58):
	symbols.append(chr(i))
for i in range(60,128):
	symbols.append(chr(i))
users = []
if(region == "ru" or region == "by"):
	users = generateByRu(cursor,tables,int(sys.argv[2]))
else:
	users = generateUSA(cursor,tables,int(sys.argv[2]))
db.close()
new_users = []
if(eps == 0):
	new_users = users
else:
	for user in users:
		new_users.append(makeError(user,eps,symbols))
print "Generated"