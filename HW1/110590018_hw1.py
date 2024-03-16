import cv2
import numpy as np
from collections import defaultdict
from copy import deepcopy

img = []
for i in range(3):
    img.append(cv2.imread(f'images/img{i+1}.png',cv2.IMREAD_COLOR))
# Q1
def Q1_1():
    imgQ1_1 = deepcopy(img)
    for i in range(3):
        imgQ1_1[i] = imgQ1_1[i].astype(np.float32)
        imgQ1_1[i] = 0.11 * imgQ1_1[i][:,:,0] + 0.59 * imgQ1_1[i][:,:,1] + 0.3 * imgQ1_1[i][:,:,2]
        imgQ1_1[i] = np.clip(imgQ1_1[i], 0, 255).astype(np.uint8)
        cv2.imwrite(f'result/img{i+1}_q1-1.png', imgQ1_1[i])
        

def Q1_2():
    imgQ1_2 = deepcopy(img)
    THRESHOLD = 128.0
    for i in range(3):
        imgQ1_2[i] = imgQ1_2[i].astype(np.float32)
        imgQ1_2[i] = 0.11 * imgQ1_2[i][:,:,0] + 0.59 * imgQ1_2[i][:,:,1] + 0.3 * imgQ1_2[i][:,:,2]
        imgQ1_2[i] = np.clip(imgQ1_2[i], 0, 255).astype(np.uint8)

    
        for x in range(imgQ1_2[i].shape[0]):
            for y in range(imgQ1_2[i].shape[1]):
                if(imgQ1_2[i][x][y]>THRESHOLD):
                    imgQ1_2[i][x][y] = 255
                else:
                    imgQ1_2[i][x][y] = 0
                

        cv2.imwrite(f'result/img{i+1}_q1-2.png', imgQ1_2[i])


