import sqlite3

# SQLite DB Name
DB_Name =  "waterlog.db"

# SQLite DB Table Schema
TableSchema="""
drop table if exists Micro_Green_Temperature_Data ;
create table Micro_Green_Temperature_Data (
  id integer primary key autoincrement,
  SensorID text,
  PostedTime text,
  Temperature text
);
"""

#Connect or Create DB File
conn = sqlite3.connect(DB_Name)
curs = conn.cursor()

#Create Tables
sqlite3.complete_statement(TableSchema)
curs.executescript(TableSchema)

#Close DB
curs.close()
conn.close()
