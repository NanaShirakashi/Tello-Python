import socket
# from tello import Tello
import sys
from datetime import datetime
import time
import json
from stats import Stats
import threading
from telegram.ext import Updater, CommandHandler,MessageHandler, Filters
from tello_bot import TelloBot



class TelloSystem:
    
    # def __init__(self):
    #     pass
 
    def __init__(self):
        self.local_ip = ''
        self.local_port = 8889
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        self.socket.bind((self.local_ip, self.local_port))

        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.tello_ip = '192.168.10.1'
        self.tello_port = 8889
        self.tello_adderss = (self.tello_ip, self.tello_port)
        self.log = []

        self.MAX_TIME_OUT = 15.0

    def send_command(self, command):
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # with open('log/' + start_time + '.txt', 'w') as f:
        #     f.write()
            
        self.log.append(Stats(command, len(self.log)))

        self.socket.sendto(command.encode('utf-8'), self.tello_adderss)
        print('sending command: %s to %s' % (command, self.tello_ip))

        start = time.time()
        while not self.log[-1].got_response():
            now = time.time()
            diff = now - start
            if diff > self.MAX_TIME_OUT:
                print('Max timeout exceeded... command %s' % command)
                message = 'Max timeout'
                return message
        print('Done!!! sent command: %s to %s' % (command, self.tello_ip))
        message = 'Done'
        return message

    def _receive_thread(self):
        """Listen to responses from the Tello.

        Runs as a thread, sets self.response to whatever the Tello last returned.

        """
        while True:
            try:
                self.response, ip = self.socket.recvfrom(1024)
                print('from %s: %s' % (ip, self.response))

                self.log[-1].add_response(self.response)
            except socket.error as exc:
                print("Caught exception socket.error : %s" % exc)

    def on_close(self):
        # pass
        # for ip in self.tello_ip_list:
        #     self.socket.sendto('land'.encode('utf-8'), (ip, 8889))

        self.socket.sendto('land'.encode('utf-8'), self.tello_adderss)
        # self.socket.close()

    def get_log(self):
        return self.log

    # def get_logfile(self):
    #     start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     with open('log/' + start_time + '.txt', 'a') as f:
    #         for stat in self.get_log:
    #             stat.print_stats()
    #             str = stat.return_stats()
    #             f.write(str)

    #     return          


    def initial_message(self, input):
        return {'utt': 'initial command', 'end':False}

    # def command(self, input):

 
    def reply(self, input):
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        t1 = time.time()

        # command = input("write command:")
        command = input['utt']

        if not command:
            return{"utt":'input command',"end":False}

        if command != '' and command != '\n':
            command = command.rstrip()

            if command.find('delay') != -1:
                sec = float(command.partition('delay')[2])
                print('delay %s' % sec)
                time.sleep(sec)
                pass
            else:
                # self.send_command(command)
                message = self.send_command(command)

        if 'end' in command:
            print('...')
            self.on_close()
            return{'utt':'command end','end':False}

        if time.time()-t1 > 20: #max 20 secs
            self.send_command('land')
            self.on_close() #land and kill socket connection
            return{'utt':'timeout','end':False} 

        # log = self.get_log()

        # with open('log/' + start_time + '.txt', 'a') as f:
        #     for stat in log:
        #         stat.print_stats()
        #         str = stat.return_stats()
        #         f.write(str)   

        return {"utt": message, "end": False}

 
 
if __name__ == '__main__':

    system = TelloSystem() 
    bot = TelloBot(system)
    bot.run()
    # log = self.get_log()
    # start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # with open('log/' + start_time + '.txt', 'a') as f:
    #     for stat in log:
    #         stat.print_stats()
    #         str = stat.return_stats()
    #         f.write(str)     