import sqlite3
from functools import lru_cache

db_path = "cbdb_sqlite.db"

conn = sqlite3.connect(db_path)

SQL_SELECT_ALL_TABLE_NAME = "SELECT name FROM sqlite_master WHERE type='table';"
SQL_DESC_TABLE_TMPL = "PRAGMA table_info('%s');"

@lru_cache()
def all_table_name():
	return list(map(lambda record: record[0], conn.execute(SQL_SELECT_ALL_TABLE_NAME).fetchall()))

@lru_cache()
def table_desc(tablename: str):
	def to_dict(record: list):
		# need to attention, there are 6 field in one record, but I can only understand 3 of them
		return {"idx": record[0], "colume_name": record[1], "data_type": record[2]}
	return list(map(lambda record: to_dict(record), conn.execute(SQL_DESC_TABLE_TMPL % tablename).fetchall()))

@lru_cache()
def all_table_desc():
	r = [];
	for tablename in all_table_name():
		r.append({
			"tablename": tablename,
			"columns": table_desc(tablename)
		})
	return r
