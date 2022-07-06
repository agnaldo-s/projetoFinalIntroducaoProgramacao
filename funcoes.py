from ast import Return
from secrets import choice
import sqlite3
from string import ascii_lowercase, ascii_uppercase
from time import sleep, time
import funcoes

def cabecario(txt):
    print("╒"+"═"*48 + "╕")
    print(f"|{txt: ^48}|")
    print("╘"+"═"*48 + "╛")
def not_vazio(txt):
    vlr = input(f"{txt}\n R: ").strip()
    if vlr =="":
        while vlr =="":
            print(f"O {txt.lower()} não pode ser vazio.")
            vlr = input(f"{txt}: R: ").strip()
    return vlr
def opcao(vlr,txt):
    print(f"     {txt:.<39}\033[1;34m {vlr} \033[m")
def sim_nao(txt):
    while True:
        texto = input(txt+" (S/N) \nR: ").upper()
        match texto:
            case "S":
                return texto
            case "N":
                return texto
            case _:
                print("\nInforme somente (S/N)\n")  
def sair():
    import time
    print("\nEncerrando o programa em",end=" ")
    for b in range(3,0,-1): 
        print(f"\033[1;3{b}m{b} \033[m",end=" ")
        time.sleep(0.5) 
    print()               
    exit()
    
def database():
    #conexão com o banco de dados
    global conn, cursor
    try:
        conn = sqlite3.connect("banco_senhas.db")
        cursor = conn.cursor()
        print("Conectado ao servidor")
    except:
        print("Algo deu errado com o servidor")
def create():
    #chamando a função de conecção com o banco de dados
    database()
    #se não existir o banco de dados pessoa e senhas, ele os criará já configurado conforme a pré programado  
       
    query="""
        CREATE TABLE IF NOT EXISTS pessoa (
            id_pessoa INTEGER      PRIMARY KEY AUTOINCREMENT
            NOT NULL,
            nome      STRING (60) NOT NULL,
            sobrenome      STRING (60) NOT NULL,
            email     STRING (60) NOT NULL,
            username  STRING (60) NOT NULL,
            senha     STRING (60) NOT NULL
        );
        CREATE TABLE IF NOT EXISTS senhas (
            id_pessoa  INTEGER       REFERENCES pessoa (id_pessoa) 
            NOT NULL,
            id_senha   INTEGER       PRIMARY KEY AUTOINCREMENT
            NOT NULL,
            nome_senha STRING (60)  NOT NULL,
            senha      STRING (60)  NOT NULL,
            data_hora  DATETIME (60) NOT NULL
        );
    """
    with conn:
        try:
            cursor.executescript(query)
            print('Tabelas criadas')
        except:
            print("Algo deu errado com a criação das tabelas")
def insert_user(nome, sobrenome, email, username, senha):
    
    query = f"""INSERT INTO pessoa 
           (nome, sobrenome, email, username, senha) 
           VALUES ('{nome}', '{sobrenome}', '{email}', '{username}', '{senha}')
           """
    with conn:
        try:
            cursor.execute(query)
            conn.commit()
            print('registro inserido')
        except:
            print("Ouve algo de errado ao registrar o usuário")
def insert_senha(a,b,c):
    import datetime
    query = f"""
        INSERT INTO senhas (id_pessoa,nome_senha, senha, data_hora)
        VALUES({a}, '{b}', '{c}', '{datetime.datetime.today().isoformat()}');
    """
    with conn:
        try:
            cursor.execute(query)
            conn.commit()
            print("Senha salva")
        except:
            print("Algo deu errado")
def verificar_username():
    cont = False
    query = f"""
            SELECT username
            FROM pessoa
        """
    with conn:
        cursor.execute(query)
        data = cursor.fetchall()
    while cont == False:
        username= not_vazio("Usuario")
        if data ==[]:
            cont = True
        for a in data:    
            if a[0].upper() == username.upper():
                print('\nJá existe esse nome de usuário.\n')
                cont = False
                break
            else:
                cont = True
    return username
