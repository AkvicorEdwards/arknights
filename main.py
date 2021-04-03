#!/usr/bin/python
# -*- coding=utf8 -*-
"""
# @Author : Akvicor
# @Created Time : 2021-02-21 19:04:04
# @Description :
"""

import os
import subprocess
import sys

from PIL import Image
from cnocr import CnOcr
import time


#======================================================

## ==== 必须修改 ==== ##

# 使用命令: adb devices
selected_device = "xxxxxxxx"

## 屏幕左边界 = 屏幕上边界 = 0
## 屏幕右边界 = resolution_x
## 屏幕下边界 = resolution_y
## 文字在屏幕中的 左边界 上边界 右边界 下边界
## 推荐使用开发者模式精确定位
Use_Free = False
Use_Pay  = False
Pay_Times = 0
if len(sys.argv) >= 2:
    print("Use Free")
    Use_Free = sys.argv[1] == '1'
if len(sys.argv) >= 4:
    print("Use Pay ", end='')
    Use_Pay = sys.argv[2] == '1'
    Pay_Times = int(sys.argv[3])
    print(Pay_Times)

### ===== 1920x1080 ===== ###
# 屏幕分辨率(可通过截图获得)
resolution_x = 1920
resolution_y = 1080

# 开始行动
resolution_1 = (1670, 960, 1850, 1012)
# 本次行动配置不可更改
resolution_2 = (750, 1010, 1140, 1065)
# 接管作战
resolution_3 = (755, 941, 910, 1015)
# 行动结束
resolution_4 = (40,862 ,605 , 1022)
# 理智已恢复
resolution_5 = (1048, 500, 1231, 556)
# 剩余理智
resolution_v1 = (1679, 33, 1850, 96)
# 关卡需要理智
resolution_v2 = (1770, 1017, 1838, 1059)
# 使用药剂恢复
rec_free = (1100, 136, 1298, 182)
# 剩余至纯源石
rec_pay = (1440, 210, 1660, 250)

press_enter = (1707,975)
press_start = (1640,700)
press_finished = (300,800)
press_lvup = (300, 340)
press_rec = (1633, 860)
### ===== END ===== ###

#======================================================
sel_device = ""
if selected_device != "xxxxxxxx":
    sel_device = "-s %s"%selected_device
    print(sel_device)
ocr = CnOcr()


