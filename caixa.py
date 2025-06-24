import datetime
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

remetente = os.getenv("REMETENTE_EMAIL")
senha = os.getenv("REMETENTE_SENHA")
destinatario = os.getenv("DESTINATARIO_EMAIL")

msg = EmailMessage()
msg['Subject'] = 'Relatório diário'
msg['From'] = remetente
msg['To'] = destinatario
msg.set_content('Segue em anexo o arquivo com o relatório do dia de hoje.')

def enviar_email():

    with open('movimentos-caixa.txt', 'rb') as f:
        conteudo = f.read()
        nome_arquivo = f.name
        msg.add_attachment(conteudo, maintype='text', subtype='plain', filename=nome_arquivo)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(remetente, senha)
        smtp.send_message(msg)

    print("relatório enviado com sucesso.")

def registrar_movimento(tipo, valor, descricao):
    data_hora = datetime.datetime.now().strftime("%d-%m-%Y %H:%M4")
    linha = f"{data_hora} | {tipo.upper()} | R${valor:.2f} | {descricao}\n"

    with open ("movimentos-caixa.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)
    print("Movimento Registrado!")

def historico():
    try:
        with open("movimentos-caixa.txt", "r", encoding="utf-8") as arquivo:
            print("\n- HISTÓRICO DE MOVIMENTOS - ")
            print(arquivo.read())

    except FileNotFoundError:
        print("Nenhum movimento registrado!")

def menu():
    while True:
        print("\n1 - Entrada de caixa")
        print("2 - Saída de caixa")
        print("3 - Historico do caixa")
        print("4 - Sair do programa")
        opcao = input("Escolha uma ação: ")

        if int(opcao) == 1:
            valorr = float(input("Informe o valor de entrada: "))
            descricaoo = input("informe uma descrição para a entrada: ")
            registrar_movimento("entrada",valorr, descricaoo)
            

        elif int(opcao) == 2:
            valorr = float(input("informe o valor de saída: "))
            descricaoo = input("informe uma descricao para a saída: ")
            registrar_movimento("saída", valorr, descricaoo)
           

        elif int(opcao) == 3:
            historico()
            
    
        elif int(opcao) == 4:
            enviar_email()
            print("saindo do programa")
            arquivo = 'movimentos-caixa.txt'
            os.remove(arquivo)
            break

menu()