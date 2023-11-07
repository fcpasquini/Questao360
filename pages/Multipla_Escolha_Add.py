import streamlit as st
import sys
import yaml
import random

from database.db import Db

with open("config/config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

# Retrieve the processed data df, which has the title and body of the news
with Db(cfg["db"]) as db:
    disciplinas_df = db.select_df('SELECT * FROM disciplinas')

disciplinas_list = list(disciplinas_df['nome'].unique())

disciplina = st.selectbox('Disciplinas', disciplinas_list)

#disciplina = st.text_input('Disciplina: ')
subdisciplina = st.text_input('Subdisciplina: ')
banca = st.text_input('Banca: ')
concurso = st.text_input('Concurso: ')
ano = st.text_input('Ano: ')
enunciado = st.text_input('Enunciado: ')
alt_a = st.text_input('A: ')
alt_b = st.text_input('B: ')
alt_c = st.text_input('C: ')
alt_d = st.text_input('D: ')
alt_e = st.text_input('E: ')
alt_correta = st.text_input('Correta: ')

def add_questao(disciplina, subdisciplina, banca, concurso, ano, enunciado, alt_a, alt_b, alt_c, alt_d, alt_e, alt_correta):
    # Retrieve the processed data df, which has the title and body of the news
    try:
        alt_correta = int(alt_correta)
    except:
        alt_correta = 0
    try:
        ano = int(ano)
    except:
        ano = 0
    questao_me = (enunciado, alt_a, alt_b, alt_c, alt_d, alt_e, alt_correta, disciplina, subdisciplina, banca, concurso, ano)
    with Db(cfg["db"]) as db:
        db.insert_questao_me(questao_me)
    st.text('Questão adicionada com sucesso!')

if st.button('Adicionar questão'):
    add_questao(disciplina, subdisciplina, banca, concurso, ano, enunciado, alt_a, alt_b, alt_c, alt_d, alt_e, alt_correta)

