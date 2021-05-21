from tello import Tello
import sys
from datetime import datetime
import time
import json

from telegram.ext import Updater, CommandHandler,MessageHandler, Filters
from tello_bot import TelloBot

class TelloSystem:
    
    def __init__(self):
        pass
 
    def initial_message(self, input):
        return {'utt': 'initial command', 'end':False}

    # def command(self, input):

 
    def reply(self, input):
        start_time = str(datetime.now())
        t1 = time.time()
        tello = Tello()
        # command = input['utt']
        while True:

            # command = input("write command:")
            command = input['utt']

            if not command:
                break

            if command != '' and command != '\n':
                command = command.rstrip()

                if command.find('delay') != -1:
                    sec = float(command.partition('delay')[2])
                    print('delay %s' % sec)
                    time.sleep(sec)
                    pass
                else:
                    tello.send_command(command)

            if 'end' in command:
                print('...')
                tello.on_close()
                break

            if time.time()-t1 > 20: #max 20 secs
                tello.send_command('land')
                tello.on_close() #land and kill socket connection
                break

        # if not command:
        #     failure = "command!!!!"
        #     return {"utt":failure,"end":False}

        # if command != '' and command != '\n':
        #     command = command.rstrip()

        #     if command.find('delay') != -1:
        #         sec = float(command.partition('delay')[2])
        #         print('deley %s' % sec)
        #         time.sleep(sec)
        #         pass
        #     else:
                # tello.send_command(command)
        
        # while True:
        #     tello.send_command(command) 
        #     ms = command + " success!!"



            return {"utt": 'ok', "end": False}

 
 
if __name__ == '__main__':
    system = TelloSystem() 
    bot = TelloBot(system)
    bot.run()
    