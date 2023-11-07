import sqlite3

import pandas as pd


class Db(object):
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        self.conn = sqlite3.connect(self.db_file)

    def close(self):
        self.conn.close()

    def select(self, sql, params=None):
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

    def insert_questao_me(self, questao_me):
        curs = self.conn.cursor()
        sql = "INSERT into questoes_me (enunciado, alternativa_1, alternativa_2, alternativa_3, alternativa_4, alternativa_5, alternativa_correta, disciplina, subdisciplina, banca, concurso, ano) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        curs.execute(sql, questao_me)
        self.conn.commit()
        return curs.lastrowid

    def insert_sources(self, sources):
        curs = self.conn.cursor()
        sql = "INSERT into sources (name, url, username, passw) values (?,?,?,?)"
        curs.executemany(sql, sources)
        self.conn.commit()
        return curs.lastrowid
    
    def insert_disciplina(self, disciplina):
        curs = self.conn.cursor()
        sql = "INSERT into disciplinas (nome, subdisciplina_1, subdisciplina_2, subdisciplina_3, tipo) values (?,?,?,?,?)"
        curs.execute(sql, disciplina)
        self.conn.commit()
        return curs.lastrowid    

    def insert_news(self, news):
        curs = self.conn.cursor()
        sql = "INSERT into news (title, page_file, url, source_id) values (?,?,?,?)"
        curs.execute(sql, news)
        self.conn.commit()
        return curs.lastrowid

    def insert_flashcards(self, fc):
        curs = self.conn.cursor()
        sql = "INSERT into cartoes_memoria (enunciado, resposta, disciplina, subdisciplina) values (?,?,?,?)"
        curs.execute(sql, fc)
        self.conn.commit()
        return curs.lastrowid

    def insert_keywords(self, keywords):
        curs = self.conn.cursor()
        sql = "INSERT into keywords (keyword, category, posneg) values (?,?,?)"
        curs.execute(sql, keywords)
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

    def run_query(self, sql):
        curs = self.conn.cursor()
        res = curs.execute(sql)
        self.conn.commit()
        return res.fetchall()