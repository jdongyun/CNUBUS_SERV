#-*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import abort
from flask import render_template_string
from flask import Response
from flaskext.mysql import MySQL
from pymysql.err import ProgrammingError
import json
import base64
from flask_api import status
import time

app = Flask(__name__)

mysql = MySQL()
mysql_pw = base64.b64decode(b'').decode('utf-8')

post_key = 'xfjNb4WqiOPVLdR'
app.config['MYSQL_DATABASE_USER'] = 'cnubus'
app.config['MYSQL_DATABASE_PASSWORD'] = mysql_pw
app.config['MYSQL_DATABASE_DB'] = 'cnubus_database'

mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

#date = time.strftime("%Y%m%d")

cursor.execute("SELECT setting_value FROM `bus_setting` WHERE setting_key='bus_num'")
bus_num = cursor.fetchone()[0]

def create_db(conn, cursor):
        date = time.strftime("%Y%m%d")
        try:
                cursor.execute("SELECT * FROM bus_location_" + str(date))
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

create_db(conn, cursor)

cursor.close()


@app.route('/')
def location_main():
	return "CNUBUS Main"


@app.route('/location/', methods=['GET'])
def location_get():
	bus_list = []
	date = time.strftime("%Y%m%d")
	try:
		conn = mysql.connect()
		cursor = conn.cursor()	
#		create_db(conn, cursor)
		for i in range(0,int(bus_num)):
			cursor.execute("SELECT * FROM `bus_location_" + str(date) + "` WHERE id='q" + str(i+1) + "' ORDER BY `bus_location_" + str(date) + "`.`time` DESC LIMIT 1")
			columns = tuple([d[0] for d in cursor.description])
			bus_list.append(dict(zip(columns, cursor.fetchall()[0])))
			for row in cursor:
				print(row)
		json_list = {"bus_num" : int(bus_num), "bus_list" : bus_list}
		resp = Response(json.dumps(json_list), status=200, mimetype='application/json')
		cursor.close()
		return resp
		
	except Exception as e:
		cursor.close()
		print(e)
		app.logger.error(e)
		abort(404)

@app.route('/location/', methods=['POST'])
def location_post():
	
	date = time.strftime("%Y%m%d")
	try:
		if request.form['key'] != post_key:
			raise KeyError
		conn = mysql.connect()
		cursor = conn.cursor()

		bus_id = request.form['id']
		bus_lat = request.form['lat']
		bus_lng = request.form['lng']
		bus_accu = request.form['accu']
		bus_route = request.form['route']
		bus_head = request.form['head']
		bus_time = request.form['time']
		
		q = "INSERT INTO bus_location_" + str(date) + "(id, lat, lng, accu, route, head, time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
		print(q)
		cursor.execute(q, (bus_id, bus_lat, bus_lng, bus_accu, bus_route, bus_head, bus_time) )
		conn.commit()
		content = {"id" : bus_id, "response" : "정상적으로 발송되었습니다.", "time" : int(bus_time)}
		resp = Response(json.dumps(content), status=200, mimetype='application/json')
		return resp
	except KeyError as e:
		print(e)
		abort(403)

@app.errorhandler(403)
def error_403(e):
	content = {"response" : "정보에 오류가 있습니다."}
	resp = Response(json.dumps(content), status=403, mimetype='application/json')
	return resp

@app.errorhandler(404)
def error_404(e):
	content = {"response" : "데이터 정보를 불러올 수 없습니다."}
	resp = Response(json.dumps(content), status=404, mimetype='application/json')
	return resp

@app.errorhandler(500)
def error_500(e):
	content = {"response" : "서버에 오류가 있습니다."}
	resp = Response(json.dumps(content), status=500, mimetype='application/json')
	return resp


if __name__ == '__main__':
	app.run(host='0.0.0.0')
	

