{
    "file_path": "channel.xls",
    "table":"channel",
    "columns":{
        "频道": {
            "column": "domain_id",
            "type": "int",
            "nullable": false,
            "foreign key": {
                "table": "domain",
                "column": "name"
            }
        },
        "服务厂商": {
            "column": "cdn_id",
            "type": "int",
            "nullable": false,
            "foreign key": {
                "table": "cdn",
                "column": "name"
            }
        },
        "状态": {
            "column": "state_id",
            "type": "int",
            "nullable": false,
            "foreign key": {
                "table": "channel_state",
                "column": "name"
            }
        },
        "key": {"column": "key_on_cdn", "type": "varchar", "nullable": false},
        "cname": {"column": "cname", "type": "varchar", "nullable": false}
    }
}
