#!/usr/bin/python
# -*- coding=utf8 -*-
"""
# @Author : Akvicor
# @Created Time : 2021-02-21 19:04:04
# @Description :
"""

import os
import resource
import subprocess
import sys

from PIL import Image
from cnocr import CnOcr
import time


#======================================================

## ==== 必须修改 ==== ##

# 使用命令: adb devices
selected_device = "xxxxxxxx"
# 屏幕分辨率(可通过截图获得)
resolution_x = 3120
resolution_y = 1440

## 屏幕左边界 = 屏幕上边界 = 0
## 屏幕右边界 = resolution_x
## 屏幕下边界 = resolution_y
## 文字在屏幕中的 左边界 上边界 右边界 下边界
## 推荐使用开发者模式精确定位

# 开始行动
resolution_1 = (2730, 1287, 2943, 1342)
# 本次行动配置不可更改
resolution_2 = (1290, 1360, 1790, 1410)
# 接管作战
resolution_3 = (1290, 1270, 1490, 1350)
# 行动结束
resolution_4 = (140, 1170, 850, 1340)
# 理智已恢复
resolution_5 = (1680, 676, 1910, 757)
# 剩余理智
resolution_v1 = (2730, 50, 3000, 110)
# 关卡需要理智
resolution_v2 = (2850, 1355, 2955, 1404)

press_enter = (2750,1330)
press_start = (2480,940)
press_finished = (700,1000)
press_lvup = (600, 740)

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
            os.remove("01.png")
            os.remove("02.png")
            os.remove("03.png")
            #os.remove("v1.png")
            #os.remove("v2.png")
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
            im.close()
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
            #print("Remain: %d"%(val1//val2))
            print("Remain: %d   %d/%d"%(val1//val2, val1, val2))
            if val1 // val2 >= 1:
                p = subprocess.Popen('adb %s shell input tap %d %d'%(sel_device,press_enter[0],press_enter[1]), stdout=subprocess.PIPE, shell=True)
                p.wait()
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


        if run_cnt > 0:
            print("")
            run_cnt = 0
        print("No Action")
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
