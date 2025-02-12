# coding=utf-8
""""
---Db operations File---

By BlockMaster
"""
import sqlite3 as sq


class DB():
    def get_CO2_per_month(self, country):
        con = sq.connect("data.db")
        cur = con.cursor()
        cur.execute("SELECT data FROM data WHERE country_name = ?", (country,))
        res = list(cur.fetchall())
        con.close()
        return str(round(float(res[0][0]) / 12 * 1000000))
    
    
    def get_countries(self):
        con = sq.connect("data.db")
        cur = con.cursor()
        cur.execute("SELECT country_name FROM data")
        res = list(cur.fetchall())
        con.close()
        return [i[0] for i in res]
        