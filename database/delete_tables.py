import sqlite3

def delete_table(table_name):
    with sqlite3.connect('EMS.db') as db:
        cursor = db.cursor() #navigate around database
        cursor.execute("drop table if exists {0}".format(table_name))
        db.commit()
