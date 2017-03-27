import sqlite3
from functools import lru_cache

# ?mode=ro means this connection only can do query operation
db_path = "file:./cbdb_sqlite.db?mode=ro"
conn = sqlite3.connect(db_path, uri=True)

SQL_ALL_TABLE_INFO = "select * from sqlite_master where type='table';"
SQL_ALL_TABLE_NAME = "SELECT name FROM sqlite_master WHERE type='table';"
SQL_TABLE_DESC = "PRAGMA table_info('%s');"
SQL_TABLE_FIELD_DESC = "select * from tablesfields where upper(accesstblnm) = upper('%s') and accessfldnm = '%s'";
SQL_TABLE_RECORD_COUNT = "select count(*) from %s ;"


@lru_cache()
def all_table_info():
	"""all tables info"""
	return object_list_execute(SQL_ALL_TABLE_INFO)


@lru_cache()
def all_table_name():
	"""
	all table name list

	:return: list
	"""
	return list(map(lambda record: record[0], conn.execute(SQL_ALL_TABLE_NAME).fetchall()))


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
	r["_record_count"] = table_record_count(table_name)
	r["columns"] = columns
	return r


@lru_cache()
def table_record_count(tablename):
	"""get a specific records count"""
	r = conn.execute(SQL_TABLE_RECORD_COUNT % tablename).fetchone();
	return r[0]


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
	field_infos = records_to_dict_list(names, cursor.fetchall())
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
	return records_to_dict_list(field_names(c), c.fetchall())


def records_to_dict_list(field_names: [], records: []):
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


SQL_SELECT_OFFICE_TYPE_CHILD_NODES = "select * from office_type_tree where c_parent_id='%s';"

SQL_SELECT_TREE_CHILDS = "select * from %s where %s='%s';"


def table_tree(table_name, node_name_clm, node_id_clm, node_parent_id_clm, root_id, info_columns_name=[]):
	"""common use table to tree constructor"""

	def tree_childs(parent_id):
		r = []
		r_nodes = object_list_execute(SQL_SELECT_TREE_CHILDS % (table_name, node_parent_id_clm, parent_id))
		if len(r_nodes) > 0:
			for node in r_nodes:
				tmp = {}
				node_name = node[node_name_clm]
				node_id = node[node_id_clm]
				node_parent_id = node[node_parent_id_clm]
				node_children = tree_childs(node_id)
				tmp['name'] = node_name
				if node_children:
					tmp["children"] = node_children
				for info_column_name in info_columns_name:
					tmp[info_column_name] = node[info_column_name]
				r.append(tmp)
		return r

	return tree_childs(root_id)


def tree_childs_of(parent_id):
	"""please use common tree child fun"""
	r = {}
	r_nodes = object_list_execute(SQL_SELECT_OFFICE_TYPE_CHILD_NODES % parent_id)
	if len(r_nodes) > 0:
		for node in r_nodes:
			node_name = node["c_office_type_desc_chn"]
			node_id = node["c_office_type_node_id"]
			node_parent_id = node["c_parent_id"]
			node_childs = tree_childs_of(node_id)
			r[node_name] = node_childs
	return r


@lru_cache()
def offce_type_tree():
	office_tree = table_tree("office_type_tree", "c_office_type_desc_chn", "c_office_type_node_id",
	                         "c_parent_id", 0, ["c_office_type_desc"])
	return office_tree
