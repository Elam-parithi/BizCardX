# SQL_Datahandler.py

import mysql.connector as sql
import secrets


def connect_db():
    mydb = sql.connect(
        host=secrets.hostname,
        port=secrets.portno,
        user=secrets.username,
        password=secrets.pswd,
        database=secrets.dataB
    )
    return mydb


def create_table(mycursor):
    mycursor.execute('''CREATE TABLE IF NOT EXISTS card_data
                        (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                         company_name TEXT,
                         card_holder TEXT,
                         designation TEXT,
                         mobile_number VARCHAR(50),
                         email TEXT,
                         website TEXT,
                         area TEXT,
                         city TEXT,
                         state TEXT,
                         pin_code VARCHAR(10),
                         image LONGBLOB
                        )''')


def insert_data(mycursor, mydb, df):
    for i, row in df.iterrows():
        sql_query = """INSERT INTO card_data(company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code, image)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        mycursor.execute(sql_query, tuple(row))
        mydb.commit()


def update_data(mycursor, mydb, data, selected_card):
    sql_query = """UPDATE card_data SET company_name=%s, card_holder=%s, designation=%s, mobile_number=%s, email=%s, website=%s, area=%s, city=%s, state=%s, pin_code=%s
                   WHERE card_holder=%s"""
    mycursor.execute(sql_query, (*data, selected_card))
    mydb.commit()


def delete_data(mycursor, mydb, selected_card):
    mycursor.execute(f"DELETE FROM card_data WHERE card_holder='{selected_card}'")
    mydb.commit()


def fetch_data(mycursor, query):
    mycursor.execute(query)
    result = mycursor.fetchall()
    return result
