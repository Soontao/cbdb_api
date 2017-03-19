import sqlite3
import os
from functools import lru_cache

# ?mode=ro means this connection only can do query operation
db_path = "file:./cbdb_sqlite.db?mode=ro"
conn = sqlite3.connect(db_path, uri=True)

SQL_SELECT_ALL_TABLE_NAME = "SELECT name FROM sqlite_master WHERE type='table';"
SQL_DESC_TABLE_TMPL = "PRAGMA table_info('%s');"


@lru_cache()
def all_table_name():
	return list(map(lambda record: record[0], conn.execute(SQL_SELECT_ALL_TABLE_NAME).fetchall()))


@lru_cache()
def table(table_name: str, param: dict):
	if str.upper(table_name) in all_table_name():
		pass
	else:
		raise Exception("no such table")


@lru_cache()
def table_desc(tablename: str):
	def to_dict(record: list):
		# need to attention, there are 6 field in one record, but I can only understand 3 of them
		return {"idx": record[0], "colume_name": record[1], "data_type": record[2]}

	columns = list(map(lambda record: to_dict(record), conn.execute(SQL_DESC_TABLE_TMPL % tablename).fetchall()))
	return {
		"tablename": tablename,
		"columns": columns,
		"columns_count": len(columns)
	}


@lru_cache()
def all_table_desc():
	r = [];
	for tablename in all_table_name():
		r.append(table_desc(tablename))
	return r
