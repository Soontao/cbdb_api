from flask import Flask, request, json, Response, jsonify, redirect
from  util import json_response
import os, db, sqlite3

app = Flask(__name__)
port = os.getenv("PORT", 3001)


@app.route('/')
def home():
	r = {"server": "cbdb server", "desc": "this is a server to share cbcd data"};
	return json_response(200, r)


@app.route("/table-desc", defaults={'table_name': 'all_table'})
@app.route("/table-desc(<string:table_name>)")
def tables(table_name: str):
	r = []
	status = 200
	if table_name == "all_table":
		r = db.all_table_desc()
	else:
		r = db.table_desc(table_name)
	return json_response(status, r)


@app.route("/query(<string:sql>)")
def query(sql):
	r = [];
	status = 200;
	try:
		r = db.conn.execute(sql).fetchall()
	except Exception as e:
		# will raise sqlite3.OperationalError when sql syntax error
		# and if user attempt to use un-query sql, also will warning with this is a read only api
		r = {"err": "error happened", "message": e.args[0]}
		status = 500;
	finally:
		return json_response(status, r)


if __name__ == '__main__':
	# Run the app, listening on all IPs with our chosen port number
	app.run(host='0.0.0.0', port=port)
