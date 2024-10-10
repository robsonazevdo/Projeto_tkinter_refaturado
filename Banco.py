from contextlib import closing
import sqlite3
import os
import werkzeug 
from datetime import date, datetime

############################################### 
#### Coisas internas do API. ####
###############################################

def extensao_arquivo(filename):
    if '.' not in filename: return ''
    return filename.rsplit('.', 1)[1].lower()

'''def salvar_arquivo_upload():
    import uuid
    if "foto" in request.files:
        foto = request.files["foto"]
        e = extensao_arquivo(foto.filename)
        if e in ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp']:
            u = uuid.uuid1()
            n = f"{u}.{e}"
            foto.save(os.path.join("funcionario_fotos", n))
            return n
    return ""

def deletar_foto(id_foto):
    if id_foto == '': return
    p = os.path.join("funcionario_fotos", id_foto)
    if os.path.exists(p):
        os.remove(p)

def autenticar_login():
    login = request.cookies.get("login", "")
    senha = request.cookies.get("senha", "")
    return db_fazer_login_admin(login, senha)
'''

##########################################
#### Definições de regras de negócio. ####
##########################################

def criar_cliente(nome, telefone): 
    cliente_ja_existe = db_verificar_cliente(nome, telefone)
    if cliente_ja_existe is not None: return True, cliente_ja_existe
    novo_cliente = db_criar_cliente(nome, telefone)
    return False, novo_cliente


def criar_agendamento(data1,hora, id_cliente, id_servico, id_funcionario):
    serie_ja_existe = db_verificar_agendamento(data1,hora, id_cliente, id_servico, id_funcionario)
    if serie_ja_existe is not None: return True, serie_ja_existe
    novo_agendamento = db_criar_agendamento(data1,hora, id_cliente, id_servico, id_funcionario)
    return False, novo_agendamento


def criar_atendimento(id_cliente, valor_unitario, desconto, valor_total, id_forma_pagamento, descricao,data):
    ja_existe = db_verificar_atendimento(id_cliente, valor_unitario, desconto, valor_total, id_forma_pagamento, descricao,data)
    if ja_existe is not None: return True, ja_existe
    novo_atendimento = db_criar_atendimento(id_cliente, valor_unitario, desconto, valor_total, id_forma_pagamento, descricao, data)
    return False, novo_atendimento


def criar_servico(nome_servico, preco_servico, duracao_servico, status, id_cargo):
    servico_ja_existe = db_verificar_servico(nome_servico, preco_servico, duracao_servico, status, id_cargo)
    if servico_ja_existe is not None: return True, servico_ja_existe
    novo_servico = db_criar_servico(nome_servico, preco_servico, duracao_servico, status, id_cargo)
    return False, novo_servico


def criar_servico_funcionario(i, id_funcionario):
    servico_ja_existe = db_verificar_servico_funcionario(i, id_funcionario)
    if servico_ja_existe is not None: return True, servico_ja_existe
    novo_servico = db_criar_servico_funcionario(i, id_funcionario)
    return False, novo_servico  


def criar_funcionario(id_cargo, nome, cpf, email, endereco, telefone, status):
    funcionario_ja_existe = db_verificar_funcionario(id_cargo, nome, cpf, email, endereco, telefone, status)
    if funcionario_ja_existe is not None: return True, funcionario_ja_existe
    novo_funcionario = db_criar_funcionario(id_cargo, nome, cpf, email, endereco, telefone, status)
    return False, novo_funcionario


def criar_comanda(id_cliente, numero_comanda, data_venda, id_operacao, id_situacao, id_funcionario):
    comanda_ja_existe = db_verificar_comanda(id_cliente, numero_comanda, data_venda, id_operacao, id_situacao, id_funcionario)
    if comanda_ja_existe is not None: return True, comanda_ja_existe
    nova_comanda = db_criar_comanda(id_cliente, numero_comanda, data_venda, id_operacao, id_situacao, id_funcionario)
    return False, nova_comanda   

 

def criar_additems(id_comanda, id_servico, quantidade, id_funcionario):
    additems_ja_existe = db_verificar_additems(id_comanda, id_servico, quantidade, id_funcionario)
    if additems_ja_existe is not None: return True, additems_ja_existe
    nova_add = db_criar_additems(id_comanda, id_servico, quantidade, id_funcionario)
    return False, nova_add



def criar_comanda_fechada(id_comanda, forma_pagamento, desconto, valor_total):
    comanda_fechada_ja_existe = db_verificar_comanda_fechada(id_comanda, forma_pagamento, desconto, valor_total)
    if comanda_fechada_ja_existe is not None: return True, comanda_fechada_ja_existe
    nova_add = db_criar_comanda_fechada(id_comanda, forma_pagamento, desconto, valor_total)
    return False, nova_add



def criar_cargo(nome_cargo):
    cargo_ja_existe = db_verificar_cargo(nome_cargo)
    if cargo_ja_existe is not None: return True, cargo_ja_existe
    novo_cargo = db_criar_cargo(nome_cargo)
    return False, novo_cargo


def apagar_agendamento(id_agendamento, data_agendamento):
    agendamento = db_meu_agendamento(id_agendamento, data_agendamento)
    if agendamento is not None: db_deletar_agendamento(id_agendamento)
    return agendamento


def apagar_funcionario(id_funcionario):
    funcionario = db_consultar_funcionario(id_funcionario)
    if funcionario is not None: db_deletar_funcionario(id_funcionario)
    return funcionario


def apagar_cliente(id_cliente, nome):
    cli = db_meu_cliente(id_cliente, nome)
    if cli is not None: db_deletar_cliente(id_cliente)
    return cli