def encotrar_nome_senhas(id):
    query=f"""  
            SELECT nome_senha
            FROM senhas
            WHERE id_pessoa = '{id}';   
            """
            
    with conn:
        cursor.execute(query)
        data = cursor.fetchall()
        return data
def encontrar_senha(id,n_senha):
    query=f"""  
            SELECT senha
            FROM senhas
            WHERE id_pessoa = '{id}' AND nome_senha = '{n_senha}';   
            """
            
    with conn:
        cursor.execute(query)
        data = cursor.fetchall()
    return data[0][0]
def verificar_email():
    cont = False
    query = f"""
            SELECT email
            FROM pessoa
            """
    with conn:
        cursor.execute(query)
        data = cursor.fetchall()
    while cont == False:
        email= not_vazio("E-mail")
        if data ==[]:
            cont = True
        for a in data:    
            if a[0].upper() == email.upper():
                print('\nJa existe um usuário com esse e-mail.\n')
                cont = False
                break
            else:
                cont = True
    return email
def cadastro():
    import time
    confirmSenha = False
    cabecario("CADASTRO")
    nome =not_vazio("Nome").title()
    sobrenome = not_vazio("Sobrenome").title()
    email = verificar_email()
    username = verificar_username()
    while confirmSenha == False:
        senha = not_vazio("Senha")
        senha1 = not_vazio("Confirme a senha")
        if senha == senha1:
            confirmSenha = True
        else:
            print("As senhas tem que ser iguais")
    insert_user(nome,sobrenome,email,username,senha)
    print("Cadastro inserido com sucesso\nRetornando ao menu principal")
    time.sleep(3)
    menu_principal()
def menu_principal():    
    import time
    cabecario("GERADOR DE SENHAS")
    print("\n","_"*49)
    while True:
        print("\n")
        cabecario("MENU")
        opcao(1,"Entrar")
        opcao(2,"Cadastrar")
        opcao(3,"Sair")
        menu=not_vazio("O que deseja? ")
        match menu:
            case "1":
                login()
            case "2":
                cadastro()
            case "3":
                sair()
            case _:
                print("\nInsira uma opção válida!!")
                time.sleep(2) 
def loca_id(username):
            query = f"""
                SELECT id_pessoa
                FROM pessoa
                WHERE username ='{username}'
            """
            with conn:
                cursor.execute(query)
                data = cursor.fetchall()

            return data[0][0]
def loca_nome(username):
            query = f"""
                SELECT nome
                FROM pessoa
                WHERE username ='{username}'
            """
            with conn:
                cursor.execute(query)
                data = cursor.fetchall()

            return data[0][0]
def menu_senhas(id,nome_usuario,senha):
    import time
    print(f"\n\nBem vindo {nome_usuario}!!\n")
    cabecario("MENU")
    while True:
        print("\nO que você quer fazer?\n ")
        opcao(1,"Gerar nova senha")
        opcao(2,"Consultar senha")
        opcao(3,"Consultar nome das senhas")
        opcao(4,"Deslogar")
        opcao(5,"Encerrar programa")
        resp = not_vazio("")
        match resp:
            case "1":
                gerador_senha(id,nome_usuario,senha)
            case "2":
                funcoes.consulta_senha(id,nome_usuario,senha)
            case "3":
                verificar_nome_senhas(id,nome_usuario,senha)
            case "4":
                menu_principal()
            case "5":
                sair()
            case _:
                print("Informe uma opção válida")
                time.sleep(2)
