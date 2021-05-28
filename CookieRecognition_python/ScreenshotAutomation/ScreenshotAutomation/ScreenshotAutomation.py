import os
import webbrowser
import pyautogui
import time

webbrowser.register('firefox', None, webbrowser.BackgroundBrowser("C://Program Files//Mozilla Firefox//firefox.exe"))
file = open(r'C:\Dev\TFG\Github\Automatic-cookie-detection\1MillionPages.txt', 'r')
Lines = file.readlines()
count = 100
for line in Lines:
    webbrowser.get('firefox').open(line, new=0)
    time.sleep(6)
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(r'C:\Dev\TFG\Screenshots\{0}.png'.format(count))
    count+=1
