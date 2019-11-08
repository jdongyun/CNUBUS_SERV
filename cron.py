#-*- coding: utf-8 -*-
from flask import Flask
from flaskext.mysql import MySQL
from pymysql.err import ProgrammingError
import base64
import datetime

app = Flask(__name__)

mysql = MySQL()
mysql_pw = base64.b64decode(b'').decode('utf-8')

app.config['MYSQL_DATABASE_USER'] = 'cnubus'
app.config['MYSQL_DATABASE_PASSWORD'] = mysql_pw
app.config['MYSQL_DATABASE_DB'] = 'cnubus_database'

mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

cursor.execute("SELECT setting_value FROM `bus_setting` WHERE setting_key='bus_num'")
bus_num = cursor.fetchone()[0]

date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y%m%d")


try:
	cursor.execute("SELECT * FROM bus_location_" + str(date))
	cursor.close()
except ProgrammingError:
	cursor.execute("CREATE TABLE `bus_location_"+ str(date)
                        +'''`(`id` varchar(5) NOT NULL,
                        `lat` double NOT NULL,
                        `lng` double NOT NULL,
                        `accu` double NOT NULL,
                        `route` varchar(3) NOT NULL,
			`head` int(11) NOT NULL,
                        `time` int(11) NOT NULL) 
                        ENGINE=InnoDB DEFAULT CHARSET=utf8''')
	for i in range(0, int(bus_num)):
#print("INSERT INTO `bus_location_"+ str(date) +"`(`id`, `lat`, `lng`, `accu`, `route`, `time`) VALUES (`q" + str(i) + "`, 0.0, 0.0, 0.0, `X`,0)")
		cursor.execute("INSERT INTO `bus_location_"+ str(date) +"`(`id`, `lat`, `lng`, `accu`, `route`, `head`, `time`) VALUES ('q" + str(i + 1) + "', 0.0, 0.0, 0.0, 'X', 0, 0)")
	conn.commit()
	cursor.close()
	
