"""Creates a new migration file in the ./migration folder

The migration is structured as follows

./migrations
    |--<datetime>_<migration name>
        |--up.sql
        |--down.sql

up.sql is used to apply the migration to the database, and down.sql removes the migration

Parameters
----------
name: str, required
"""

import sys
import os
import re
import datetime

if len(sys.argv) < 2:
    raise BaseException("to few arguments. must be invoked as py ./bin/create_migration.py NAME")
name = sys.argv[-1]

if not re.match(r'[a-zA-Z_\-0-9]+',name):
    raise BaseException("Name must only consist of alphanumerics dash or underscore")

date = datetime.datetime.utcnow().isoformat(sep='T', timespec='seconds')
date = date.replace(':','')
date = date.replace('-','')

name = f"{date}_{name}"

path = f"./migrations/{name}"

if not os.path.exists(path):
    os.makedirs(path)

f = open(f"{path}/up.sql",'x')
f.close()
f = open(f"{path}/down.sql", 'x')
f.close()