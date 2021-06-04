import tello       
import time
import cv2
import threading
import datetime
import os
from glob import glob
import torch
import torchvision
import numpy as np


from tello_bot import TelloBot
import concurrent.futures
from tello_detect import TelloDetect
from PyTorch_YOLOv3.models import *



class TelloSystem:
    def __init__(self, model):

        self.drone = tello.Tello('', 8889, command_timeout=.01)  
        self.model = model
        self.current_time = time.time()
        self.pre_time = self.current_time


    def show_window(self):
        time.sleep(0.5)
        while True:
            frame = self.drone.read()
            if frame is None or frame.size == 0:
                continue


            image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            small_image = cv2.resize(image, dsize=(600,450) )

            cv2.imshow('Tello Window', small_image)   


            current_time = time.time()
            if current_time - self.pre_time > 5.0 : 
                self.drone.send_command('command')  
                self.pre_time = current_time         

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # del self.drone
    
    def detect(self):
        
        classes = TelloDetect(self.model)
        classes = "と".join(classes)
        target = os.path.join('/mnt/c/Users/nana/Tello-Python-master/Tete/img/', "*")
        files = [(f, os.path.getmtime(f)) for f in glob(target)]
        img_path = sorted(files, key=lambda files: files[1])[-1]
        img_path = img_path[0]
        os.remove(img_path)
        
        return classes


    def initial_message(self, input):
        return {'utt': 'コマンドを入力してください', 'end':False}
 
    def reply(self, input):
        t1 = time.time()
        command = input['utt']
        message = command + "しました"
        if '離陸' in command:
            self.drone.takeoff()
            # message = command + "しました"
            return {'utt':message, 'end':False}
        if '着陸' in command:
            self.drone.land()
            return {'utt':message, 'end':False}

        if 'フリップ' in command:
            self.drone.flip('r')
            return {"utt":message, 'end':False}

        if '回転' in command:
            self.drone.rotate_cw(360)
            return{"utt":message,'end':False}

        if '移動' in command:
            self.drone.move('back',50)
            return{'utt':command,'end':False}

        if '撮影' in command:
            self.drone.takeSnapshot()
            return {'utt':'cheese!!', 'end':False}

        if '何が見える？' in command:
            classes = self.detect()
            message = classes + "が見えます"
            return { 'utt': message, 'end':False}


        if '終了' in command:
            print('...')
            self.drone.land()
            del self.drone
            return{'utt':message,'end':False}

        # if time.time()-t1 > 20:
        #     self.drone.land()
        #     del self.drone #land and kill socket connection
        #     return{'utt':'timeout','end':False} 

        # self.drone.send_command(command)  
        if 'battery' in command:
            print(self.drone.get_battery())
            return{'utt':str(self.drone.get_battery()),'end':False}



        return {"utt": 'コマンドが間違ってます', "end": False}

def detectmodel():
    weights_path = "./PyTorch-YOLOv3/weights/yolov3.weights"
    model_def = './PyTorch-YOLOv3/config/yolov3.cfg'
    n_cpu = 0
    img_size = 416
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    os.makedirs("output", exist_ok=True)

        # Set up model
    model = Darknet(model_def, img_size=img_size).to(device)

    if weights_path.endswith(".weights"):
            # Load darknet weights
        model.load_darknet_weights(weights_path)
    else:
            # Load checkpoint weights
        model.load_state_dict(torch.load(weights_path))

    model.eval()
    return model

if __name__ == "__main__":
    detectmodel()

    system = TelloSystem(detectmodel())
    bot = TelloBot(system)
    
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    executor.submit(bot.run)
    executor.submit(system.show_window)
  


