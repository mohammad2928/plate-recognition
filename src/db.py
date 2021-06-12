import pyodbc
import logging

from parameters import db_path, db_pass 
import datetime

class DB:

    def __init__(self):
        pass

    def connect(self):
        driver = "Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        conn = pyodbc.connect(r"{}DBQ={}; PWD={};".format(driver, db_path, db_pass))
        cursor = conn.cursor()
        return cursor, conn

    def select_rows(self, cursor, conn, query):
        rows = []
        cursor.execute(query)
        for row in cursor.fetchall():
            rows.append(row)
        return rows
    
    def remove_table(self, cursor, conn, query):
        cursor.execute(query)
        conn.commit()
        logging.warning("table {} removed".format(query))

    def list_of_tables(self, cursor, conn):
        for row in cursor.tables():
            print (row.table_name)

    def create_table(self, cursor, conn, query):
        cursor.execute(query)
        conn.commit()
        logging.warning("table {} added".format(query))

    def insert(self, cursor, conn, query, values):
        cursor.execute(query, values)
        conn.commit()
        logging.info("inserted")

    def update(self, cursor, conn, query, values):
        cursor.execute(query, values)
        conn.commit()
        logging.info("update {} by values {} ".format(query, values))

if __name__ == "__main__":

    db = DB()
    cursor, conn = db.connect()

    # query = "INSERT INTO Plate_table ([image_path], [plate_text],[capture_date]) VALUES (?,?, ?)"
    # values = ("val", "text plate", datetime.datetime.now())
    # db.insert(cursor, conn, query, values)

    # query = "UPDATE Plate_table SET plate_text = ? WHERE capture_date = ?"
    # values = ("update value", datetime.datetime(2021, 6, 11, 19, 52, 37))
    # db.update(cursor, conn, query, values)


    query = 'select * from {}'.format("Plate_table")
    print(db.select_rows(cursor, conn, query))

    # query = 'DROP TABLE Plate_table'
    # db.remove_table(cursor, conn, query)

    # query = "CREATE TABLE Plate_table(image_path varchar(70), plate_text varchar(70), capture_date date)"
    # db.create_table(cursor, conn, query)

    # db.list_of_tables(cursor, conn)
