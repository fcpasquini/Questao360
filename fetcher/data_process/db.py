import sqlite3
import pandas as pd


# This step of the process will be replaced by the container, which will better manage the files of the project
def get_project_root(number_of_ups):
    import os
    import sys

    project_root = os.path.dirname(__file__)

    number_of_ups -= 1

    for up in range(number_of_ups):
        project_root = os.path.dirname(project_root)
    
    sys.path.append(project_root)

get_project_root(3)


class Db(object):
    '''This python class aims to allow the usage of the sqlite3 database, in the other steps of the project. When instantiated, it creates a db object, that easily interacts with the sqlite3 database, to allow selects, insertions, table creations and deletion. To instantiate this class, it requires:
    - object(string): the filepath of the database which will be used.'''

    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        '''This method opens the database file, to allow the db edition. No args are required'''
        self.conn = sqlite3.connect(self.db_file)

    def close(self):
        '''This method closes the database file after finishing using it. No args are required'''
        self.conn.close()

    def select(self, sql, params=None):
        '''This method runs a sql query, to retrieve a table data. The following args are required:
        - sql(string): sql query that you aim to execute on the database, which will be modified if the params argument have been provided;
        - params(list[any]): list of parameters to be used in the sql query, changing its output
        '''
        curs = self.conn.cursor()
        if params is not None:
            res = curs.execute(sql, params)
        else:
            res = curs.execute(sql)
        return res.fetchall()

    def select_df(self, query):
        return pd.read_sql_query(query, self.conn)

    def get_tables(self):
        sql = """SELECT name FROM sqlite_master 
            WHERE type='table' AND 
            name NOT LIKE 'sqlite_%'
            ORDER BY name"""

        curs = self.conn.cursor()
        res = curs.execute(sql)
        tables = res.fetchall()
        tables = [t[0] for t in tables]
        return tables

    def get_table_df(self, table):
        return pd.read_sql_query(f"SELECT * FROM {table}", self.conn)

    def get_table(self, table):
        curs = self.conn.cursor()
        res = curs.execute(f"SELECT * FROM {table}")
        return res.fetchall()

    def get_table_where(self, table, source):
        curs = self.conn.cursor()
        res = curs.execute(f"SELECT * FROM {table} WHERE name = '{source}'")
        return res.fetchall()

    def insert_entities(self, names):
        curs = self.conn.cursor()
        sql = "INSERT into entities (name, full_name, type, segment) values (?, ?, ?, ?)"
        curs.executemany(sql, names)
        self.conn.commit()
        return curs.lastrowid

    def insert_sources(self, sources):
        curs = self.conn.cursor()
        sql = "INSERT into sources (name, url, username, passw) values (?,?,?,?)"
        curs.executemany(sql, sources)
        self.conn.commit()
        return curs.lastrowid

    def insert_corpus(self, sources):
        curs = self.conn.cursor()
        sql = "INSERT into corpus (sentence) values (?)"
        curs.execute(sql, sources)
        self.conn.commit()
        return curs.lastrowid

    def insert_news(self, news):
        curs = self.conn.cursor()
        sql = "INSERT into news (title, page_file, url, source_id) values (?,?,?,?)"
        curs.execute(sql, news)
        self.conn.commit()
        return curs.lastrowid

    def insert_keywords(self, keywords):
        curs = self.conn.cursor()
        sql = "INSERT into keywords (keyword, category, posneg) values (?,?,?)"
        curs.execute(sql, keywords)
        self.conn.commit()
        return curs.lastrowid
    
    def insert_sentences(self, sentence):
        curs = self.conn.cursor()
        sql = "INSERT into raw_sentences (sentence, origin_file) values (?,?)"
        curs.execute(sql, sentence)
        self.conn.commit()
        return curs.lastrowid

    def update_entity(self, name, id):
        sql = "update entities set name = ? where id = ?"
        curs = self.conn.cursor()
        curs.execute(sql, (name, id))
        self.conn.commit()

    def update_source(self, fields, id):
        i = 0
        values = []
        sql = "update sources set "
        for f, v in fields.items():
            if i > 0 and i < len(fields):
                sql += ", "
            sql += f + " = ?"
            values.append(v)
            i += 1
        sql += " where id = ?"
        values.append(id)

        curs = self.conn.cursor()
        curs.execute(sql, (values))
        self.conn.commit()

    def delete_by_ids(self, table, ids):
        curs = self.conn.cursor()
        sql = f"DELETE FROM {table} WHERE id = ?"
        ids = [(x,) for x in ids]
        curs.executemany(sql, ids)
        cnt = curs.rowcount
        self.conn.commit()
        return cnt
    

class ET_Db(Db):
    def __init__(self):
        super().__init__('data/db/sources.db')

