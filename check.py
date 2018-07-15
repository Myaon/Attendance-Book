# -*- coding:utf-8 -*-
from __future__ import print_function
from ctypes import *

# libpafe.hの77行目で定義
FELICA_POLLING_ANY = 0xffff
if __name__ == '__main__':
    
    libpafe = cdll.LoadLibrary("/usr/local/lib/libpafe.so")

    libpafe.pasori_open.restype = c_void_p
    pasori = libpafe.pasori_open()

    libpafe.pasori_init(pasori)

    libpafe.felica_polling.restype = c_void_p
    felica = libpafe.felica_polling(pasori, FELICA_POLLING_ANY, 0, 0)

    idm = c_ulonglong() #←16桁受けとるために変更
    libpafe.felica_get_idm.restype = c_void_p
    libpafe.felica_get_idm(felica, byref(idm))

    if idm.value == 0:
        # READMEより、felica_polling()使用後はfree()を使う
        # なお、freeは自動的にライブラリに入っているもよう
        libpafe.free(felica)

        libpafe.pasori_close(pasori)
    
    else:
        # IDmは16進表記
        print("%016X" % idm.value) #←16桁表示させるために変更

        # READMEより、felica_polling()使用後はfree()を使う
        # なお、freeは自動的にライブラリに入っているもよう
        libpafe.free(felica)

        libpafe.pasori_close(pasori)

# pandasをpdとして使う
import pandas as pd
# csvデータを二次元行列として取得
csv_data = pd.read_csv('/home/pi/Desktop/test.csv').values.tolist()
# 行列の行数を取得
length = 0
for x in csv_data:
    length += 1
n = 0
while n < length:
    if csv_data[n][0] == str("%016X" % idm.value):
        # 編集したいファイル（元ファイル）を開く
        file = open("test.csv","r")
        # 書き出し用のファイルを開く
        out_file = open("result.csv","a")
        tako = file.readlines()[n+1]
        tako = tako.replace("\n","")
        tako=tako.split(",")
        row = "{},{},{}\n".format(
            tako[0],
            tako[1],
            tako[2]+" OK"
        )
        out_file.write(row)      

        # ２つのファイルを閉じる
        file.close()
        out_file.close()
        n+=1
    else:
        n+=1



#ファイルの内容を表示する
print('\n <the contents of file are ...> \n')
with open ("result.csv",mode = 'r')as f:
    for line in f:
        print(line)