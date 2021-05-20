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
sitesList = r'C:\Dev\TFG\Sites.txt'
tesseractPath = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
firefoxPath = "C://Program Files//Mozilla Firefox//firefox.exe"
screenshotsPath = r'../Screenshots/'

def compareImages(imgPost, img, x, y, w, h):
    preCrop = img[y:h, x:w]
    postCrop = imgPost[y:h,x:w]
    err = np.sum((preCrop.astype("float") - postCrop.astype("float")) ** 2)
    err /= float(preCrop.shape[0] * preCrop.shape[1])
    return err

def FindAndClick(d, img):
    n_boxes = len(d['level'])
    found_button = False
    for i in range(n_boxes):
        ## Set for matching acceptance words in key_words_accept
            matches = [c for c in key_words_accept if c.lower() == d['text'][i].lower()]
            if  matches:
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                pyautogui.click(x+w/2, y+h/2)

                time.sleep(0.7)
                myScreenshot = pyautogui.screenshot()
                ImagePath = screenshotsPath + 'Temp.png'
                myScreenshot.save(ImagePath)
                imgPost = cv2.imread(ImagePath)
                os.remove(ImagePath)
                if compareImages(imgPost, img, x, y, x+w, y+h) > 0.5:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
                    return True
                
if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = tesseractPath
    
    ## In firefox options -> privacy and security, check the option "Eliminar cookies y datos del sitio cuando cierre Firefox" 
    ## in order to show the consent form each time you access a website
    webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefoxPath))

    ## A file with one webpage per line.
    file = open(sitesList, 'r')
    Lines = file.readlines()
    iterator = 1
    for line in Lines:
        ## new = 0 -> open in same tab
        ## new = 1 -> open in new window
        ## new = 2 -> open in new tab
        webbrowser.get('firefox').open(line, new=1)
        time.sleep(2)
        myScreenshot = pyautogui.screenshot()
        ImagePath = screenshotsPath + 'Temp.png'
        myScreenshot.save(ImagePath)
        img = cv2.imread(ImagePath)
        os.remove(ImagePath)

        d = pytesseract.image_to_data(img, lang='spa+eng', output_type=Output.DICT)
        found = FindAndClick(d, img)

        if not found:
        ## Try with black and white image and if not a binarized one
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            d = pytesseract.image_to_data(gray, lang='spa+eng', output_type=Output.DICT)
            found = FindAndClick(d,img)
            if not found:
                (thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                d = pytesseract.image_to_data(im_bw, lang='spa+eng', output_type=Output.DICT)
                found = FindAndClick(d,img)
                if not found:
                    d = pytesseract.image_to_data(cv2.bitwise_not(im_bw), lang='spa+eng', output_type=Output.DICT)
                    found = FindAndClick(d,img)

        if not found:
        ## Try with other channels like hsv
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hue,sat,val = cv2.split(hsv)
            d = pytesseract.image_to_data(hue, lang='spa+eng', output_type=Output.DICT)
            found = FindAndClick(d,img)
            if not found:
                d = pytesseract.image_to_data(val, lang='spa+eng', output_type=Output.DICT)
                found = FindAndClick(d,img)
        if found: 
            cv2.imwrite(screenshotsPath + '{0}-Found.png'.format(iterator), img)
        else:
            cv2.imwrite(screenshotsPath + '{0}-Error.png'.format(iterator), img)
        iterator+=1

        ## This kills all firefox processes when a site has been visited
        os.system("taskkill /im firefox.exe /f")