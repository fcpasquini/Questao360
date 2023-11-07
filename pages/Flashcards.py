import streamlit as st
import sys
import yaml
import random

from database.db import Db

with open("config/config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

# Retrieve the processed data df, which has the title and body of the news
with Db(cfg["db"]) as db:
    fc_df = db.select_df('SELECT * FROM cartoes_memoria')
    disciplinas_df = db.select_df('SELECT * FROM disciplinas')

disciplinas_list = list(disciplinas_df['nome'].unique())

def encapsulate_in_tag(mkdown_text, tag):
    tags_dict = {"p":["<p>", "</p>"], "div":["<div>", "</div>"], 
    "span":['<span class="highlight-text">', "</span>"], "div_column1":['<div class="column" id="column1">', 
    "</div>"], "div_column2":['<div class="column" id="column2">', "</div>"], 
    "div_column3":['<div class="column" id="column3">', "</div>"]}
    mkdown_text = f"{tags_dict[tag][0]}{mkdown_text}{tags_dict[tag][1]}"
    return mkdown_text

def get_fc_list(fc_df, disciplina_selecionada):
    fc_list = list(fc_df[fc_df['disciplina'] == disciplina_selecionada]['enunciado'])
    return fc_list

def get_fc(fc_df, disciplina_selecionada, fc_selecionado):
    fc_df_filtered = fc_df[fc_df['disciplina'] == disciplina_selecionada]
    fc_df_filtered = fc_df_filtered[fc_df_filtered['enunciado'] == fc_selecionado]
    resposta = list(fc_df_filtered['resposta'])[0]
    return fc_selecionado, resposta

st.set_page_config(page_title='Flashcards', page_icon=':car:', layout = 'wide')

with open('./page_content/03_Flashcards.txt', encoding="UTF-8") as file:
    page_content = file.read()

st.markdown(page_content, unsafe_allow_html=True)

fc_mkdown = ''

resposta_mkdown = ''

col1, col2 = st.columns([5, 5])

## Creating the sidebar to select the disciplina 
disciplina_selecionada = col1.selectbox('Disciplinas', disciplinas_list)

fc_list = get_fc_list(fc_df, disciplina_selecionada)

fc_selecionado = col1.selectbox('Flashcards', fc_list)

if col1.button('Atualizar flashcards'):
    fc_mkdown, resposta_mkdown = get_fc(fc_df, disciplina_selecionada, fc_selecionado)


col2.markdown(fc_mkdown, unsafe_allow_html = True)

expander = col2.expander('Mostrar resposta: ')
expander.markdown(resposta_mkdown, unsafe_allow_html = True)

