#import asyncio
#import aioodbc

#trying to make a connection pool, getting a little fancy here

# loop = asyncio.get_event_loop()
#
# async def db_pool():
#     dsn = 'Driver=SQLite;Database=sqlite.db'
#     pool = await aioodbc.create_pool(dsn=dsn,loop=loop)
#
#     async with pool.acquire() as conn:
#         curr = await conn.cursor()

import sqlite3
import json
from time import gmtime, strftime

DB_Name = 'waterlog.db'

class DataBaseManager():
    """
    The beginnings of a database connection manager -- will eventually be "thread-safe"
    """
    def __init__(self):
        self.conn = sqlite3.connect(DB_Name)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.curr = self.conn.cursor()

    #this could be a lot more protective guarding against data pollution and such
    def insert_into_db(self,insert_query,args=()):
        self.curr.execute(insert_query,args)
        self.conn.commit()
        return

    def __del__(self):
        self.curr.close()
        self.conn.close()

def handle_microgreens_data(json_data):
    mc_data_dict = json.loads(json_data)
    s_id = mc_data_dict['sensor_id']
    time = mc_data_dict['time_stamp']
    temp = mc_data_dict['temperature']

    # print(s_id)
    # print(time)
    # print(temp)

    dbm = DataBaseManager()
    dbm.insert_into_db("INSERT into Micro_Green_Temperature_Data (SensorID,PostedTime,Temperature) VALUES (?,?,?)",(s_id,time,temp))
    del dbm
