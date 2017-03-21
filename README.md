# cbdb_api

cbdb to api

in dev，欢迎与我交流，theo.sun@outlook.com

## install

```text
pip install -r requirements.txt
```

download and save **cbdb_sqlite.db** in root directory, you can download it from [here](http://projects.iq.harvard.edu/chinesecbdb/%E4%B8%8B%E8%BC%89cbdb%E5%96%AE%E6%A9%9F%E7%89%88)

## api

* http://server/ -- home page
* http://server/table-desc() -- all table describe info
* http://server/table-desc([tablename]) -- specific table describe info
* http://server/query([sql]) -- query table with sql
* http://server/tree/office-type -- give an office_type_tree json hierarchy object

Note: 可以不带括号


## sample

```text
GET https://cbdb-api.fornever.org
GET https://cbdb-api.fornever.org/table-desc()
GET https://cbdb-api.fornever.org/table-desc(addresses)
GET https://cbdb-api.fornever.org/query(select * from addresses limit 10)
GET https://cbdb-api.fornever.org/query()?sql=select * from addresses limit 10
```


## todo

* [ ] query api
* [x] query should be limit, only can be query
* [ ] server metadata
* [ ] any rdb data query server
* [ ] make api easy to use
* [ ] history address name change
* [ ] tree
* [ ] simplified chinese, introduce opencc

## Reference

* [CHINA BIOGRAPHICAL DATABASE PROJECT (CBDB)](http://projects.iq.harvard.edu/chinesecbdb)

## LICENCE

Since CBDB uses [CC BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh), the license is also used for this project