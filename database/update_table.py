import sqlite3

def update_table(table_name, field, ID, data):
    with sqlite3.connect("EMS.db") as db:
        cursor = db.cursor()
        sql = "UPDATE {0} set {1}=? where {2}=?".format(table_name, field, ID)
        cursor.execute(sql, data)
        db.commit()

def increment_table(table_name, field, ID, data):
    with sqlite3.connect("EMS.db") as db:
        cursor = db.cursor()
        sql = "UPDATE {0} set {1}={1}+? where {2}=?".format(table_name, field, ID)
        cursor.execute(sql, data)
        db.commit()

def reduce_table(table_name, field, ID, data):
    with sqlite3.connect("EMS.db") as db:
        cursor = db.cursor()
        sql = "UPDATE {0} set {1}={1}-? where {2}=?".format(table_name, field, ID)
        cursor.execute(sql, data)
        db.commit()
