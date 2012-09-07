#!/bin/sh

rm -f forexsys.db
python ./manage.py syncdb --noinput
python ./manage.py loaddata data/initial-all.json

#re-backup
python ./manage.py dumpdata > data/initial-all.json

