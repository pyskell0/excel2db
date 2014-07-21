{
    "file_path": "用户.xls",
    "table":"user",
    "columns":{
        "用户名": {"column": "name", "type": "varchar", "nullable": false},
        "类型": {"column": "type", "type": "int", "nullable": false, "map": {"普通用户":0, "超级用户":1}},
        "状态": {"column": "enable", "type": "int", "nullable": false}
    }
}
