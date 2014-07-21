#!/usr/bin/env python
# coding:utf8

import web
from config import *
web.config.debug = debugIO
db = web.database(
        dbn="mysql",
        host=dbhost,
        db=dbname,
        user=dbuser,
        pw=dbpasswd)
