#!/usr/bin/env python

import requests
import cv2
import numpy as np

eps = 2  # величина погрешности аппроксимации
# downloading map from google maps
latitude = 59.8702089
longitude = 29.8649487

try:
    satOutput = open('output_sat.png', 'wb')
except:
    print("Couldn't open file for writing.")
    exit(1)

try:
    satOutput.write(requests.get(
        'https://maps.googleapis.com/maps/api/staticmap?center=' + str(latitude) + ',' + str(longitude) + '&zoom=16' +
        '&size=640x640&scale=1&maptype=roadmap'
        '&style=feature:all|element:labels|visibility:off'
        '&style=feature:all|visibility:off'
        #'&style=feature:landscape.man_made|visibility:on|element:geometry.stroke|color:0xff0000'
        '&style=feature:landscape.man_made|visibility:on|element:geometry.stroke'
        '&style=feature:road|element:geometry|color:0x00ff00'
        '&style=feature:water|element:geometry|color:0x0000ff'
    ).content)
    satOutput.close()
except:
    print("Something terrible happened.")
    exit(1)

try:
    satImage = cv2.imread('output_sat.png', cv2.IMREAD_GRAYSCALE)
except:
    print("Couldn't open the map image.")
    exit(1)

img = cv2.imread('output_sat.png', 0)
ret, thresh = cv2.threshold(img, 127, 255, 0)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


print(len(contours))
# Удаляем незамкнутые контуры
mask = np.ones(len(contours), dtype=bool)
for i in range(len(contours)):
    if cv2.contourArea(contours[i]) < 50:
        mask[i] = False
print(mask)


for i in range(len(contours)):
    contours[i] = cv2.approxPolyDP(contours[i], eps, True)  #Ramer–Douglas–Peucker_algorithm

np.delete(contours, 2, 0)
#cv2.drawContours(satImage, contours, -1, (255,255,255), cv2.FILLED)
#cv2.fillPoly(satImage, contours, (255,255,255))
#cv2.imshow("Map With Contours Added (" + str(latitude) + ',' + str(longitude) + ")", satImage)
#cv2.waitKey()
print(contours)
print(len(contours))
print(contours[0])
exit(0)
