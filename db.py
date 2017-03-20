import sqlite3
from functools import lru_cache

# ?mode=ro means this connection only can do query operation
db_path = "file:./cbdb_sqlite.db?mode=ro"
conn = sqlite3.connect(db_path, uri=True)

SQL_SELECT_ALL_TABLE_NAME = "SELECT name FROM sqlite_master WHERE type='table';"
SQL_TABLE_DESC = "PRAGMA table_info('%s');"
SQL_TABLE_FIELD_DESC = "select * from tablesfields where upper(accesstblnm) = upper('%s') and accessfldnm = '%s'";


@lru_cache()
def all_table_name():
	"""
	all table name list

	:return: list
	"""
	return list(map(lambda record: record[0], conn.execute(SQL_SELECT_ALL_TABLE_NAME).fetchall()))


@lru_cache()
def table(table_name: str, param: dict):
	if str.upper(table_name) in all_table_name():
		pass
	else:
		raise Exception("no such table")


@lru_cache()
def table_desc(table_name: str, with_fields_desc=True):
	"""
	give out the table describe object

	:param table_name: the table name

	:param with_fields_desc: if need table fields info

	:return: dict
	"""
	columns = object_list_execute(SQL_TABLE_DESC % table_name)
	if with_fields_desc:
		for c in columns:
			_desc = table_field_desc(table_name, c["name"])
			if len(_desc):
				c["_field_desc"] = _desc
	r = {};
	r["_table_name"] = table_name
	r["_columns_count"] = len(columns)
	r["columns"] = columns
	return r


@lru_cache()
def all_table_desc(with_field_info=True):
	"""
	get all table describe objects

	:param with_field_info: if need table fields info

	:return: list[dict]
	"""
	r = [];
	for table_name in all_table_name():
		r.append(table_desc(table_name, with_field_info))
	return r


@lru_cache()
def table_field_desc(table_name: str, field_name: str):
	"""
	get specific field describe in a table

	:param table_name:

	:param field_name:

	:return:
	"""
	cursor = conn.execute(SQL_TABLE_FIELD_DESC % (table_name, field_name))
	names = field_names(cursor)
	field_infos = record_to_dict_list(names, cursor.fetchall())
	return field_infos[0] if len(field_infos) else {}


def field_names(c: sqlite3.Cursor):
	return list(map(lambda x: x[0], c.description))


def object_list_execute(sql: str):
	"""
	execute sql and return obejct list

	:param sql:

	:return:
	"""
	c = conn.execute(sql)
	return record_to_dict_list(field_names(c), c.fetchall())


def record_to_dict_list(field_names: [], records: []):
	"""
	transfer db records list to a dict

	:param field_names: db headers

	:param records: db records

	:return: list[dict]
	"""
	r = []
	for record in records:
		tmp_record = {}
		for i in range(len(field_names)):
			tmp_record[field_names[i]] = record[i]
		r.append(tmp_record)
	return r