def editar_agendamento(id_agendamento, data1, hora, id_cliente, id_servico, id_funcionario):
    agendamento = db_consultar_agendamento(id_agendamento)
    
    if agendamento is None:
        return 'não existe', None
    
    db_editar_agendamento(id_agendamento, data1, hora, id_cliente, id_servico, id_funcionario)
    return 'alterado', agendamento


def editar_funcionario(id_funcionario, nome, email, endereco, cpf, telefone, id_cargo, status):
    funcionario = db_consultar_funcionario(id_funcionario)
    
    if funcionario is None:
        return 'não existe', None

    f = db_editar_funcionario(id_funcionario,nome,email,endereco,cpf,telefone,id_cargo,status)
    return 'alterado', f



def editar_servico(id_servico, nome, valor, duracao, status, id_cargo):
    servico = db_consultar_servico(id_servico)
    
    if servico is None:
        return 'não existe', None

    s = db_editar_servico(id_servico, nome, valor, duracao, status, id_cargo)
    return 'alterado', s

###############################################
#### Funções auxiliares de banco de dados. ####
###############################################

# Converte uma linha em um dicionário.
def row_to_dict(description, row):
    if row is None: return None
    d = {}
    for i in range(0, len(row)):
        d[description[i][0]] = row[i]
    return d

# Converte uma lista de linhas em um lista de dicionários.
def rows_to_dict(description, rows):
    result = []
    for row in rows:
        result.append(row_to_dict(description, row))
    return result

#### Definições básicas do banco. ####

sql_create = """ 



CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL,
    telefone VARCHAR(11) NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_admin (
    id_admin INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    senha VARCHAR(10) NOT NULL,
    UNIQUE(email)
);

CREATE TABLE IF NOT EXISTS cargo (
    id_cargo INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_cargo VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS situacao (
    id_situacao INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(8) NOT NULL
);

CREATE TABLE IF NOT EXISTS operacao (
    id_operacao INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(8) NOT NULL
);

CREATE TABLE IF NOT EXISTS forma_pagamento (
    id_forma_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(8) NOT NULL
);

CREATE TABLE IF NOT EXISTS servico (
    id_servico INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_servico VARCHAR(50) NOT NULL,
    preco_servico REAL NOT NULL,
    duracao_servico INTEGER NOT NULL,
    status VARCHAR(7) NOT NULL,
    id_cargo INTEGER NOT NULL,
    FOREIGN KEY (id_cargo) REFERENCES cargo(id_cargo)
);

CREATE TABLE IF NOT EXISTS funcionario (
    id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cargo INTEGER NOT NULL,
    nome VARCHAR(50) NOT NULL,
    cpf VARCHAR(14) NOT NULL,
    email VARCHAR(50) NOT NULL,
    endereco VARCHAR(50) NOT NULL,
    telefone VARCHAR(12) NOT NULL,
    status VARCHAR(7) NOT NULL,
    UNIQUE(email),
    FOREIGN KEY (id_cargo) REFERENCES cargo(id_cargo)
);

CREATE TABLE IF NOT EXISTS servico_funcionario (
    id_servico_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
    id_servico INTEGER NOT NULL,
    id_funcionario INTEGER NOT NULL,
    FOREIGN KEY (id_servico) REFERENCES servico(id_servico),
    FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario)
    
);

CREATE TABLE IF NOT EXISTS agendamento (
    id_agendamento INTEGER PRIMARY KEY AUTOINCREMENT,
    data1 date NOT NULL,
    hora time NOT NULL,
    id_cliente INTEGER NOT NULL,
    id_servico INTEGER NOT NULL,
    id_funcionario INTEGER NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_servico) REFERENCES servico(id_servico),
    FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario)

);

CREATE TABLE IF NOT EXISTS comanda (
    id_comanda INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_comanda INTEGER NOT NULL,
    data_venda Date NOT NULL,
    id_cliente INTEGER NOT NULL,
    id_operacao INTEGER NOT NULL,
    id_situacao INTEGER NOT NULL,
    id_funcionario INTEGER NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_situacao) REFERENCES situacao(id_situacao),
    FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario),
    FOREIGN KEY (id_operacao) REFERENCES operacao(id_operacao)

);

CREATE TABLE IF NOT EXISTS addItems (
    id_item_comanda INTEGER PRIMARY KEY AUTOINCREMENT, 
    id_comanda INTEGER NOT NULL,
    id_servico INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    id_funcionario INTEGER NOT NULL,    
    FOREIGN KEY (id_comanda) REFERENCES comanda(id_comanda),
    FOREIGN KEY (id_servico) REFERENCES servico(id_servico),
    FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario)
);



CREATE TABLE IF NOT EXISTS comandaFechada (
    id_comanda_fechada INTEGER PRIMARY KEY,
    id_comanda INTEGER NOT NULL,
    forma_pagamento JSON NOT NULL,  
    desconto REAL NOT NULL,
    valor_total REAL NOT NULL,
    FOREIGN KEY (id_comanda) REFERENCES comanda(id_comanda)
);

CREATE TABLE IF NOT EXISTS atendimento (
    id_atendimento INTEGER PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    valor_unitario REAL NOT NULL,
    desconto REAL NOT NULL,
    valor_total REAL NOT NULL,
    id_forma_pagamento INTERGER NOT NULL,
    descricao VARCHAR(300) NOT NULL,
    data DATETIME NOT NULL,
    FOREIGN KEY (id_forma_pagamento) REFERENCES forma_pagamento(id_forma_pagamento),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)

);

CREATE TABLE IF NOT EXISTS saida (
    id_saida INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATETIME NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    valor_total REAL NOT NULL,
    observacao VARCHAR(100) NOT NULL
    
);

REPLACE INTO forma_pagamento (id_forma_pagamento, nome) VALUES (1, 'PIX');
REPLACE INTO forma_pagamento (id_forma_pagamento, nome) VALUES (2, 'Dinheiro');
REPLACE INTO forma_pagamento (id_forma_pagamento, nome) VALUES (3, 'Débito');
REPLACE INTO forma_pagamento (id_forma_pagamento, nome) VALUES (4, 'Crédito a vista');
REPLACE INTO forma_pagamento (id_forma_pagamento, nome) VALUES (5, 'Crédito Parcelado');
REPLACE INTO forma_pagamento (id_forma_pagamento, nome) VALUES (6, 'Pagamento Misto');
REPLACE INTO forma_pagamento (id_forma_pagamento, nome) VALUES (7, 'Vale-presente');



REPLACE INTO tb_admin (nome, email, senha) VALUES ('Susana Alves Azevedo', 'susana.azevedo', '198385');

REPLACE INTO cargo (id_cargo, nome_cargo) VALUES (1,'Cabelereiro');
REPLACE INTO cargo (id_cargo, nome_cargo) VALUES (2,'Manicure');
REPLACE INTO cargo (id_cargo, nome_cargo) VALUES (3,'Auxiliar');
REPLACE INTO cargo (id_cargo, nome_cargo) VALUES (4,'Design');


REPLACE INTO situacao (id_situacao, nome) VALUES (1,'Aberto');
REPLACE INTO situacao (id_situacao, nome) VALUES (2,'Fechado');


REPLACE INTO operacao (id_operacao, nome) VALUES (1,'Venda');
REPLACE INTO operacao (id_operacao, nome) VALUES (2,'Troca');
REPLACE INTO operacao (id_operacao, nome) VALUES (3,'Devolção');


"""


