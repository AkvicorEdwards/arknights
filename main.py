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


def get_memory():
    with open('/proc/meminfo', 'r') as mem:
        free_memory = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                free_memory += int(sline[1])
    return free_memory


ocr = CnOcr()


def main():

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
        # print("MEM:", get_memory())
        p = subprocess.Popen('adb shell screencap -p /sdcard/00.png', stdout=subprocess.PIPE, shell=True)
        p.wait()
        time.sleep(1)
        p = subprocess.Popen('adb pull /sdcard/00.png 00.png', stdout=subprocess.PIPE, shell=True)
        p.wait()
        time.sleep(1)
        im = Image.open(r"00.png")

        im1 = im.crop((2750, 1287, 2750 + 213, 1287 + 55))
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
            print("select 1")
            imv1 = im.crop((2730, 50, 2890, 110))
            imv1.save(r"v1.png")
            imv1.close()
            res = ocr.ocr("v1.png")
            val1 = 0
            for i in res:
                for j in i:
                    if j not in "1234567890":
                        break
                    val1 *= 10
                    val1 += int(j)
                break
            imv2 = im.crop((2850, 1355, 2955, 1404))
            im.close()
            imv2.save(r"v2.png")
            imv2.close()
            res = ocr.ocr("v2.png")
            val2 = 0
            for i in res:
                for j in i:
                    if j not in "1234567890":
                        continue
                    val2 *= 10
                    val2 += int(j)
                break
            print(val1, val2, val1 // val2)
            if val1 // val2 >= 1:
                p = subprocess.Popen('adb shell input tap 2750 1330', stdout=subprocess.PIPE, shell=True)
                p.wait()
            time.sleep(1.5)
            continue

        im2 = im.crop((1290, 1360, 1790, 1410))
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
            print("select 2")
            p = subprocess.Popen('adb shell input tap 2480 940', stdout=subprocess.PIPE, shell=True)
            p.wait()
            time.sleep(1)
            im.close()
            continue

        im3 = im.crop((140, 1170, 850, 1340))
        im3.save(r"03.png")
        im3.close()
        res = ocr.ocr("03.png")
        n = 0
        for r in res:
            if '结' in r:
                n += 1
            if '束' in r:
                n += 1
        if n == 2:
            print("select 3")
            p = subprocess.Popen('adb shell input tap 700 1000', stdout=subprocess.PIPE, shell=True)
            p.wait()
            im.close()
            time.sleep(1.5)
            continue

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
