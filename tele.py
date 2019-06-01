import time, datetime
import RPi.GPIO as GPIO
import telepot
from telepot.loop import MessageLoop

led = 26
now = datetime.datetime.now()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 #LED
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, 0) #Off initially

def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    print 'Received: %s' % command

    if 'Ligar' in command:
        message = "Alarme ativado "
        if 'alarme' in command:
            message = message + "com sucesso"
            GPIO.output(led, 1)
            telegram_bot.sendMessage (chat_id, message)

    if 'Desligar' in command:
        message = "Alarme desativado "
        if 'alarme' in command:
            message = message + "com sucesso"
            GPIO.output(led, 0)
            telegram_bot.sendMessage (chat_id, message)

telegram_bot = telepot.Bot('812788093:AAExMbZKwLDp_AHbwlaf7CVn6cWo-ci_tnc')
print (telegram_bot.getMe())

MessageLoop(telegram_bot, action).run_as_thread()
print 'Up and Running....'

while 1:
    time.sleep(10)