# REPLACE INTO servico (id_servico, nome_servico, preco_servico, duracao_servico, status, id_cargo) VALUES (1, 'Corte', 50.00, '60', 'ativo', '1');
# REPLACE INTO servico (id_servico, nome_servico, preco_servico, duracao_servico, status, id_cargo) VALUES (2, 'Escova', 40.00, '40', 'ativo', '1');
# REPLACE INTO servico (id_servico, nome_servico, preco_servico, duracao_servico, status, id_cargo) VALUES (3, "Luzes", 600.00, '240', 'ativo', '1');
# REPLACE INTO servico (id_servico, nome_servico, preco_servico, duracao_servico, status, id_cargo) VALUES (4, "Progressiva", 200.00, '240', 'ativo', '1');
# REPLACE INTO servico (id_servico, nome_servico, preco_servico, duracao_servico, status, id_cargo) VALUES (5, "Aplicação Coloração", 40.00, '60', 'ativo', '1');
# REPLACE INTO servico (id_servico, nome_servico, preco_servico, duracao_servico, status, id_cargo) VALUES (6, "Coloração", 80.00, '60', 'ativo', '1');
# REPLACE INTO servico (id_servico, nome_servico, preco_servico, duracao_servico, status, id_cargo) VALUES (7, "Designer de Sobrancelhas", 30.00, '30', 'ativo', '4');
# REPLACE INTO servico (id_servico, nome_servico, preco_servico, duracao_servico, status, id_cargo) VALUES (8, "Buço", 25.00, '60', 'ativo', '4');

# REPLACE INTO funcionario (id_funcionario, id_cargo, nome, cpf, email, endereco, telefone, status) VALUES (1, 1, 'Susana Azevedo', '00000000000', 'susana@email.com', 'rua tal', '00988887777', 'ativo');
# REPLACE INTO funcionario (id_funcionario, id_cargo, nome, cpf, email, endereco, telefone, status) VALUES (2, 1, 'Robson Azevedo', '00000000000', 'robson@email.com', 'rua tal', '00988887777', 'ativo');
# REPLACE INTO funcionario (id_funcionario, id_cargo, nome, cpf, email, endereco, telefone, status) VALUES (3, 1, 'Joana Feliz', '00000000000', 'joana@email.com', 'rua tal', '00988887777', 'ativo');


# CREATE TABLE IF NOT EXISTS comanda_item (
#     id_item INTEGER PRIMARY KEY AUTOINCREMENT,
#     id_comanda INTEGER,
#     descricao_servico TEXT,
#     valor_servico REAL,
#     FOREIGN KEY (id_comanda) REFERENCES comanda(id_comanda)
# );

# CREATE TABLE IF NOT EXISTS comanda_pagamento (
#     id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
#     id_comanda INTEGER,
#     forma_pagamento TEXT,
#     valor_pagamento REAL,
#     FOREIGN KEY (id_comanda) REFERENCES comanda(id_comanda)
# );





def conectar():
    return sqlite3.connect('agenda.db')


def db_inicializar():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.executescript(sql_create)
        con.commit()


def db_verificar_cliente(nome, telefone):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cliente, nome,telefone FROM cliente WHERE nome = ? AND telefone = ?", [nome,telefone])
        return row_to_dict(cur.description, cur.fetchone())


