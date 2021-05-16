import os
import cv2
import pytesseract
import pyautogui
from pytesseract import Output


key_words_accept = ['Acepto', 'ok','Accept',  'Aceptar','consent', 'Got', 'Agree', 'cerrar', 'close', 'Entendido']
key_words_deny = ['Deny','customize', 'deny', 'Read more', 'Reject', 'Cookie Policy', 'More information', 'Denegar', 'Gestionar', 'gestionar', 'Administrar', 'cookie', 'policy', 'here', 'uso', 'información', 'informacion']
workingDirectory = r'C:\Dev\TFG\Screenshots'

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images

def findButtons(d, img):
    n_boxes = len(d['level'])
    found_button = False
    for i in range(n_boxes):
            matches = [c for c in key_words_accept if c.lower() == d['text'][i].lower()]
            if  matches:
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
                found_button = True
    return found_button

if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    #images = load_images_from_folder2(workingDirectory)
    images = load_images_from_folder(workingDirectory)
    iterator = 0
    counterfound = 0
    for img in images:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
        #img2 = cv2.dilate(img, kernel)
        #height, width, channels = img.shape
        #img = cv2.resize(img, (int(width/2), int(height/2)))
        ## Config despres de config='--psm 11 --oem 1'
        d = pytesseract.image_to_data(img, lang='spa+eng', output_type=Output.DICT)
        found = findButtons(d, img)
        if not found:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            d2 = pytesseract.image_to_data(gray, lang='spa+eng', output_type=Output.DICT)
            found = findButtons(d2,img)
            if not found:
                (thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                d2 = pytesseract.image_to_data(im_bw, lang='spa+eng', output_type=Output.DICT)
                found = findButtons(d2,img)
                if not found:
                    d2 = pytesseract.image_to_data(cv2.bitwise_not(im_bw), lang='spa+eng', output_type=Output.DICT)
                    found = findButtons(d2,img)
        if not found:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hue,sat,val = cv2.split(hsv)
            d2 = pytesseract.image_to_data(hue, lang='spa+eng', output_type=Output.DICT)
            found = findButtons(d2,img)
            if not found:
                d2 = pytesseract.image_to_data(val, lang='spa+eng', output_type=Output.DICT)
                found = findButtons(d2,img)
        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(4,4))
        #img = cv2.dilate(img, kernel)
        #img = cv2.morphologyEx(img,cv2.MORPH_CLOSE, kernel)
        cv2.imwrite('./Prova-2/Sample{0}.png'.format(iterator), img)
        iterator+=1
        if found:
            counterfound +=1
    print(counterfound/len(images))