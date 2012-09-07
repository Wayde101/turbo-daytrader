#!/bin/sh

rm -f forexsys.db
python ./manage.py syncdb --noinput
python ./manage.py loaddata data/initial-auth.json
python ./manage.py loaddata data/initial-tradesys.json

#re-backup
python ./manage.py dumpdata accounts > data/initial-auth.json
python ./manage.py dumpdata tradesys > data/initial-tradesys.json