def main():
    start = time.time()
    loop = time.time()
    run_cnt = 0
    while True:
        try:
            os.remove("00.png")
            pass
        except:
            pass
        p = subprocess.Popen('adb %s shell screencap -p /sdcard/00.png'%sel_device, stdout=subprocess.PIPE, shell=True)
        p.wait()
        time.sleep(1)
        p = subprocess.Popen('adb %s pull /sdcard/00.png 00.png'%sel_device, stdout=subprocess.PIPE, shell=True)
        p.wait()
        time.sleep(1)
        im = Image.open(r"00.png")

        im1 = im.crop(resolution_1)
        im1.save(r"01.png")
        im1.close()
        res = ocr.ocr("01.png")
        n = 0
        for r in res:
            if '开' in r:
                n += 1
            if '始' in r:
                n += 1
        if n == 2:
            imv1 = im.crop(resolution_v1)
            imv1.save(r"v1.png")
            imv1.close()
            res = ocr.ocr("v1.png")
            val1 = 0
            for i in res:
                for j in i:
                    if j == '/':
                        break
                    if j not in "1234567890loOLiI][|)(!}{":
                        continue
                    if j in "LliI][|)(!}{":
                        j = '1'
                    if j in "oO":
                        j = '0'
                    val1 *= 10
                    val1 += int(j)
                break
            imv2 = im.crop(resolution_v2)
            imv2.save(r"v2.png")
            imv2.close()
            res = ocr.ocr("v2.png")
            val2 = 0
            for i in res:
                for j in i:
                    if j == '/':
                        break
                    if j not in "1234567890loOLiI][|)(!}{":
                        continue
                    if j in "LliI][|)(!}{":
                        j = '1'
                    if j in "oO":
                        j = '0'
                    val2 *= 10
                    val2 += int(j)
                break
            if run_cnt > 0:
                print("")
                run_cnt = 0
            print("Remain: %d   %d/%d"%(val1//val2, val1, val2))
            p = subprocess.Popen('adb %s shell input tap %d %d'%(sel_device,press_enter[0],press_enter[1]), stdout=subprocess.PIPE, shell=True)
            p.wait()
            if val1 // val2 >= 1:
                im.close()
                time.sleep(2)
                continue

        im2 = im.crop(resolution_2)
        im2.save(r"02.png")
        im2.close()
        res = ocr.ocr("02.png")
        n = 0
        for r in res:
            if '本' in r:
                n += 1
            if '次' in r:
                n += 1
            if '配' in r:
                n += 1
            if '置' in r:
                n += 1
            if '不' in r:
                n += 1
            if '可' in r:
                n += 1
            if '更' in r:
                n += 1
            if '改' in r:
                n += 1
        if n >= 7:
            if run_cnt > 0:
                print("")
                run_cnt = 0
            print("Start")
            p = subprocess.Popen('adb %s shell input tap %d %d'%(sel_device,press_start[0],press_start[1]), stdout=subprocess.PIPE, shell=True)
            p.wait()
            start = time.time()
            run_cnt = 0
            time.sleep(20)
            im.close()
            continue

        im3 = im.crop(resolution_3)
        im3.save(r"03.png")
        im3.close()
        res = ocr.ocr("03.png")
        n = 0
        for r in res:
            if '接' in r:
                n += 1
            if '管' in r:
                n += 1
            if '作' in r:
                n += 1
            if '战' in r:
                n += 1
        if n >= 3:
            run_cnt += 1
            print("Running %d"%run_cnt, end="\r")
            im.close()
            time.sleep(2)
            continue

        im4 = im.crop(resolution_4)
        im4.save(r"04.png")
        im4.close()
        res = ocr.ocr("04.png")
        n = 0
        for r in res:
            if '结' in r:
                n += 1
            if '束' in r:
                n += 1
        if n == 2:
            if run_cnt > 0:
                print("")
                run_cnt = 0
            print("Finished %ds %ds"%(int(time.time()-start), int(time.time()-loop)))
            loop = time.time()
            p = subprocess.Popen('adb %s shell input tap %d %d'%(sel_device,press_finished[0],press_finished[1]), stdout=subprocess.PIPE, shell=True)
            p.wait()
            im.close()
            time.sleep(3.5)
            continue

        im5 = im.crop(resolution_5)
        im5.save(r"05.png")
        im5.close()
        res = ocr.ocr("05.png")
        n = 0
        for r in res:
            if '理' in r:
                n += 1
            if '智' in r:
                n += 1
            if '已' in r:
                n += 1
            if '恢' in r:
                n += 1
            if '复' in r:
                n += 1
        if n >= 4:
            if run_cnt > 0:
                print("")
                run_cnt = 0
            print("LV UP")
            p = subprocess.Popen('adb %s shell input tap %d %d'%(sel_device,press_lvup[0],press_lvup[1]), stdout=subprocess.PIPE, shell=True)
            p.wait()
            im.close()
            time.sleep(1)
            continue

        if Use_Free or Use_Pay:
            imr1 = im.crop(rec_free)
            imr1.save(r"r1.png")
            imr1.close()
            res = ocr.ocr("r1.png")
            for r in res:
                if '使' in r:
                    n += 1
                if '用' in r:
                    n += 1
                if '药' in r:
                    n += 1
                if '剂' in r:
                    n += 1
                if '恢' in r:
                    n += 1
                if '复' in r:
                    n += 1
            if n >= 5:
                n = 0
                imr2 = im.crop(rec_pay)
                imr2.save(r"r2.png")
                imr2.close()
                res = ocr.ocr("r2.png")
                for r in res:
                    if '剩' in r:
                        n += 1
                    if '余' in r:
                        n += 1
                    if '至' in r:
                        n += 1
                    if '纯' in r:
                        n += 1
                    if '源' in r:
                        n += 1
                    if '石' in r:
                        n += 1
                if n >= 6:
                    global Pay_Times
                    if Pay_Times <= 0:
                        if run_cnt > 0:
                            print("")
                            run_cnt = 0
                        continue
                    Pay_Times -= 1
                    print("Pay", Pay_Times)
                p = subprocess.Popen('adb %s shell input tap %d %d'%(sel_device,press_rec[0],press_rec[1]), stdout=subprocess.PIPE, shell=True)
                p.wait()
                im.close()
                time.sleep(3)
                continue

        if run_cnt > 0:
            print("")
            run_cnt = 0
        im.close()
        time.sleep(2)


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(e)
            time.sleep(5)
            pass
