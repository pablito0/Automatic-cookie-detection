import os
import cv2
import pytesseract
import pyautogui
import webbrowser
import time
import datetime
import numpy as np
from pytesseract import Output


key_words_accept = ['Acepto', 'ok','Accept',  'Aceptar','consent', 'Got', 'Agree', 'cerrar', 'close', 'Entendido']
key_words_deny = ['Deny','customize', 'deny', 'Read more', 'Reject', 'Cookie Policy', 'More information', 'Denegar', 'Gestionar', 'gestionar', 'Administrar', 'cookie', 'policy', 'here', 'uso', 'información', 'informacion']
workingDirectory = r'C:\Dev\TFG\Screenshots'

def compareImages(imgPost, img, x, y, w, h):
    preCrop = img[y:h, x:w]
    postCrop = imgPost[y:h,x:w]
    err = np.sum((preCrop.astype("float") - postCrop.astype("float")) ** 2)
    err /= float(preCrop.shape[0] * preCrop.shape[1])
    if err < 0.2:
        return False
    return True

def FindAndClick(d, img):
    n_boxes = len(d['level'])
    found_button = False
    for i in range(n_boxes):
        ## Set for matching acceptance words in key_words_accept
            matches = [c for c in key_words_accept if c.lower() == d['text'][i].lower()]
            if  matches:
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                #pyautogui.click(x+w/2, y+h/2)

                time.sleep(2)
                myScreenshot = pyautogui.screenshot()
                ImagePath = r'C:\Dev\TFG\Screenshots\1.png'
                myScreenshot.save(ImagePath)
                imgPost = cv2.imread(ImagePath)
                if compareImages(imgPost, img, x, y, x+w, y+h):
                    return True
                
if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    webbrowser.register('firefox', None, webbrowser.BackgroundBrowser("C://Program Files//Mozilla Firefox//firefox.exe"))
    file = open(r'C:\Dev\TFG\Amazon.txt', 'r')
    Lines = file.readlines()
    count = 1
    for line in Lines:
        webbrowser.get('firefox').open(line, new=0)
        time.sleep(2)
        myScreenshot = pyautogui.screenshot()
        ImagePath = r'C:\Dev\TFG\Screenshots\0.png'
        myScreenshot.save(ImagePath)
        img = cv2.imread(ImagePath)

        d = pytesseract.image_to_data(img, lang='spa+eng', output_type=Output.DICT)
        found = FindAndClick(d, img)
        if not found:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            d2 = pytesseract.image_to_data(gray, lang='spa+eng', output_type=Output.DICT)
            found = FindAndClick(d2,img)
            if not found:
                (thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                d2 = pytesseract.image_to_data(im_bw, lang='spa+eng', output_type=Output.DICT)
                found = FindAndClick(d2,img)
                if not found:
                    d2 = pytesseract.image_to_data(cv2.bitwise_not(im_bw), lang='spa+eng', output_type=Output.DICT)
                    found = FindAndClick(d2,img)
        if not found:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hue,sat,val = cv2.split(hsv)
            d2 = pytesseract.image_to_data(hue, lang='spa+eng', output_type=Output.DICT)
            found = FindAndClick(d2,img)
            if not found:
                d2 = pytesseract.image_to_data(val, lang='spa+eng', output_type=Output.DICT)
                found = FindAndClick(d2,img)
        cv2.imwrite('./Prova-2/Sample.png', img)