def login():
    
    #verifica se o usuario está cadastrado, confirma senha e se autenticação acontecer corretamente, 
    # retorna id de cadastro, username e senha
    
    import time
    cont = False
    query = f"""
            SELECT username
            FROM pessoa
        """
    with conn:
        cursor.execute(query)
        data = cursor.fetchall()
    cabecario("LOGIN")
    username= not_vazio("Usuario:")
    for a in data:    
        if a[0] == username:
            senha = not_vazio("Senha:")
            query = f"""
                SELECT senha
                FROM pessoa
                WHERE username ='{username}'
            """
            with conn:
                cursor.execute(query)
                data = cursor.fetchall()
            while True:
                if str(data[0][0]) == senha:
                    menu_senhas(loca_id(username),loca_nome(username), senha)
                if senha != "":
                    print("Senha incorreta.\n")
                time.sleep(1)
                opcao(1, "Inserir nova senha")
                opcao(2, "Retornar ao menu principal")
                opcao(3, "Encerrar o programa")
                rep_senha=input("O que deseja fazer?")
                match rep_senha:
                    case "1":
                        senha = not_vazio("Senha")
                    case "2":
                        menu_principal()
                    case "3":
                        sair()
                    case _ :
                        senha =""
                        print("Informe uma opção válida\n")
                        time.sleep(2)     
    if cont == False:
        print(f"\nNão existe o usuário {username} informado, retornando ao menu principal\n")
        time.sleep(2)
        menu_principal()
def gerador_senha(id,nome_usuario,senha_usuario):
    import string
    import time
    from random import random
    while True:
        carac = ""
        verific = {}
        nome_senha= encotrar_nome_senhas(id)
        if nome_senha ==[]:
            nome_senha=[[""]]
        cabecario("GERAR SENHA")
        while True:
            nome = not_vazio(f"{nome_usuario}, informe o nome com qual deseja armazenar a senha").title()
            for i in nome_senha:
                if nome.upper() == i[0].upper():
                    print(f"{nome_usuario}, {nome} já está em seu banco de dados, informe um nome diferente")
                    time.sleep(2)
                    break
            if nome.upper() != i[0].upper():
                break
        while True:
            try:
                qtd= int(input("Quantos caracteres que a senha deve conter? (MINIMO 4) \nR:  "))
                if qtd >= 4:
                    break
                else:
                    print("A senha deve conter no minimo 4 caracteres\n")
                    time.sleep(2)
            except:
                print("Informe um valor válido")
                time.sleep(3)
                
            
        while True:
            minusculas = sim_nao("Deseja ter letras minúsculas?")
            if minusculas =="S":    
                carac += string.ascii_lowercase
                verific['minusculas']= 0
                
            maiusculas = sim_nao("Deseja ter letras maiúsculas?")
            if maiusculas =="S":    
                carac += string.ascii_uppercase
                verific['maiusculas']= 0
                
            numero = sim_nao("Deseja ter números?")
            if numero =="S":    
                carac += string.digits
                verific['numero']= 0
                
            carac_especiais = sim_nao("Deseja ter caracteres especiais?")
            if carac_especiais =="S":    
                carac+= string.punctuation
                verific['carac_especiais']= 0
            if verific != {}:
                copy_verific = verific.copy()
                while True:
                    senha = ""
                    for i in range(0,qtd):
                        senha += choice(carac)
                    for e in senha:
                        if e in string.ascii_lowercase:
                            verific['minusculas']= 1
                        elif e in string.ascii_uppercase:
                            verific['maiusculas']= 1
                        elif e in string.digits:
                            verific['numero']= 1
                        elif e in string.punctuation:
                            verific['carac_especiais']= 1
                    if len(verific) == sum(verific.values()):
                        salvar=sim_nao(f"A senha gerada foi:\033[1;31m{senha} \033[m, deseja usa-lá no {nome}? ")
                        match salvar:
                                case "S":
                                    insert_senha(id,nome,senha)
                        while True:
                            match salvar:
                                case "S":
                                    print("\nO que deseja fazer?")
                                    opcao(1,"Gerar nova senha")
                                    opcao(2,"Ir para o menu principal")
                                    opcao(3,"Sair para login")
                                    opcao(4, "Encerrar programa")
                                    resp = not_vazio("")
                                    match resp:
                                        case "1":
                                            gerador_senha(id,nome_usuario,senha_usuario)
                                        case "2":
                                            menu_senhas(id,nome_usuario,senha_usuario)
                                        case "3":
                                            menu_principal()
                                        case "4":
                                            sair()
                                        case _:
                                            print("Informe uma opção válida")
                                            time.sleep(2)
                                    
                                case "N":
                                    print("\nO que deseja fazer?")
                                    opcao(1,f"Gerar nova senha para {nome}?")
                                    opcao(2,"Gerar nova senha")
                                    opcao(3,"Ir para o menu principal")
                                    opcao(4,"Sair para login")
                                    opcao(5, "Encerrar programa")
                                    resp = not_vazio("")
                                    match resp:
                                        case "1":
                                            break
                                        case "2":
                                            gerador_senha(id,nome_usuario,senha_usuario)
                                        case "3":
                                            menu_senhas(id,nome_usuario,senha_usuario)
                                        case "4":
                                            menu_principal()
                                        case "5":
                                            sair()
                                        case _:
                                            print("Informe uma opção válida")
                                            time.sleep(2)
                                
                    verific = copy_verific.copy()
            else:
                print("A senha deve conter pelo menos 1 tipo de caracter")
                time.sleep(2)
