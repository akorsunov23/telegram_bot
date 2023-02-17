import sqlite3 as sql
from typing import List

with sql.connect('data_base.db') as file:
	cur = file.cursor()

	cur.execute("""CREATE TABLE IF NOT EXISTS user (
		id_user INTEGER,
		name_command TEXT,
		data_time TEXT,
		info_hotels BLOB
		)""")


def add_data(id_user: int, command: str, date_time: str, info: str) -> None:
	with sql.connect('data_base.db') as db:
		insert = db.cursor()
		insert.execute(f"INSERT INTO user values {id_user, command, date_time, info}")


def get_data(id_user: int, amount: int) -> List:
	with sql.connect('data_base.db') as db:
		choose = db.cursor()
		choose.execute(f"SELECT name_command, data_time, info_hotels "
					f"FROM user WHERE id_user == {id_user} "
					f"ORDER by data_time DESC LIMIT {amount}")
		return choose.fetchall()
