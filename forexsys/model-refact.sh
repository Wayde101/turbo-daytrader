#!/bin/sh

#rbackup
python ./manage.py dumpdata > data/initial-all.json
sleep 10

rm -f forexsys.db
python ./manage.py syncdb --noinput
python ./manage.py loaddata data/initial-all.json


