{
    "file_path": "domain.xls",
    "table":"domain",
    "columns":{
        "频道": {"column": "name", "type": "varchar", "nullable": false},
        "CDN类型": {
            "column": "service_type_id",
            "type": "int",
            "nullable": false,
            "foreign key": {
                "table": "service_type",
                "column": "name"
            }
        },
        "产品": {
            "nullable": false,
            "key": "domain_id",
            "key_type": "int",
            "type": "varchar",
            "many_to_many": {
                "inner_table": "group_domain",
                "table": "groups",
                "column": "name",
                "key": "group_id",
                "key_type": "int"
            }
        },
        "用途": {"column": "purpose", "type": "varchar", "nullable": true},
        "负责人": {"column": "responsible_person", "type": "varchar", "nullable": false},
        "源站": {"column": "src_station", "type": "varchar", "nullable": false},
        "负载均衡后面的机器": {
            "column": "src_station_real_servers",
            "type": "varchar",
            "nullable": true
        },
        "源站是否回位备份": {"column": "src_station_conn_strategy", "type": "varchar", "nullable": true},
        "缓存规则": {"column": "cache_strategy", "type": "varchar", "nullable": true}
    }
}
