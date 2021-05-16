import cv2
import numpy as np
import matplotlib.pyplot as plt 

img=cv2.imread('E:\Documents\TFG\Data\Screenshots\FacebookBanner.png')
# print(img)
img2 = cv2.Canny(img,100,200)
img3 = img > 245
# des = img.copy()
# contour,hier = cv2.findContours(des,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

# for cnt in contour:
#     cv2.drawContours(des,[cnt],0,255,-1)

# gray = cv2.bitwise_not(des)

# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
# res = cv2.morphologyEx(gray,cv2.MORPH_OPEN,kernel)
# res = cv2.bitwise_not(res)
# cv2.erode(res, res, cv2.getStructuringElement(cv2.MorphSh))

cv2.imshow("ll", img3)
cv2.waitKey(0)