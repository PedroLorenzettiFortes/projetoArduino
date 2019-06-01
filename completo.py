#!/usr/bin/env python
import email
import imaplib
import smtplib
from email.mime.text import MIMEText
import RPi.GPIO as GPIO         #Importa a biblioteca das GPIO
import time                     #Importa a biblioteca de tempo

def enviar_email():
	smtp_ssl_host = 'smtp.gmail.com'
	smtp_ssl_port = 465
	# username ou email para logar no servidor
	username = 'meuportao289@gmail.com'
	password = 'portao$$289'

	from_addr = 'meuportao289@gmail.com'
	to_addrs = ['victorleandro19@gmail.com']

	# para diferentes formatos de mensagem
	# neste caso usaremos MIMEText para enviar
	# somente texto
	message = MIMEText('Ligue policia 190')
	message['subject'] = 'sensor ativado'
	message['from'] = from_addr
	message['to'] = ', '.join(to_addrs)

	# conectaremos de forma segura usando SSL
	server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
	# para interagir com um servidor externo precisaremos
	# fazer login nele
	server.login(username, password)
	server.sendmail(from_addr, to_addrs, message.as_string())
	server.quit()

def receber_email():
	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login('meuportao289@gmail.com', 'portao$$289')
	mail.list()
	mail.select("inbox") # connect to inbox.

	result, data = mail.search(None, "ALL")

	ids = data[0] # data is a list.
	id_list = ids.split() # ids is a space separated string
	latest_email_id = id_list[-1] # get the latest

	result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID

	raw_email = data[0][1] # here's the body, which is raw text of the whole email
	email_message = email.message_from_string(raw_email)

	print email_message['subject']
	print email_message['To']
	print email.utils.parseaddr(email_message['From']) # for parsing "Yuji Tomita" <yuji@grovemade.com>


GPIO.setmode(GPIO.BOARD)        #Configura o modo de definicao de pinos como BOARD (contagem de pinos da placa)
GPIO.setwarnings(False)         #Desativa os avisos
GPIO.setup(18, GPIO.OUT)        #Configura o pino 18 da placa (GPIO24) como saida para o led nok
GPIO.setup(12, GPIO.OUT)        #Configura o pino 12 da placa (GPIO18) como saida para o led ok
GPIO.setup(22, GPIO.OUT)        #Configura o pino 22 da placa (GPIO25) como saida para o buzzer
GPIO.setup(16, GPIO.IN)         #Configura o pino 16 da placa (GPIO23) como entrada para o sensor
GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)		#Configura o pino 16 da placa (GPIO23) como entrada para telegran

email_enviado = 0               # 0 - email nao enviado      1 - email enviado

while (True):
	if(GPIO.input(32) == 1):
        	if(GPIO.input(16) == 1):
                	GPIO.output(18,1)
			GPIO.output(22,1)
			GPIO.output(12,0)
                	print("SENSOR IDENTIFICOU MOVIMENTACAO ESTRANHA!! Ligue para a policia")
                	time.sleep(1)
                	if(email_enviado == 0):
                        	print("Enviando email")
                        	enviar_email()
                        	email_enviado = 1
        	else:
                	GPIO.output(18,0)
                	GPIO.output(22,0)
                	GPIO.output(12,1)
                	print("Tudo sobre controle")
                	time.sleep(1)
                	email_enviado = 0
	else:
		print("Alarme desativado")
		GPIO.output(18,0)
                GPIO.output(22,0)
		GPIO.output(12,0)
		time.sleep(1)
