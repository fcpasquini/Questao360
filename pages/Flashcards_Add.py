import streamlit as st
import yaml

from database.db import Db

with open("config/config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

button_value = False

# Retrieve the processed data df, which has the title and body of the news
with Db(cfg["db"]) as db:
    disciplinas_df = db.select_df('SELECT * FROM disciplinas')

disciplinas_list = list(disciplinas_df['nome'].unique())

disciplina = st.selectbox('Disciplinas', disciplinas_list)
subdisciplina = st.text_input('Subdisciplina: ')
enunciado = st.text_input('Flashcard: ')
resposta = st.text_input('Resposta: ')

def add_fc(enunciado, resposta, disciplina, subdisciplina):
    # Retrieve the processed data df, which has the title and body of the news
    fc = (enunciado, resposta, disciplina, subdisciplina)
    if fc[0] != '':
        with Db(cfg["db"]) as db:
            db.insert_flashcards(fc)
        st.text('Questão adicionada com sucesso!')

button_value = st.button('Adicionar flashcard')

if button_value:
    on_click=add_fc(enunciado, resposta, disciplina, subdisciplina)
    button_value = False