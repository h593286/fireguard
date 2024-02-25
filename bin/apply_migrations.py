import os
import hashlib

migration_table = """
GO
CREATE TABLE IF NOT EXISTS `Migrations` (
	`createdOn` TIMESTAMP(20),
	`name` VARCHAR(20),
	`hash` BINARY(16),
	PRIMARY KEY (`timestamp`,`name`)
);\n

CREATE INDEX Migrations_name_createdOn_IDX On Migrations(createdOn, name);\n
"""

migrations = [
    migration_table
]
if not os.path.exists("./migrations"):
    exit(1)
files = os.listdir("./migrations")

files.sort()

for file in files:
    date, name = file.split('_',1)
    # yyyymmddThhmmss
    year = date[:4]
    month = date[4:6]
    day = date[6:8]
    hour = date[9:11]
    minute = date[11:13]
    second = date[13:15]

    timestamp = f"{year}-{month}-{day} {hour}:{minute}:{second}"


    with open(f"./migrations/{file}/up.sql") as m:
        content = m.read()

        hash = hashlib.md5(content.encode('utf-8')).hexdigest()

        migrations.append("GO\n")
        migrations.append("IF NOT EXISTS (SELECT 1 FROM Migrations as M WHERE M.timestamp='")
        migrations.append(timestamp)
        migrations.append("' AND M.name='")
        migrations.append(name)
        migrations.append("')\nBEGIN\n")
        migrations.append("INSERT INTO Migrations(timestamp, name, hash) VALUES('")
        migrations.append(timestamp)
        migrations.append("', '")
        migrations.append(name)
        migrations.append("', '")
        migrations.append(hash)
        migrations.append("');\n")
        migrations.append(content)
        migrations.append("\nEND\n")


for m in migrations:
    print(m, sep='', end='')