def db_verificar_agendamento(data1, hora, id_cliente, id_servico, id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_agendamento, data1, hora, id_cliente, id_servico, id_funcionario FROM agendamento WHERE data1 = ? AND hora = ? AND id_funcionario = ?", [data1, hora, id_funcionario])
        return row_to_dict(cur.description, cur.fetchone())
    
    
def db_verificar_atendimento(id_cliente, valor_unitario, desconto, valor_total, id_forma_pagamento, descricao,data):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_atendimento, id_cliente, valor_unitario, desconto, valor_total, id_forma_pagamento, descricao, data FROM atendimento WHERE id_cliente = ? AND descricao = ? AND valor_unitario = ? AND desconto = ? AND valor_total = ? AND id_forma_pagamento = ? AND data =?", [id_cliente, valor_unitario, desconto, valor_total, id_forma_pagamento, descricao,data])
        return row_to_dict(cur.description, cur.fetchone())


def db_verificar_servico_funcionario(i, id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT sf.id_servico, sf.id_funcionario FROM servico_funcionario as sf INNER JOIN servico AS s ON s.id_servico = sf.id_servico WHERE s.id_servico = ? AND id_funcionario = ? ", [i - 1, id_funcionario])
        return row_to_dict(cur.description, cur.fetchone())


def db_verificar_servico(nome_servico, preco_servico, duracao_servico, status, id_cargo):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_servico, nome_servico, preco_servico, duracao_servico, status, id_cargo FROM servico WHERE nome_servico = ? AND preco_servico = ? AND duracao_servico = ? AND status = ? AND id_cargo = ?", [nome_servico, preco_servico, duracao_servico, status, id_cargo])
        return row_to_dict(cur.description, cur.fetchone())


def db_verificar_cargo(nome_cargo):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cargo, nome_cargo FROM cargo WHERE nome_cargo = ?", [nome_cargo])
        return row_to_dict(cur.description, cur.fetchone())


def db_verificar_funcionario(id_cargo, nome, cpf, email, endereco, telefone, status):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_funcionario, id_cargo, nome, cpf, email, endereco, telefone, status FROM funcionario WHERE id_cargo = ? AND nome = ? AND cpf = ? AND email = ? AND endereco = ? AND telefone = ? AND status = ?", [id_cargo, nome, cpf, email, endereco, telefone, status])
        return row_to_dict(cur.description, cur.fetchone())


def db_verificar_comanda(id_cliente, numero_comanda, data_venda, id_operacao, id_situacao, nome):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        # Verificar se já existe uma comanda com id_situacao = 1
        cur.execute("SELECT id_comanda FROM comanda WHERE id_cliente = ? AND numero_comanda = ? AND id_situacao = 1", 
                    [id_cliente, numero_comanda])

        # Se encontrar uma comanda com id_situacao = 1, bloquear a criação
        comanda_existente = cur.fetchone()
        if comanda_existente:
            return {"erro": "Comanda não pode ser criada. Já existe uma comanda com a situação ativa (id_situacao = 1)."}

        # Continuar com a criação se a situação não for 1
        cur.execute("SELECT id_comanda, id_cliente, numero_comanda, data_venda, id_operacao, id_situacao, id_funcionario "
                    "FROM comanda WHERE id_cliente = ? AND numero_comanda = ? AND data_venda = ? AND id_operacao = ? AND id_situacao = ? AND id_funcionario = ?",
                    [id_cliente, numero_comanda, data_venda, id_operacao, id_situacao, nome])
        
        return row_to_dict(cur.description, cur.fetchone())


def verificar_comanda_aberta(comanda_numero):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT comanda.id_comanda, comanda.numero_comanda,comanda.data_venda, cliente.nome AS nome_cliente, situacao.nome AS situacao,funcionario.nome AS nome_funcionario,operacao.nome AS operacao FROM  comanda INNER JOIN  situacao ON comanda.id_situacao = situacao.id_situacao INNER JOIN cliente ON comanda.id_cliente = cliente.id_cliente INNER JOIN     funcionario ON comanda.id_funcionario = funcionario.id_funcionario INNER JOIN     operacao ON comanda.id_operacao = operacao.id_operacao WHERE situacao.nome = 'Aberto' AND comanda.numero_comanda = ?", [comanda_numero])
        resultado = row_to_dict(cur.description, cur.fetchone())
        if resultado:
            situacao = resultado["situacao"]
            return situacao == 'Aberto'  # Retorna True se estiver aberta
        else:
            return False  # Comanda não encontrada


def db_verificar_additems(id_comanda, id_servico, quantidade, id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_comanda, id_servico, quantidade, id_funcionario FROM addItems WHERE id_comanda = ? and id_servico = ? and quantidade = ? and id_funcionario = ?", [id_comanda, id_servico, quantidade, id_funcionario])
        return row_to_dict(cur.description, cur.fetchone())
    

def db_verificar_comanda_fechada(id_comanda, forma_pagamento, desconto, valor_total):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_comanda, forma_pagamento, desconto, valor_total FROM comandaFechada WHERE id_comanda = ? and forma_pagamento = ? and desconto = ? and valor_total = ?", [id_comanda, forma_pagamento, desconto, valor_total])
        return row_to_dict(cur.description, cur.fetchone())
    


def db_verifica_additem(id_comanda):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_comanda, id_servico, quantidade, id_funcionario FROM addItems WHERE id_comanda = ? ", [id_comanda])
        return row_to_dict(cur.description, cur.fetchone())

def db_verificar_num_comanda(numero_comanda):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cliente, id_comanda, numero_comanda FROM comanda WHERE id_situacao = 1 AND numero_comanda = ?",[numero_comanda])
        return row_to_dict(cur.description, cur.fetchone())


####################################################################################################

def db_criar_cliente(nome, telefone):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO cliente (nome, telefone) VALUES (?, ?)", [nome,telefone])
        id_cliente = cur.lastrowid
        con.commit()
        return {'id_cliente': id_cliente, 'nome': nome, 'telefone':telefone}


def db_criar_admin(nome, email, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO tb_admin (nome, email, senha) VALUES (?, ?, ?)", [nome, email, senha])
        id_admin = cur.lastrowid
        con.commit()
        return {'id_admin': id_admin, 'nome': nome, 'email': email, 'senha':senha}


def db_criar_agendamento(data1,hora, id_cliente, id_servico, id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO agendamento (data1,hora, id_cliente, id_servico, id_funcionario) VALUES (?, ?, ?, ?, ?)", [data1,hora, id_cliente, id_servico, id_funcionario])
        id_agendamento = cur.lastrowid
        con.commit()
        return {'id_agendamento':id_agendamento, 'data1':data1, 'hora':hora, 'id_cliente':id_cliente, 'id_servico':id_servico, 'id_funcionario':id_funcionario}


def db_criar_atendimento(id_cliente, valor_unitario, desconto, valor_total, id_forma_pagamento, descricao,data):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO atendimento (id_cliente, valor_unitario, desconto, valor_total, id_forma_pagamento, descricao, data) VALUES (?, ?, ?, ?, ?, ?, ?)", [id_cliente, valor_unitario, desconto, valor_total, id_forma_pagamento, descricao, data])
        id_atendimento = cur.lastrowid
        con.commit()
        return {'id_atendimento':id_atendimento, 'id_cliente':id_cliente, 'valor_unitario':valor_unitario, 'desconto':desconto, 'valor_total':valor_total, 'id_forma_pagamento':id_forma_pagamento, 'descricao': descricao, 'data': data}


def db_criar_servico(nome_servico, preco_servico, duracao_servico, status, id_cargo):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO servico (nome_servico, preco_servico, duracao_servico, status, id_cargo) VALUES (?, ?, ?, ?,?)", [nome_servico, preco_servico, duracao_servico, status, id_cargo])
        id_servico = cur.lastrowid
        con.commit()
        return {'id_servico':id_servico, 'nome_servico':nome_servico, 'preco_servico':preco_servico, 'duracao_servico':duracao_servico, 'status':status, 'id_cargo':id_cargo}


def db_criar_servico_funcionario(i, id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO servico_funcionario (id_servico, id_funcionario) VALUES (?, ?)", [i, id_funcionario])
        id_servico_funcionario = cur.lastrowid
        con.commit()
        return {'id_servico_funcionario':id_servico_funcionario, 'id_servico':i, 'id_funcinario':id_funcionario}


def db_criar_funcionario(id_cargo, nome, cpf, email, endereco, telefone, status):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO funcionario (id_cargo, nome, cpf, email, endereco, telefone, status) VALUES (?, ?, ?, ?, ?, ?, ?)", [id_cargo, nome, cpf, email, endereco, telefone, status])
        id_funcionario = cur.lastrowid
        con.commit()
        return {'id_funcionario':id_funcionario, 'id_cargo':id_cargo, 'nome':nome, 'cpf':cpf, 'email':email, 'endereco':endereco, 'telefone':telefone}


def db_criar_cargo(nome_cargo):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO cargo(nome_cargo) VALUES (?)", [nome_cargo])
        id_cargo = cur.lastrowid
        con.commit()
        return {'id_cargo':id_cargo,'nome_cargo':nome_cargo}


def db_criar_comanda(id_cliente, numero_comanda, data_venda, id_operacao, id_situacao, id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO comanda (id_cliente, numero_comanda, data_venda, id_operacao, id_situacao, id_funcionario) VALUES (?, ?, ?, ?, ?, ?)", [id_cliente, numero_comanda, data_venda, id_operacao, id_situacao, id_funcionario])
        id_comanda = cur.lastrowid
        con.commit()
        return {'id_comanda':id_comanda, 'id_cliente':id_cliente, 'numero_comanda':numero_comanda, 'data_venda':data_venda, 'id_operacao':id_operacao, 'id_situacao':id_situacao, 'id_funcionario':id_funcionario}


def db_criar_saida(data, descricao, valor, observacao):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO saida (data, descricao, valor_total, observacao) VALUES (?, ?, ?, ?)", [data, descricao, valor, observacao])
        id_saida = cur.lastrowid
        con.commit()
        return {'id_saida':id_saida, 'data':data, 'descricao':descricao, 'valor_total':valor, 'observacao':observacao}





def db_criar_additems(id_comanda, id_servico, quantidade, id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO addItems (id_comanda, id_servico, quantidade, id_funcionario) VALUES (?, ?, ?, ?)", [id_comanda, id_servico, quantidade, id_funcionario])
        id_item_comanda = cur.lastrowid
        con.commit()
        return {'id_item_comanda': id_item_comanda, 'id_comanda':id_comanda, 'id_servico':id_servico, 'quantidade':quantidade, 'id_funcionario':id_funcionario}


def db_criar_comanda_fechada(id_comanda, forma_pagamento, desconto, valor_total):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO comandaFechada (id_comanda, forma_pagamento, desconto, valor_total) VALUES (?, ?, ?, ?)", [id_comanda, forma_pagamento, desconto, valor_total])
        id_comanda_fechada = cur.lastrowid
        con.commit()
        return {'id_comanda_fechada': id_comanda_fechada, 'id_comanda':id_comanda, 'forma_pagamento':forma_pagamento, 'desconto':desconto, 'valor_total':valor_total}


def db_fazer_login_admin(email, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT email, senha, nome FROM tb_admin WHERE email = ? AND senha = ?", [email, senha])
        return row_to_dict(cur.description, cur.fetchone())



def db_consultar_agendamento(id_agendamento):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT a.id_agendamento, c.nome AS nome_cliente, c.id_cliente, a.data1, a.hora, s.nome_servico, s.id_servico, s.preco_servico, f.id_funcionario, f.nome AS nome_funcionario FROM cliente AS c LEFT JOIN agendamento AS a ON c.id_cliente = a.id_cliente LEFT join servico as s ON a.id_servico = s.id_servico LEFT join funcionario as f on f.id_funcionario = a.id_funcionario where a.id_agendamento = ?",[id_agendamento])
        return row_to_dict(cur.description, cur.fetchone())

def db_consultar_servico(id_servico):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM servico WHERE id_servico = ?",[id_servico])
        return row_to_dict(cur.description, cur.fetchone())

def db_consultar_funcionario(id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT f.id_funcionario, f.nome, f.email, f.endereco, f.telefone, f.cpf, cg.nome_cargo, f.status, cg.id_cargo FROM funcionario AS f inner join cargo As cg ON f.id_cargo = cg.id_cargo  where f.id_funcionario = ?",[id_funcionario])
        return row_to_dict(cur.description, cur.fetchone())


def db_historico_cliente(nome_cliente):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cliente, nome, telefone FROM cliente WHERE nome LIKE '%"+nome_cliente+"%' ORDER BY id_cliente")
        return rows_to_dict(cur.description, cur.fetchall())
    
    
def db_historico_atendimento(nome):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT a.id_atendimento, a.data, c.nome, a.valor_unitario, a.descricao, a.desconto, a.valor_total, f.nome as forma_pagamento FROM atendimento as a INNER JOIN cliente as c ON a.id_cliente = c.id_cliente INNER JOIN forma_pagamento as f ON f.id_forma_pagamento = a.id_forma_pagamento WHERE c.nome LIKE '%"+nome+"%' ORDER BY a.data ")
        return rows_to_dict(cur.description, cur.fetchall())


def db_trazer_historico_atendimento(data):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT a.id_atendimento, a.data, c.nome, a.valor_unitario, a.descricao, a.desconto, a.valor_total, f.nome as forma_pagamento FROM atendimento as a INNER JOIN cliente as c ON a.id_cliente = c.id_cliente INNER JOIN forma_pagamento as f ON f.id_forma_pagamento = a.id_forma_pagamento WHERE a.data = ?",[data])
        return rows_to_dict(cur.description, cur.fetchall())
    
    
def db_trazer_historico_atendimento_mes_ano(m,Y):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT a.id_atendimento, a.data, c.nome, a.valor_unitario, a.descricao, a.desconto, a.valor_total, f.nome as forma_pagamento FROM atendimento as a INNER JOIN cliente as c ON a.id_cliente = c.id_cliente INNER JOIN forma_pagamento as f ON f.id_forma_pagamento = a.id_forma_pagamento WHERE strftime('%m', a.data) = ? AND strftime('%Y', a.data) = ?",[f"{int(m):02}", str(Y)])
        results = rows_to_dict(cur.description, cur.fetchall())
        for result in results:
            result['data'] = converter_data(result['data'])
        return results
    

 
def db_listar_saida(data):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM saida WHERE data = ?",[data])
        return rows_to_dict(cur.description, cur.fetchall())
    

def db_listar_saida_mes_ano2(m,Y):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("""SELECT * FROM saida WHERE strftime('%m', data) = ? AND strftime('%Y', data) = ?""",[f"{int(m):02}", str(Y)])
        return rows_to_dict(cur.description, cur.fetchall())
    
    
def db_historico_saida333(m,Y):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        query = """
        SELECT SUM(valor_total) as tt FROM saida
        WHERE strftime('%m', data) = ? AND strftime('%Y', data) = ?
        """
        cur.execute(query, [f"{int(m):02}", str(Y)])
        return rows_to_dict(cur.description, cur.fetchall())
    # with closing(conectar()) as con, closing(con.cursor()) as cur:
    #     cur.execute("SELECT SUM(valor_total) as tt FROM saida WHERE data = ?", [nome])
    #     return rows_to_dict(cur.description, cur.fetchall())
    
    
def db_listar_saida2():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM saida")
        return rows_to_dict(cur.description, cur.fetchall())
    
    
def db_listar_saida_mes_ano(data_inicial, data_fim):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT SUM(valor_total) as tt FROM saida WHERE data BETWEEN ? and ?",[date(data_inicial[0],data_inicial[1],data_inicial[2]), date(data_fim[0], data_fim[1],data_fim[2])])
        return rows_to_dict(cur.description, cur.fetchall())
    
    
    
def db_historico_entrada_saida(data_inicial, data_fim):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT SUM(a.valor_total) as tt FROM atendimento as a INNER JOIN cliente as c ON a.id_cliente = c.id_cliente INNER JOIN forma_pagamento as f ON f.id_forma_pagamento = a.id_forma_pagamento WHERE a.data BETWEEN ? and ?",[date(data_inicial[0],data_inicial[1],data_inicial[2]), date(data_fim[0], data_fim[1],data_fim[2])])
        return rows_to_dict(cur.description, cur.fetchall())
    
       
    
def db_historico_entrada(data):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT SUM(a.valor_total) as tt FROM atendimento as a INNER JOIN cliente as c ON a.id_cliente = c.id_cliente INNER JOIN forma_pagamento as f ON f.id_forma_pagamento = a.id_forma_pagamento WHERE a.data = ?",[data])
        return rows_to_dict(cur.description, cur.fetchall())
    

def db_historico_entrada_mes_ano(m,Y):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("""SELECT SUM(a.valor_total) as tt FROM atendimento as a INNER JOIN cliente as c ON a.id_cliente = c.id_cliente INNER JOIN forma_pagamento as f ON f.id_forma_pagamento = a.id_forma_pagamento WHERE strftime('%m', data) = ? AND strftime('%Y', data) = ?""",[f"{int(m):02}", str(Y)])
        return rows_to_dict(cur.description, cur.fetchall())
    



    
def db_historico_saida(nome):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT SUM(valor_total) as tt FROM saida WHERE data = ?", [nome])
        return rows_to_dict(cur.description, cur.fetchall())
    
    
def cosultaEntrada(nome):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT a.id_atendimento, a.data, c.nome, a.valor_unitario, a.descricao, a.desconto, a.valor_total, f.nome as forma_pagamento FROM atendimento as a INNER JOIN cliente as c ON a.id_cliente = c.id_cliente INNER JOIN forma_pagamento as f ON f.id_forma_pagamento = a.id_forma_pagamento WHERE a.data = ?",[nome])
        return rows_to_dict(cur.description, cur.fetchall())
    

def ver_comanda_fechar(id_comanda):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT c.nome, co.numero_comanda, s.nome_servico, ad.quantidade, s.preco_servico as valor_unitario FROM addItems as ad INNER JOIN servico AS s ON ad.id_servico = s.id_servico INNER JOIN comanda AS co ON ad.id_comanda = co.id_comanda INNER JOIN cliente AS c ON c.id_cliente = co.id_cliente WHERE ad.id_comanda = ?",[id_comanda])
        return rows_to_dict(cur.description, cur.fetchall())
    

def db_historico_funcionario():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT f.id_funcionario, f.nome, f.email, f.endereco, f.telefone, f.cpf, cg.nome_cargo, f.status FROM funcionario AS f inner join cargo As cg ON f.id_cargo = cg.id_cargo")
        return rows_to_dict(cur.description, cur.fetchall())
    
    

def db_agenda(data_agendamento):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT c.nome AS nome_cliente, a.data1, a.hora, s.nome_servico, s.preco_servico, f.nome AS nome_funcionario, a.id_agendamento FROM cliente AS c INNER JOIN agendamento AS a ON c.id_cliente = a.id_cliente LEFT join servico as s ON a.id_servico = s.id_servico LEFT join funcionario as f on f.id_funcionario = a.id_funcionario where a.data1 = ?",[data_agendamento])
        return rows_to_dict(cur.description, cur.fetchall())
    

def db_agenda_cliente(nome_cliente):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT c.nome AS nome_cliente, a.data1, a.hora, s.nome_servico, s.preco_servico, f.nome AS nome_funcionario, a.id_agendamento FROM cliente AS c INNER JOIN agendamento AS a ON c.id_cliente = a.id_cliente LEFT join servico as s ON a.id_servico = s.id_servico LEFT join funcionario as f on f.id_funcionario = a.id_funcionario where nome_cliente LIKE '%"+nome_cliente+"%' ORDER BY a.data1 DESC")
        return rows_to_dict(cur.description, cur.fetchall())



def db_meu_agendamento(nome_cliente, data_agendamento):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT c.nome AS nome_cliente, a.data1, a.hora, s.nome_servico, s.preco_servico, f.nome AS nome_funcionario, a.id_agendamento FROM cliente AS c INNER JOIN agendamento AS a ON c.id_cliente = a.id_cliente LEFT join servico as s ON a.id_servico = s.id_servico LEFT join funcionario as f on f.id_funcionario = a.id_funcionario where nome_cliente = ? AND a.data1 = ?",[nome_cliente, data_agendamento])
        return rows_to_dict(cur.description, cur.fetchall())
    

def db_meu_cliente(id_cliente, nome):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cliente, nome FROM cliente WHERE id_cliente = ? AND nome = ?",[id_cliente, nome])
        return rows_to_dict(cur.description, cur.fetchall())


def db_listar_funcionarios():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM funcionario")
        return rows_to_dict(cur.description, cur.fetchall())
    

def db_listar_nome_funcionario(nome):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_funcionario, nome, cpf, email, endereco, telefone, id_cargo, status FROM funcionario WHERE  nome LIKE '%"+nome+"%'")
        return rows_to_dict(cur.description, cur.fetchall())
    
    
def db_listar_atendimento():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT a.id_atendimento, a.data, c.nome, a.valor_unitario, a.descricao, a.desconto, a.valor_total, f.nome as forma_pagamento FROM atendimento as a INNER JOIN cliente as c ON a.id_cliente = c.id_cliente INNER JOIN forma_pagamento as f ON f.id_forma_pagamento = a.id_forma_pagamento ORDER BY a.data ASC")
        return rows_to_dict(cur.description, cur.fetchall())
 
 

def db_listar_agendamentos():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_agendamento, data1, hora, id_cliente, id_servico, id_funcionario FROM agendamento")
        return rows_to_dict(cur.description, cur.fetchall())
    
def db_listar_forma_pagamento():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_forma_pagamento, nome FROM forma_pagamento")
        return rows_to_dict(cur.description, cur.fetchall())

def db_listar_cliente():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cliente, nome, telefone FROM cliente ORDER BY id_cliente")
        return rows_to_dict(cur.description, cur.fetchall())


def db_listar_servico():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_servico, nome_servico, preco_servico, duracao_servico, status, id_cargo FROM servico")
        return rows_to_dict(cur.description, cur.fetchall())
    
    
def db_listar_nome_servico(servico):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_servico, nome_servico, preco_servico, duracao_servico, status FROM servico WHERE  nome_servico LIKE '%"+servico+"%' ")
        return rows_to_dict(cur.description, cur.fetchall())


def db_listar_servico_cargo():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT s.nome_servico, s.preco_servico, s.duracao_servico, c.nome_cargo, s.status FROM servico as s INNER join cargo as c ON c.id_cargo = s.id_cargo")
        return rows_to_dict(cur.description, cur.fetchall())


def db_listar_cargo():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cargo, nome_cargo FROM cargo")
        return rows_to_dict(cur.description, cur.fetchall())


def db_listar_operacao():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_operacao, nome FROM operacao")
        return rows_to_dict(cur.description, cur.fetchall())

def db_listar_situacao():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_situacao, nome FROM situacao")
        return rows_to_dict(cur.description, cur.fetchall())


def db_trazer_ultimo_id_servico():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM servico ORDER BY id_servico DESC LIMIT 1")
        return row_to_dict(cur.description, cur.fetchone())



def db_deletar_agendamento(id_agendamento):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM agendamento WHERE id_agendamento = ?", [id_agendamento])
        con.commit()

def db_deletar_funcionario(id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM funcionario WHERE id_funcionario = ?", [id_funcionario])
        con.commit()
        
def db_deletar_atendimento(id_atendimento):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM atendimento WHERE id_atendimento = ?", [id_atendimento])
        con.commit()
        
        
def db_deletar_cliente(id_cliente):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM cliente WHERE id_cliente = ?", [id_cliente])
        con.commit()


def db_deletar_cargo(id_cargo):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM cargo WHERE id_cargo = ?", [id_cargo])
        con.commit()
        
    
def db_deletar_operacao(id_operacao):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM operacao WHERE id_operacao = ?", [id_operacao])
        con.commit()


def db_alterar():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("ALTER TABLE addItems ADD CONSTRAINT PK_add_items PRIMARY KEY(id_comanda,id_servico)")
        con.commit()



def db_editar_agendamento(id_agendamento, data1, hora, id_cliente, id_servico, id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE agendamento SET data1 = ?, hora = ?, id_cliente = ?, id_servico = ?, id_funcionario = ? WHERE id_agendamento = ?", [data1, hora, id_cliente, id_servico, id_funcionario, id_agendamento])
        con.commit()
        return {'id_agendamento':id_agendamento, 'data1': data1, 'hora': hora, 'id_cliente': id_cliente, 'id_servico': id_servico, 'id_funcionario': id_funcionario}
    

def db_editar_servico(id_servico, nome, valor, duracao, status, id_cargo):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE servico SET nome_servico = ?, preco_servico = ?, duracao_servico = ?, status = ?, id_cargo = ? WHERE id_servico = ?", [nome, valor, duracao, status, id_cargo, id_servico])
        id_servico = cur.lastrowid
        con.commit()
        return {'id_servico':id_servico, 'nome_servico': nome, 'preco_servico': valor, 'duracao_servico': duracao, 'status': status, 'id_cargo': id_cargo}
    
    
    
def db_editar_atendimento(id_atendimento, id_cliente, valor_unitario, desconto, valor_total, id_forma_pagamento, descricao,data):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE atendimento SET id_cliente = ? , valor_unitario = ?, desconto = ?, valor_total = ?, id_forma_pagamento = ?, descricao = ?, data = ? WHERE id_atendimento = ?", [id_cliente, valor_unitario, desconto, valor_total, id_forma_pagamento, descricao, data, id_atendimento])
        con.commit()
        return {'id_atendimento':id_atendimento, 'id_cliente':id_cliente, 'valor_unitario':valor_unitario, 'desconto':desconto, 'valor_total':valor_total, 'id_forma_pagamento':id_forma_pagamento, 'descricao': descricao, 'data': data}




def db_editar_funcionario(id_funcionario, nome, email, endereco, cpf, telefone, id_cargo, status):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE funcionario SET id_cargo = ?, nome = ?, cpf = ?, email = ?, endereco = ?, telefone = ?, status = ? WHERE id_funcionario = ?", [id_cargo, nome, cpf, email, endereco, telefone, status, id_funcionario])
        id_funcionario = cur.lastrowid
        con.commit()
        return {'id_funcionario': id_funcionario, 'id_cargo': id_cargo, 'nome': nome, 'cpf': cpf, 'email': email, 'endereco': endereco, 'telefone': telefone, 'status': status}


def db_editar_cliente(id_cliente, nome, telefone):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE cliente SET nome = ?, telefone = ? WHERE id_cliente = ? ", [nome, telefone, id_cliente])
        id_cliente = cur.lastrowid
        con.commit()
        return {'id_cliente':id_cliente, 'nome':nome, 'telefone':telefone}
    


def db_atualizar_comanda(id_situacao, numero_comanda):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE comanda SET id_situacao = ? WHERE numero_comanda = ?", [id_situacao, numero_comanda])
        con.commit()
        return {'id_situacao':id_situacao, 'numero_comanda':numero_comanda}


# def db_alterar_saida():
#     with closing(conectar()) as con, closing(con.cursor()) as cur:
#         cur.execute("DROP TABLE forma_pagamento_antiga;")
#         con.commit()


# def db_alterar_saida2():
#     with closing(conectar()) as con, closing(con.cursor()) as cur:
#        cur.execute("""INSERT INTO cliente (id_cliente, nome, telefone)SELECT id_cliente, nome, telefone FROM cliente_backup;""")
#        con.commit()

         
def db_atualizar_saida(id_saida, data, descricao, valor_total, observacao):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE saida SET data = ?, descricao = ?, valor_total = ?, observacao = ? WHERE id_saida = ?", [data, descricao, valor_total, observacao, id_saida])
        id_saida = cur.lastrowid
        con.commit()
        return {id_saida:'id_saida',data:'data', descricao:'descricao', valor_total:'valor_total', observacao:'observacao'}  
 

def converter_data(data_str):
    data_obj = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
    return data_obj.strftime("%d/%m/%Y")

def obter_id_servico(nome_servico):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_servico FROM servico WHERE nome_servico = ?", [nome_servico])
        resultado = cur.fetchone()
        if resultado:
            return resultado[0]
        return None


def obter_id_funcionario(nome_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_funcionario FROM funcionario WHERE nome = ?", [nome_funcionario,])
        resultado = cur.fetchone()
        if resultado:
            return resultado[0]
        return None
    

def obter_id_comanda(numero_comanda):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_comanda FROM comanda WHERE numero_comanda = ? AND id_situacao = 1", [numero_comanda,])
        resultado = cur.fetchone()
        if resultado:
            return resultado[0]
        return None


def obter_historico_atendimento(nome):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT c.numero_comanda, c.data_venda, cf.valor_total, cf.desconto, cf.forma_pagamento, s.nome_servico, ai.quantidade FROM comanda c JOIN cliente cli ON c.id_cliente = cli.id_cliente JOIN comandaFechada cf ON c.id_comanda = cf.id_comanda JOIN addItems ai ON c.id_comanda = ai.id_comanda JOIN servico s ON ai.id_servico = s.id_servico WHERE cli.nome = ? and c.id_situacao = 2 ORDER BY c.data_venda DESC;", [nome])
        return rows_to_dict(cur.description, cur.fetchall())