def verificar_nome_senhas(id,nome_usuario,senha):
    import time
    nome=encotrar_nome_senhas(id)
    cabecario("CONSULTA NOME DE SENHAS SALVAS")
    if nome != []:        
        print(f"{nome_usuario}, as suas senhas salvas são:")
        for i in nome:
            print(i[0])
            time.sleep(0.5)
    elif nome == []:
        print("Você ainda não salvou nenhuma senha")
        
    while True:
        print("O que deseja fazer?")        
        opcao(1,"Consultar senha")
        opcao(2,"Menu")
        opcao(3,"Gerar nova senha")
        resp = not_vazio("")
        match resp:
            case "1":
                time.sleep(2) 
                consulta_senha(id,nome_usuario,senha)
            case "2":
                time.sleep(2) 
                menu_senhas(id,nome_usuario,senha)
            case "3":
                gerador_senha(id,nome_usuario,senha)
            case _:
                print("Informe uma opção válida")
                time.sleep(2)
def consulta_senha(id,nome_usuario,senha):
    import time
    while True:
        cabecario ("CONSULTA DE SENHA")
        nome_senha= not_vazio(f"{nome_usuario}, informe o nome que a senha foi armazenada").title()
        for i in encotrar_nome_senhas(id):
            if nome_senha.upper() == i[0].upper():
                while True:
                    inf_senha=input("Informe a senha do seu usuário: ")
                    if inf_senha == senha:
                        print(f"{nome_senha}= \033[1;31m {encontrar_senha(id,nome_senha)}\033[m")
                        time.sleep(2)
                        
                        while True:
                            print("O que deseja fazer agora?\n")
                            opcao(1,"Consultar outra senha")
                            opcao(2,"Retornar ao menu principa")
                            resp = not_vazio("")
                            match resp:
                                case "1":
                                    consulta_senha(id,nome_usuario,senha)
                                case "2":
                                    menu_senhas(id,nome_usuario,senha)
                                case _:
                                    print("Informe uma opção válida")
                                    time.sleep(2)                                
                                
                    else:
                        while True: 
                            print("Senha incorreta!!")
                            time.sleep(2)
                            print("O que deseja fazer?")
                            opcao(1,"Inserir a senha novamente")
                            opcao(2,"Retornar ao menu principal")
                            resp = not_vazio("R: ")
                            match resp:
                                case "1":
                                    break
                                case "2":
                                    menu_senhas(id,nome_usuario,senha)
                                case _:
                                    print("Informe uma opção válida")
                                    time.sleep(2) 
        else:
             while True: 
                            print("Esse nome de senha não está armazenado")
                            time.sleep(2)
                            print("O que deseja fazer?")
                            opcao(1,"Inserir outro nome de senha")
                            opcao(2,"Gerar nova senha")
                            opcao(3,"Retornar ao menu principal")
                            
                            opcao
                            resp = not_vazio("")
                            match resp:
                                case "1":
                                    break
                                case "2":
                                    time.sleep(2)
                                    funcoes.gerador_senha(id,nome_usuario,senha)
                                case "3":
                                    time.sleep(2)
                                    menu_senhas(id,nome_usuario,senha)
                                case _:
                                    print("Informe uma opção válida")
                                    time.sleep(2)
                                    

create()
menu_principal()                                 



    
                    
    
