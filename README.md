# cbdb_api

cbdb to api

in dev

## install

```
pip install -r requirements.txt
```

download and save **cbdb_sqlite.db** in root directory

## api

* http://server/ -- home page
* http://server/table-desc -- all table describe info
* http://server/table-desc(\<tablename\>) -- specific table describe info
* http://server/query(\<sql\>) -- query table

## sample

```text
GET https://api.fornever.org/cbdb
GET https://api.fornever.org/cbdb/table-desc
GET https://api.fornever.org/cbdb/table-desc(address)
GET https://api.fornever.org/cbdb/query(select * from addresses limit 10)
```

## todo

* [ ] query api
* [ ] query should be limit
* [ ] server metadata
* [ ] any rdb data query server
* [ ] make api easy to use