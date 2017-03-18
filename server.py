from flask import Flask, request, json, Response, jsonify, redirect
from  util import json_response
import os
import db

app = Flask(__name__)
port = os.getenv("PORT", 3001)


@app.route('/')
def home():
	r = {"server": "cbdb server", "desc": "this is a server to share cbcd data"};
	return Response(response=json.dumps(r, ensure_ascii=False, indent=2),
									status=200,
									mimetype="application/json")


@app.route("/tables")
def tables():
	resp = Response(response=json.dumps(db.all_table_desc(), ensure_ascii=False, indent=2),
									status=200,
									mimetype="application/json")
	return resp


@app.route("/query('<string:sql>')")
def query(sql):
	r = db.conn.execute(sql).fetchall()
	return json_response(200, r)


if __name__ == '__main__':
	# Run the app, listening on all IPs with our chosen port number
	app.run(host='0.0.0.0', port=port)
