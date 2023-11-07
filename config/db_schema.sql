CREATE TABLE questoes_me (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enunciado TEXT NOT NULL,
    alternativa_1 TEXT NOT NULL,
    alternativa_2 TEXT NOT NULL,
    alternativa_3 TEXT NOT NULL,
    alternativa_4 TEXT NOT NULL,
    alternativa_5 TEXT NOT NULL,
    alternativa_correta INTEGER NOT NULL,
    disciplina TEXT NOT NULL,
    subdisciplina TEXT NOT NULL,
    banca TEXT NOT NULL,
    concurso TEXT NOT NULL,
    ano INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE questoes_ce (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enunciado TEXT NOT NULL,
    correta TEXT NOT NULL,
    disciplina TEXT NOT NULL,
    subdisciplina TEXT NOT NULL,
    banca TEXT NOT NULL,
    concurso TEXT NOT NULL,
    ano INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE disciplinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    tipo TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE subdisciplinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    disciplina_pai TEXT NOT NULL,
    tipo TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE concurso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    localidade_atuacao TEXT NOT NULL,    
    nivel_localidade TEXT NOT NULL,
    area_atuacao TEXT NOT NULL,
    situacao TEXT NOT NULL,
    edital_caminho TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE cartoes_memoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enunciado TEXT NOT NULL,
    resposta TEXT NOT NULL,
    disciplina TEXT NOT NULL,
    subdisciplina TEXT NOT NULL);
