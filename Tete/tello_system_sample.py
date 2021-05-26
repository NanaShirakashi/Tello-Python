#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tello        # tello.pyをインポート
import time         # time.sleepを使いたいので
import cv2          # OpenCVを使うため
import threading
import datetime
import os

from tello_bot import TelloBot
import concurrent.futures



# メイン関数
class TelloSystem:
    def __init__(self):
        pass
        # Telloクラスを使って，droneというインスタンス(実体)を作る
        self.drone = tello.Tello('', 8889, command_timeout=.01)  

        self.current_time = time.time()  # 現在時刻の保存変数
        self.pre_time = self.current_time


    def show_window(self):
        time.sleep(0.5)
        while True:
            frame = self.drone.read()    # 映像を1フレーム取得
            if frame is None or frame.size == 0:    # 中身がおかしかったら無視
                continue

            # (B)ここから画像処理
            image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            small_image = cv2.resize(image, dsize=(480,360) )   # 画像サイズを半分に変更


                    # (X)ウィンドウに表示
            cv2.imshow('Tello Window', small_image)    # ウィンドウに表示するイメージを変えれば色々表示できる

                    # (Z)5秒おきに'command'を送って、死活チェックを通す
            current_time = time.time()  # 現在時刻を取得
            if current_time - self.pre_time > 5.0 : 
                self.drone.send_command('command')   # 'command'送信
                self.pre_time = current_time         # 前回時刻を更新

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

        if time.time()-t1 > 20:
            self.drone.land()
            del self.drone #land and kill socket connection
            return{'utt':'timeout','end':False} 

        # self.drone.send_command(command)  

        if 'takeoff' in command:
            self.drone.takeoff()
        if 'land' in command:
            self.drone.land()

        if 'flip' in command:
            return {"utt":'input diection', "end":False}
        if 'flip l' in command:
            self.drone.flip(l)

        return {"utt": 'Done!', "end": False}

if __name__ == "__main__":
    system = TelloSystem()
    bot = TelloBot(system)
    
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    executor.submit(bot.run)
    executor.submit(system.show_window)
  


