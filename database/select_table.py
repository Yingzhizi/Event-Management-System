import sqlite3

def select_all_products(table_name):
    with sqlite3.connect("EMS.db") as db:
        cursor = db.cursor()
        sql = "SELECT * FROM {0}".format(table_name)
        cursor.execute(sql)
        results = list(cursor.fetchall())
        return results

def select_product(table_name, field, id):
    with sqlite3.connect("EMS.db") as db:
        cursor = db.cursor()
        sql = "SELECT * FROM {0} where {1}=?".format(table_name, field)
        cursor.execute(sql, (id,)) # i can narrow it down Name,Price
        result = cursor.fetchone()
        return result

def select_products(table_name, field, id):
    with sqlite3.connect("EMS.db") as db:
        cursor = db.cursor()
        sql = "SELECT * FROM {0} where {1}=?".format(table_name, field)
        cursor.execute(sql, (id,)) # i can narrow it down Name,Price
        result = list(cursor.fetchall())
        return result

def select_column(sql, id):
    with sqlite3.connect("EMS.db") as db:
        cursor = db.cursor()
        cursor.execute(sql, id) # i can narrow it down Name,Price
        result = list(cursor.fetchall())
        return result
