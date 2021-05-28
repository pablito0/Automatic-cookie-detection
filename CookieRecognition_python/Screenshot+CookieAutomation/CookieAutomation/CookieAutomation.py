import os
import cv2
import pytesseract
import pyautogui
import webbrowser
import time
import datetime
import numpy as np
from pytesseract import Output

key_words_accept_spanish = ['Acepto', 'ok','or','Accept',  'Aceptar','Got',  'cerrar', 'Entendido', 'Entiendo', 'continuar', 'todas', 'Consiento', 'Consentir', 'Sí', 'Si', 'Acuerdo', 'continuar']
key_words_accept = ['Acepto', 'ok','Accept',  'Aceptar','consent', 'Got', 'Agree', 'cerrar', 'close', 'Entendido']
key_words_deny = ['Deny','customize', 'deny', 'Read more', 'Reject', 'Cookie Policy', 'More information', 'Denegar', 'Gestionar', 'gestionar', 'Administrar', 'cookie', 'policy', 'here', 'uso', 'información', 'informacion']
sitesList = r'C:\\Dev\\TFG\\Github\\Automatic-cookie-detection\\CookieRecognition_python\\Screenshot+CookieAutomation\\PaginasEspana.txt'
errorList = r'C:\\Dev\\TFG\\Github\\Automatic-cookie-detection\\CookieRecognition_python\\Screenshot+CookieAutomation\\ErrorSites.txt'
tesseractPath = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
firefoxPath = "C://Program Files//Mozilla Firefox//firefox.exe"
screenshotsPath = r'C:\Dev\TFG\Github\Automatic-cookie-detection\CookieRecognition_python\Screenshot+CookieAutomation\Screenshots'

## Only with grayscale images
def remove_noise_and_smooth(img):
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 41)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = cv2.blur(img, (3,3))
    or_image = cv2.bitwise_or(img, closing)
    return or_image

def compareImages(imgPost, img, x, y, w, h):
    preCrop = img[y:h, x:w]
    postCrop = imgPost[y:h,x:w]
    err = np.sum((preCrop.astype("float") - postCrop.astype("float")) ** 2)
    if err == 0:
        return err
    err /= float(preCrop.shape[0] * preCrop.shape[1])
    return err

def FindAndClick(d, origImg, offsetX, offsetY):
    n_boxes = len(d['level'])
    found_button = False
    for i in range(n_boxes):
        ## Set for matching acceptance words in key_words_accept
            matches = [c for c in key_words_accept_spanish if c.lower() == d['text'][i].lower()]
            if  matches:
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                y = int(y/offsetY)
                h = int(h/offsetY)
                x = int(x/offsetX)
                w = int(w/offsetX)
                pyautogui.click(int(x+w/2), int(y+h/2))

                time.sleep(1)
                myScreenshot = pyautogui.screenshot()
                ImagePath = screenshotsPath + 'Temp.png'
                myScreenshot.save(ImagePath)
                imgPost = cv2.imread(ImagePath)
                os.remove(ImagePath)
                if compareImages(imgPost, origImg, x, y, x+w, y+h) > 0.5:
                    cv2.rectangle(origImg, (x, y), (x + w, y + h), (0, 255, 0), 4)
                    return True
    return False
                
if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = tesseractPath
    
    ## In firefox options -> privacy and security, check the option "Eliminar cookies y datos del sitio cuando cierre Firefox" 
    ## in order to show the consent form each time you access a website
    webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefoxPath))

    ## A file with one webpage per line.
    file = open(sitesList, 'r')
    Lines = file.readlines()
    ErrorIterator = 1
    FoundIterator = 1
    inOrig = inSmooth = inGray = inBW = inInv =0
    for line in Lines:
        ## new = 0 -> open in same tab
        ## new = 1 -> open in new window
        ## new = 2 -> open in new tab
        webbrowser.get('firefox').open(line, new=1)
        time.sleep(6)
        myScreenshot = pyautogui.screenshot()
        ImagePath = screenshotsPath + 'Temp.png'
        myScreenshot.save(ImagePath)
        img = cv2.imread(ImagePath)
        origImg = img;
        dsize = (int(origImg.shape[1]),int(origImg.shape[0])*2)
        dsize2 = (int(origImg.shape[1])*2,int(origImg.shape[0]))
        img = cv2.resize(origImg,dsize)
        img2 = cv2.resize(origImg,dsize2)
        os.remove(ImagePath)

        ## Try with black and white image and if not, a binarized one
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        d = pytesseract.image_to_data(gray, lang='spa+eng', output_type=Output.DICT)
        found = FindAndClick(d,origImg,1,2)
        if not found:
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            d = pytesseract.image_to_data(gray, lang='spa+eng', output_type=Output.DICT)
            found = FindAndClick(d,origImg,2,1)
        if found:
            inGray+=1

        if not found:
            #bw and wb
            (thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            d = pytesseract.image_to_data(cv2.bitwise_not(im_bw), lang='spa+eng', output_type=Output.DICT)
            found = FindAndClick(d,origImg,1,2)
            if found:
                inInv +=1
            if not found:
                d = pytesseract.image_to_data(im_bw, lang='spa+eng', output_type=Output.DICT)
                found = FindAndClick(d,origImg,1,2)
                if found:
                    inBW +=1
        if not found:
            smooth = cv2.blur(img,(4,4))
            d = pytesseract.image_to_data(smooth, lang='spa+eng', output_type=Output.DICT)
            found = FindAndClick(d, origImg,1,2)
            if found:
                inSmooth +=1

        if not found:
            #orig
            d = pytesseract.image_to_data(img, lang='spa+eng', output_type=Output.DICT)
            found = FindAndClick(d, origImg,1,2)
            if found:
                inOrig+=1
        if found: 
            cv2.imwrite(screenshotsPath + '\\Success\\{0}.png'.format(FoundIterator), origImg)
            FoundIterator+=1
        else:
            cv2.imwrite(screenshotsPath + r'\\Error\\{0}.png'.format(ErrorIterator), origImg)
            with open(errorList,'a') as f:
                f.write(line)
                f.close()
            ErrorIterator+=1

        ## This kills all firefox processes when a site has been visited
        pyautogui.click(img.shape[1]-5,5)
        pyautogui.click(int(img.shape[1]/2),5)
        time.sleep(0.5)
    file.close()
    print(inOrig + ' ' + inSmooth + ' ' + inGray  + ' ' + inBW  + ' ' +inInv + ' ' +'\n')