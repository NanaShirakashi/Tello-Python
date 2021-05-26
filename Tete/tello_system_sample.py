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
        self.pre_time = self.current_time     # 5秒ごとの'command'送信のための時刻変数

        time.sleep(0.5)     # 通信が安定するまでちょっと待つ

        # while True:

        #      # (A)画像取得
        #     frame = self.drone.read()    # 映像を1フレーム取得
        #     if frame is None or frame.size == 0:    # 中身がおかしかったら無視
        #         continue

        #         # (B)ここから画像処理
        #     image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        #     small_image = cv2.resize(image, dsize=(480,360) )   # 画像サイズを半分に変更


        #         # (X)ウィンドウに表示
        #     cv2.imshow('OpenCV Window', small_image)    # ウィンドウに表示するイメージを変えれば色々表示できる

        #         # (Z)5秒おきに'command'を送って、死活チェックを通す
        #     current_time = time.time()  # 現在時刻を取得
        #     if current_time - pre_time > 5.0 :  # 前回時刻から5秒以上経過しているか？
        #         self.drone.send_command('command')   # 'command'送信
        #         pre_time = current_time         # 前回時刻を更新

        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break

        # telloクラスを削除
        # del self.drone
    # def takeSnapshot(self,frame):
    #     """
    #     save the current frame of the video as a jpg file and put it into outputpath
    #     """

    #     # grab the current timestamp and use it to construct the filename
    #     ts = datetime.datetime.now()
    #     filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))

    #     p = os.path.sep.join((self.outputPath, filename))

    #     # save the file
    #     cv2.imwrite(p, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    #     print("[INFO] saved {}".format(filename))


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
            cv2.imshow('OpenCV Window', small_image)    # ウィンドウに表示するイメージを変えれば色々表示できる

                    # (Z)5秒おきに'command'を送って、死活チェックを通す
            current_time = time.time()  # 現在時刻を取得
            if current_time - self.pre_time > 5.0 :  # 前回時刻から5秒以上経過しているか？
                self.drone.send_command('command')   # 'command'送信
                self.pre_time = current_time         # 前回時刻を更新

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


    def initial_message(self, input):
        return {'utt': 'initial command', 'end':False}

    # def command(self, input):

 
    def reply(self, input):
        # tello = Tello()
        
        # # start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        t1 = time.time()

        # # command = input("write command:")
        command = input['utt']

        # if not command:
        #     return{"utt":'input command',"end":False}

        # # if command != '' and command != '\n':
        # #     command = command.rstrip()

        # #     if command.find('delay') != -1:
        # #         sec = float(command.partition('delay')[2])
        # #         print('delay %s' % sec)
        # #         time.sleep(sec)
        # #         pass
        # #     else:
        # #         # self.send_command(command)
        # #         message = self.send_command(command)

        if 'snapshot' in command:
            self.drone.takeSnapshot()

        if 'takeoff' in command:
            self.drone.takeoff()
        if 'land' in command:
            self.drone.land()

        if 'end' in command:
            print('...')
            self.drone.land()
            return{'utt':'command end','end':False}

        if time.time()-t1 > 20: #max 20 secs
            # self.send_command('land')
            self.drone.land() #land and kill socket connection
            return{'utt':'timeout','end':False} 


        return {"utt": 'Done!', "end": False}

# class TelloWindow():
#     def __init__(self):
#         self.drone = TelloSystem()
#         # self.drone = tello.Tello('', 8889, command_timeout=.01)
#         self.current_time = time.time()  # 現在時刻の保存変数
#         self.pre_time = self.current_time     # 5秒ごとの'command'送信のための時刻変数

#         time.sleep(0.5)

#     def show_window(self):
#         print("hello")
#         time.sleep(0.5)
#         while True:
#             frame = self.drone.read()    # 映像を1フレーム取得
#             if frame is None or frame.size == 0:    # 中身がおかしかったら無視
#                 continue

#                     # (B)ここから画像処理
#             image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
#             small_image = cv2.resize(image, dsize=(480,360) )   # 画像サイズを半分に変更


#                     # (X)ウィンドウに表示
#             cv2.imshow('OpenCV Window', small_image)    # ウィンドウに表示するイメージを変えれば色々表示できる

#                     # (Z)5秒おきに'command'を送って、死活チェックを通す
#             current_time = time.time()  # 現在時刻を取得
#             if current_time - self.pre_time > 5.0 :  # 前回時刻から5秒以上経過しているか？
#                 self.drone.send_command('command')   # 'command'送信
#                 self.pre_time = current_time         # 前回時刻を更新

#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
    



# "python main.py"として実行された時だけ動く様にするおまじない処理
if __name__ == "__main__":

    system = TelloSystem()
    # thread_tello = threading.Thread(target=system.show_window())
    bot = TelloBot(system)
    # thread_bot = threading.Thread(target=bot.run())
    # thread_bot2 = threading.Thread(target=bot.show_window())
    # thread_bot.start()
    # thread_bot2.start()
    # thread_tello.start()
    # bot.run()
    
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    executor.submit(bot.run)
    executor.submit(system.show_window)
  


