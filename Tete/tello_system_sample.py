import tello       
import time
import cv2
import threading
import datetime
import os

from tello_bot import TelloBot
import concurrent.futures



class TelloSystem:
    def __init__(self):

        self.drone = tello.Tello('', 8889, command_timeout=.01)  

        self.current_time = time.time()
        self.pre_time = self.current_time


    def show_window(self):
        time.sleep(0.5)
        while True:
            frame = self.drone.read()
            if frame is None or frame.size == 0:
                continue


            image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            small_image = cv2.resize(image, dsize=(480,360) )

            cv2.imshow('Tello Window', small_image)   


            current_time = time.time()
            if current_time - self.pre_time > 5.0 : 
                self.drone.send_command('command')  
                self.pre_time = current_time         

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        del self.drone


    def initial_message(self, input):
        return {'utt': 'initial command', 'end':False}
 
    def reply(self, input):
        t1 = time.time()
        command = input['utt']

        if 'snapshot' in command:

            self.drone.takeSnapshot()
            return {'utt':'cheese!!', 'end':False}

        if 'end' in command:
            print('...')
            self.drone.land()
            del self.drone
            return{'utt':'end','end':False}

        # if time.time()-t1 > 20:
        #     self.drone.land()
        #     del self.drone #land and kill socket connection
        #     return{'utt':'timeout','end':False} 

        # self.drone.send_command(command)  

        if 'takeoff' in command:
            self.drone.takeoff()
            return {'utt':command, 'end':False}
        if 'land' in command:
            self.drone.land()
            return {'utt':command, 'end':False}

        # if 'flip' in command:
        #     return {"utt":'input diection', "end":False}
        if 'flip' in command:
            self.drone.flip("l")
            return {"utt":command, 'end':False}

        if 'rotate' in command:
            self.drone.rotate_cw(180)
            return{"utt":command,'end':False}
        if 'move' in command:
            self.drone.move('forward',500)
            return{'utt':'command','end':False}

        return {"utt": 'warong command!', "end": False}

if __name__ == "__main__":
    system = TelloSystem()
    bot = TelloBot(system)
    
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    executor.submit(bot.run)
    executor.submit(system.show_window)
  


