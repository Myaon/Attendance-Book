# -*- coding: utf-8 -*-f
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

#ファイルの有無を調べるためのモジュール
import os.path

#パス、ファイル名をfilenameとする
filename = '/home/pi/Desktop/test.csv'

#表のヘッダ
header = 'num,name,now'

#キーボードから入力された文字列を入れる変数
personalData = ''

#ファイルが存在しない場合は、新たに作成してヘッダに書き込む
if not os.path.exists(filename):
    with open(filename,mode = 'w')as f:
        f.write(header+'\n')

#キーボードから入力したデータを書き足す
personalData += input('input yourname')+','

#ファイルをappendモードで開いて文字列を書き込む
with open(filename,mode = 'a')as f:
    f.write("%016X" % idm.value+",")
    f.write(personalData)
    f.write("Attend"+'\n')

#ファイルの内容を表示する
print('\n <the contents of file are ...> \n')
with open (filename,mode = 'r')as f:
    for line in f:
        print(line)