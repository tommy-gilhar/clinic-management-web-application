"""
Created on Wed Feb 24 13:28:13 2021

@author: hadas
"""
from Initialization import Table
from sqlalchemy import create_engine
import mysql.connector

user = "root"
password = "8072362tommy"
ip = "127.0.0.1"
port = 3306
host = "localhost"
db = ""
tables = []
cursor = ""
con = ""


# Create Connection, save user, password into privates
def connect2server(usr=user, passwd=password, hst=host, prt=port):
    global user, password, host, port, cursor, con
    user = usr
    password = passwd
    host = hst
    port = prt
    con = mysql.connector.connect(host=host, user=user, passwd=password)
    cursor = con.cursor()
    return


def show_db():
    global cursor
    cursor.execute("SHOW DATABASES")
    print("Databases in server:")
    for x in cursor:
        print(x)
    return


def init_db(dbname):
    # this function enables communication with existing server
    # and initiation of a new DB
    global db, cursor
    db = dbname
    print(db)
    print(f"drop database if exists {db.lower()}")
    cursor.execute(f"drop database if exists {db.lower()}")
    # create a new database
    cursor.execute(f"CREATE DATABASE {db.upper()}")
    # showing that the database has been created
    show_db()
    return


def connect2server_db(database=db):
    # this function assumes existing connection to server
    # provided global connection specifications
    # and an existing DB.
    # it outputs the connection cursor to the db
    global user, password, host, port, cursor, db, con
    db = database
    # reconnect to database from server
    con = mysql.connector.connect(
        host=host, user=user, passwd=password, database=db.upper()
    )
    cursor = con.cursor()
    return cursor, con


def show_tables():
    # this function assumes existing connection cursor to server DB
    global cursor
    cursor.execute("show tables")
    print(f"Tables in DB:")
    for i in cursor:
        print(i)


def create_new_table(table, headers=[], dbname=db):
    global db, cursor
    if dbname != db:
        connect2server_db(dbname)
    if len(headers) == 0:
        headers = table.headers
    print(table.tableName.lower())
    cursor.execute(f"use {db}")
    cursor.execute(f"drop table if exists {table.tableName.lower()}")
    if "Timestamp" in table.headers:
        tbl_ftrs = f"CREATE TABLE {table.tableName.lower()} ({headers[0]} TIMESTAMP"
    else:
        tbl_ftrs = f"CREATE TABLE {table.tableName.lower()} ({headers[0]} VARCHAR(255)"
    for i in headers[1:]:
        if "Date" in i:
            tbl_ftrs += f", {i} DATE"
        else:
            tbl_ftrs += f", {i} VARCHAR(255)"

    tbl_ftrs += f")"
    print(tbl_ftrs)
    cursor.execute(tbl_ftrs)
    show_tables()
    return


def insert_data_to_table(table):
    global user, password, ip, port, db
    con = create_engine(
        "mysql+pymysql://"
        + user
        + ":"
        + password
        + "@"
        + ip
        + ":"
        + str(port)
        + "/"
        + db
    )
    table.data.to_sql(
        name=table.tableName.lower(), con=con, index=False, if_exists="append"
    )
    return


def add_pks(table):
    global cursor, db
    # re-initiate cursor
    connect2server_db(database=db)
    for i in table.pks:
        alter_table_com = (
            f"ALTER TABLE {table.tableName.lower()} " f"ADD PRIMARY KEY ({i})"
        )
        print(alter_table_com)
        cursor.execute(alter_table_com)


def add_fks(table):
    global cursor, db
    # re-initiate cursor
    connect2server_db(database=db)
    for i, k in enumerate(table.fks):
        alter_table_com = (
            f"ALTER TABLE {table.tableName.lower()} "
            f"ADD FOREIGN KEY ({k}) "
            f"REFERENCES {table.ref_tables[i]}({table.refs[i]})"
        )
        print(alter_table_com)
        cursor.execute(alter_table_com)


def main():
    # form a connection to server
    connect2server(usr="root", passwd="8072362tommy", hst="localhost", prt=3306)
    # initiate a database
    init_db("emr")
    # read csv file into table object
    tables = [
        Table("Doctors", "../doctors.csv", pks=["DOC_ID"]),
        Table(
            "Patients",
            "../patients.csv",
            pks=["patientID"],
            fks=["DOC_ID"],
            ref_tables=["doctors"],
            refs=["DOC_ID"],
        ),
        Table(
            "drugs",
            "../drugs.csv",
            fks=["patientID"],
            ref_tables=["patients"],
            refs=["patientID"],
        ),
        Table(
            "labresults",
            "../labresults.csv",
            fks=["patientID"],
            ref_tables=["patients"],
            refs=["patientID"],
        ),
    ]

    for table in tables:
        # create sql-table that corresponds to table object
        create_new_table(table, dbname="emr")
        # inject table data into corresponding sql table
        insert_data_to_table(table)
        # add primary keys to table
        add_pks(table)
        # add foreign keys to table (make sure they're in order of appearance)
        add_fks(table)


def commit_changes():
    global con
    con.commit()


if __name__ == "__main__":
    main()
