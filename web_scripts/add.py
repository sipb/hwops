#!/usr/bin/python2
# -*- coding: utf-8 -*-
import cgi
import main

arguments = cgi.FieldStorage()
main.print_add(arguments["rack"].value, int(arguments["slot"].value))
