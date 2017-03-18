import db


def test_get_all_tables_name():
	table_names = db.all_table_name()
	assert len(table_names) > 0


def test_desc_of_table():
	table_name = "addresses"
	desc = db.table_desc(table_name)
	assert len(desc) > 0


def test_all_table_desc():
	assert db.all_table_desc()
