#!/bin/bash
kill -9 $(lsof -t -i:9008) >/dev/null 2>&1
python2 manage.py runserver 0.0.0.0:9008 >/dev/null 2>&1 & disown
echo -e "http://localhost:9008"

