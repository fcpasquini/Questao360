import streamlit as st
import sys
import yaml
import random

from database.db import Db

with open("config/config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

# Retrieve the processed data df, which has the title and body of the news
with Db(cfg["db"]) as db:
    me_df = db.select_df('SELECT * FROM questoes_me')
    ce_df = db.select_df('SELECT * FROM questoes_ce')
    disciplinas_df = db.select_df('SELECT * FROM disciplinas')

disciplinas_list = list(disciplinas_df['nome'].unique())

questions_list = ['', '', '']

def encapsulate_in_tag(mkdown_text, tag):
    tags_dict = {"p":["<p>", "</p>"], "div":["<div>", "</div>"], 
    "span":['<span class="highlight-text">', "</span>"], "div_column1":['<div class="column" id="column1">', 
    "</div>"], "div_column2":['<div class="column" id="column2">', "</div>"], 
    "div_column3":['<div class="column" id="column3">', "</div>"]}
    mkdown_text = f"{tags_dict[tag][0]}{mkdown_text}{tags_dict[tag][1]}"
    return mkdown_text


def get_questoes_por_disciplina(disciplina, question_number, aleatorio = False):
    me_df_filtered = me_df[me_df['disciplina'] == disciplina]
    if aleatorio:
        question_number = random.randint(me_df_filtered.shape[0])
    dict_questao = get_questao(me_df_filtered, question_number)
    enunciado_mkdown = encapsulate_in_tag(dict_questao['enunciado'], 'p')

    header_text = '(' + dict_questao['banca'] + ' - ' + dict_questao['concurso'] + ' - ' + str(dict_questao['ano']) + ')'

    header_mkdown = encapsulate_in_tag(header_text, 'p')

    alternativa_1_mkdown = encapsulate_in_tag('A-) ' + dict_questao['A'], 'p')
    alternativa_2_mkdown = encapsulate_in_tag('B-) ' + dict_questao['B'], 'p')
    alternativa_3_mkdown = encapsulate_in_tag('C-) ' + dict_questao['C'], 'p')
    alternativa_4_mkdown = encapsulate_in_tag('D-) ' + dict_questao['D'], 'p')
    alternativa_5_mkdown = encapsulate_in_tag('E-) ' + dict_questao['E'], 'p')
    questao_mkdown = header_mkdown + enunciado_mkdown + alternativa_1_mkdown + alternativa_2_mkdown + alternativa_3_mkdown + alternativa_4_mkdown + alternativa_5_mkdown
    questao_mkdown = encapsulate_in_tag(questao_mkdown, 'div')

    resposta_mkdown = encapsulate_in_tag(str(dict_questao['correta']), 'p')

    return questao_mkdown, resposta_mkdown

def get_questao(df, question_number):
    me_df_filtered_question = df.loc[question_number - 1]
    enunciado = me_df_filtered_question['enunciado']
    alternativa_1 = me_df_filtered_question['alternativa_1']
    alternativa_2 = me_df_filtered_question['alternativa_2']
    alternativa_3 = me_df_filtered_question['alternativa_3']
    alternativa_4 = me_df_filtered_question['alternativa_4']
    alternativa_5 = me_df_filtered_question['alternativa_5']
    alternativa_correta = me_df_filtered_question['alternativa_correta']
    banca = me_df_filtered_question['banca']
    concurso = me_df_filtered_question['concurso']
    ano = me_df_filtered_question['ano']
    return {'enunciado':enunciado, 'A':alternativa_1, 'B':alternativa_2, 'C':alternativa_3, 
            'D':alternativa_4, 'E':alternativa_5, 'correta':alternativa_correta, 'banca':banca, 
            'concurso':concurso, 'ano':ano}

st.set_page_config(page_title='Questões de Múltipla Escolha', page_icon=':car:', layout = 'wide')

with open('./page_content/01_Multipla_Escolha.txt', encoding="UTF-8") as file:
    page_content = file.read()

st.markdown(page_content, unsafe_allow_html=True)

questao_mkdown = ''

resposta_mkdown = ''

col1, col2 = st.columns([3, 7])

## Creating the sidebar to select the disciplina 
disciplina_selecionada = col1.selectbox('Disciplinas', disciplinas_list)

questions_list = list(me_df[me_df['disciplina'] == disciplina_selecionada]['id'])

question_number = col1.selectbox('Questão', questions_list)

if col1.button('Atualizar questão'):
    questao_mkdown, resposta_mkdown = get_questoes_por_disciplina(disciplina_selecionada, question_number=question_number)

col2.markdown(questao_mkdown, unsafe_allow_html = True)

expander = col2.expander('Mostrar resposta: ')
expander.markdown(resposta_mkdown, unsafe_allow_html = True)

