#!/usr/bin/env python

import requests
import cv2
import numpy as np
import bpy
import bmesh

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

for i in range(len(contours)):
    contours[i] = cv2.approxPolyDP(contours[i], eps, True)  #Ramer–Douglas–Peucker_algorithm

M = cv2.moments(contours[0])
cX = int(M["m10"] / M["m00"])/10
cY = int(M["m01"] / M["m00"])/10


def create_base(context, contours):
    bm = bmesh.new()
    print(len(contours))
    for cnt in contours:
        print(cnt)
        bm_verts = []
        if (len(cnt)>2):
            for point in range(len(cnt)):
                bm_verts.append(bm.verts.new(((cnt[point][0][0]-320)/5, (cnt[point][0][1]-320)/5, 0)))
            bm.faces.new(bm_verts)

    me = bpy.data.meshes.new(name='MyMesh')
    ob = bpy.data.objects.new(name='MyObject', object_data=me)
    bm.to_mesh(ob.data)
    context.scene.objects.link(ob)
    
create_base(bpy.context, contours)