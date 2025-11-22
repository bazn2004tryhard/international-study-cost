import mysql.connector
from config.db_config import DB_CONFIG as database_config

# Prepare connection settings without the database so we can create it if needed
db_settings = database_config.copy()
database_name = db_settings.pop("database", None)

conn = mysql.connector.connect(**db_settings)
cursor = conn.cursor()

if database_name:
    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS `{database_name}` "
        "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    )
    cursor.execute(f"USE `{database_name}`")

# Đọc file .sql
with open(r"C:\Users\Vitus\Downloads\international_education_dump.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

# Tách theo dấu ;
commands = sql_script.split(";")

for command in commands:
    cmd = command.strip()
    if cmd:  # bỏ dòng trống
        cursor.execute(cmd)

conn.commit()
cursor.close()
conn.close()

print("SQL script executed.")
