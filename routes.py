from flask import url_for, request

import db
from util import *


def routes(app):
	@app.route('/')
	def index():
		r = {}
		for rule in app.url_map.iter_rules():
			# Filter out rules we can't navigate to in a browser
			# and rules that require parameters
			if "GET" in rule.methods and has_no_empty_params(rule):
				endpoint = rule.endpoint
				url = url_decode(url_for(endpoint, **(rule.defaults or {})))
				func = app.view_functions[endpoint]
				args = rule.defaults or {}
				methods = list(rule.methods)
				func_doc = str.strip(func.__doc__).splitlines()[0] if func.__doc__ else ""
				r[endpoint] = {
					"url": url,
					"describe": func_doc,
					"methods": methods,
					"args": args
				}
			# links is now a list of url, endpoint tuples
		return json_response(200, r, True)

	@app.route("/table-desc", defaults={'table_name': ""})
	@app.route("/table-desc()", defaults={'table_name': ""})
	@app.route("/table-desc(<string:table_name>)")
	def cbdb_table_describe(table_name: str):
		"""
		get one or all tables describe infos
		:param table_name: optional, empty means all table desc
		"""
		r = []
		with_field_info = False if str(request.args.get("with_field_info")).lower() == "false" else True
		status = 200
		if not table_name:
			r = db.all_table_desc()
		elif table_name.upper() in db.all_table_name():
			r = db.table_desc(table_name, with_field_info)
		else:
			raise Exception("no such table")
		return json_response(status, r, True)

	@app.route("/query", defaults={"sql": ""})
	@app.route("/query()", defaults={"sql": ""})
	@app.route("/query(<string:sql>)")
	def cbdb_sql_query(sql):
		"""use sql to query cbdb"""
		sql = sql if sql else request.args.get("sql")
		r = [];
		status = 200;
		c = db.conn.execute(sql)
		r = db.record_to_dict_list(db.field_names(c), c.fetchall())
		return json_response(status, r)
