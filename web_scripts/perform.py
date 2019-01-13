#!/usr/bin/python2
# -*- coding: utf-8 -*-
import cgi
import main

arguments = cgi.FieldStorage()
action = arguments["action"].value
if action == "add":
    main.perform_add({field: arguments[field].value for field in arguments})
elif action == "update":
    main.perform_update({field: arguments[field].value for field in arguments})
elif action == "add-part":
    main.perform_add_part({field: arguments[field].value for field in arguments})
elif action == "update-stock":
    main.perform_update_stock({field: arguments[field].value for field in arguments})
else:
    assert False