def Q1_3():
    MAX_COLORS = 16
    SEGEMENT = 3
    THRESHOLD = 20
    
    imgs = []
    def ColorDistanse(color1, color2, threshold = THRESHOLD):
        if abs(color1[0]-color2[0]) < threshold and abs(color1[1]-color2[1]) < threshold and abs(color1[2]-color2[2]) < threshold:
            return True
        return False
    for i in range(3):
        imgs.append(cv2.imread(f'images/img{i+1}.png'))
    imgs = [img.astype(np.float32) for img in imgs]
    for id, img in enumerate(imgs):
        colorList = []
        for x in range(img.shape[0]//SEGEMENT):
            for y in range(img.shape[1]//SEGEMENT):
                segementPixel = img[SEGEMENT*x:SEGEMENT*(x+1),SEGEMENT*y:SEGEMENT*(y+1)]
                avg = np.mean(segementPixel, axis=(0,1))
                rgb = (avg[0].astype(np.uint16)) << 16 | (avg[1].astype(np.uint16)) << 8 | (avg[2].astype(np.uint16))
                flag = True
                for color in colorList:
                    if(ColorDistanse(color[0], avg, THRESHOLD)):
                        color[1][rgb]+=1
                        flag = False
                        break
                if flag:
                    colorList.append([avg, defaultdict(int)])
                    colorList[-1][1][rgb]+=1
        colorList.sort(key=lambda k:len(k[1]),reverse=True)                
        for color in colorList:
                color[1] = [colorPair[0]
                            for colorPair in sorted(color[1].items(),
                                                    key=lambda x: x[1], reverse=True)[:MAX_COLORS]]
        colors = []
        ListNum = 0
        while len(colors) < MAX_COLORS:
            try:
                colors.append(colorList[ListNum][1][0])
            except:
                ListNum = (ListNum + 1) % len(colorList)
            colorList[ListNum][1].pop(0)
            ListNum = (ListNum + 1) % len(colorList)
        print(f"color : {[hex(color) for color in colors]}")
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                pixel = img[i, j]
                minDiff = float('inf')
                index = -1
                for k in range(len(colors)):
                    r = (colors[k] >> 16) & 0xFF
                    g = (colors[k] >> 8) & 0xFF
                    b = colors[k] & 0xFF
                    diff = abs(
                        pixel[0]-r) + abs(pixel[1]-g) + abs(pixel[2]-b)
                    if diff < minDiff:
                        minDiff = diff
                        index = k
                img[i, j] = [((colors[index] >> 16) & 0xFF), (
                    (colors[index] >> 8) & 0xFF), (colors[index] & 0xFF)]
        # cv2.imwrite(f'result/img{id+1}_q1-3.png', img)
        
            
def Q2_1():
    doubleImage = []
    halfImage = []
    imgQ2_1 = deepcopy(img)
    for i in range(3):
        doubleImage.append(np.zeros((imgQ2_1[i].shape[0]*2, imgQ2_1[i].shape[1]*2,3),dtype=np.uint8))
        for x in range(imgQ2_1[i].shape[0]):
            for y in range(imgQ2_1[i].shape[1]):
                doubleImage[i][x*2, y*2] = imgQ2_1[i][x, y]
                doubleImage[i][x*2, y*2+1] = imgQ2_1[i][x, y]
                doubleImage[i][x*2+1, y*2] = imgQ2_1[i][x, y]
                doubleImage[i][x*2+1, y*2+1] = imgQ2_1[i][x, y]
        
        halfImage.append( np.zeros((imgQ2_1[i].shape[0]//2, imgQ2_1[i].shape[1]//2,3),dtype=np.uint8))
        for x in range(halfImage[i].shape[0]):
            for y in range(halfImage[i].shape[1]):
                halfImage[i][x, y] = imgQ2_1[i][x*2, y*2]

        cv2.imwrite(f'result/img{i+1}_q2-1-double.png', doubleImage[i])
        cv2.imwrite(f'result/img{i+1}_q2-1-half.png', halfImage[i])


def Q2_2():
    SCALE = 2
    imgQ2_2 = deepcopy(img)
    imgQ2_2 = [imgQ2_2[i].astype(np.float32) for i in range(3)]
    doubleImage = []
    halfImage = []
    for i in range(3):
        doubleImage.append(np.zeros((imgQ2_2[i].shape[0]*SCALE, imgQ2_2[i].shape[1]*SCALE,3),dtype=np.uint8))
        for x in range(doubleImage[i].shape[0]):
            for y in range(doubleImage[i].shape[1]):
                
                x1 = x//SCALE
                y1 = y//SCALE
                x2 = x1+1 if x1+1 < imgQ2_2[i].shape[0] else x1
                y2 = y1+1 if y1+1 < imgQ2_2[i].shape[1] else y1
                doubleImage[i][x, y] =imgQ2_2[i][x1, y1]*(SCALE-(x%SCALE))/SCALE * (SCALE-(y%SCALE))/SCALE \
                                    + imgQ2_2[i][x2, y1]*((x%SCALE))/SCALE * (SCALE-(y%SCALE))/SCALE\
                                    + imgQ2_2[i][x1, y2]*(SCALE-(x%SCALE))/SCALE * ((y%SCALE))/SCALE\
                                    + imgQ2_2[i][x2, y2]*((x%SCALE))/SCALE *((y%SCALE))/SCALE
        
        halfImage.append(np.zeros((imgQ2_2[i].shape[0]//SCALE, imgQ2_2[i].shape[1]//SCALE,3),dtype=np.uint8))
        for x in range(halfImage[i].shape[0]):
            for y in range(halfImage[i].shape[1]):
                x1 = x*SCALE
                y1 = y*SCALE
                x2 = x1+1 if x1+1 < imgQ2_2[i].shape[0] else x1
                y2 = y1+1 if y1+1 < imgQ2_2[i].shape[1] else y1
                halfImage[i][x, y] =(imgQ2_2[i][x1, y1]
                                    + imgQ2_2[i][x1, y2]+ imgQ2_2[i][x2, y2]+ imgQ2_2[i][x2, y1])/4
    
        cv2.imwrite(f'result/img{i+1}_q2-2-double.png', doubleImage[i].astype(np.uint8))
        cv2.imwrite(f'result/img{i+1}_q2-2-half.png', halfImage[i].astype(np.uint8))


            


if __name__ == '__main__':
    # Q1_1()
    # Q1_2()
    Q1_3()
    # Q2_1() 
    # Q2_2()   



