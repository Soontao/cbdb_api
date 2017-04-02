from flask import url_for, request

import db
from util import *


def routes(app):
    """app routes"""

    @app.route('/')
    def index():
        """index page"""
        r = {}
        for rule in app.url_map.iter_rules():
            # Filter out rules we can't navigate to in a browser, and rules that require parameters
            if has_no_empty_params(rule):
                endpoint = rule.endpoint
                end_point_url = url_decode(
                    url_for(endpoint, **(rule.defaults or {})))
                end_point_func = app.view_functions[endpoint]
                r[endpoint] = {
                    "url":
                    end_point_url,
                    "describe":
                    str.strip(end_point_func.__doc__).splitlines()[0]
                    if end_point_func.__doc__ else "",
                    "methods":
                    list(rule.methods),
                    "args":
                    rule.defaults or {}
                }
        return json_response(200, r, True)

    @app.route("/tables")
    def cbdb_table_basic_info():
        """get basic table infos"""
        return json_response(obj=db.all_table_info())

    @app.route("/table-desc")
    def cbdb_table_describe():
        """
        get one or all tables describe infos
        :param table_name: optional, empty means all table desc
        """
        r = []
        table_name = request.args.get("table_name") or ""
        with_field_info = False if str(
            request.args.get("with_field_info")).lower() == "false" else True
        status = 200
        if not table_name:
            r = db.all_table_desc()
        elif table_name.upper() in db.all_table_name():
            r = db.table_desc(table_name, with_field_info)
        else:
            raise Exception("no such table")
        return json_response(status, r, True)

    @app.route("/query")
    def cbdb_sql_query():
        """use sql to query cbdb"""
        sql = request.args.get("sql") or ""
        r = []
        status = 200
        c = db.conn.execute(sql)
        r = db.records_to_dict_list(db.field_names(c), c.fetchall())
        return json_response(status, r)

    @app.route("/tree/office-type")
    def cbdb_office_type_tree():
        """get the office type tree"""
        return json_response(obj=db.offce_type_tree())
