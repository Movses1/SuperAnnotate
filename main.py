import json
import random

import numpy as np
import cv2

try:
    file = open('aachen_000000_000019_gtFine_polygons.json',)
    data = json.load(file)
except:
    print('couldn\'t load file')
else:
    print('file loaded')

height = data['imgHeight']
width = data['imgWidth']

######################################################################### Data extraction ^

bluemaskImg = np.ones((height,width,3),np.uint8)*255
fuseImg = np.zeros((height,width,3),np.uint8)
#i=np.ones((2,3,2), np.uint8)
#print(i)

objects = data['objects']

objAmount = {}                         # key is the class/label, value is the amount that class has appeared
usedColors = {}                        # key is the class/label, value is the color prescribed to it

for object in objects:                 # creating Fuse.jpg
    label = object['label']
    objColor = []

    if(label in usedColors):
        objColor = usedColors[object['label']]
        objAmount[label] += 1
    else:
        while True:
            red = random.randint(0,255)
            green = random.randint(0,255)
            blue = random.randint(0,255)
            objColor = [blue, green, red]
            if(not objColor in usedColors.values()):
                break
        usedColors[label] = objColor
        objAmount[label] = 1

    pts = object['polygon']
    npPts = np.array(pts)
    cv2.fillPoly(fuseImg, [npPts], objColor)

cv2.imwrite('Fuse.jpg',fuseImg)

objectColor=70
colVariation = 185/len(objects)

for object in objects:                 # creating Bluemask.jpg
    pts = object['polygon']
    npPts = np.array(pts)
    cv2.fillPoly(bluemaskImg, [npPts], objectColor)
    objectColor += colVariation

cv2.imwrite('C:Bluemask.jpg',bluemaskImg)
