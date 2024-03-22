import cv2
import numpy as np
from copy import deepcopy

class Answer:
    def __init__(self):
        self.imgs=[]
        self.binaryImgs=[]
        self.Dye={0:[0,0,0],
                  1:[255,0,0],
                  2:[0,255,0],
                  3:[0,0,255],
                  4:[255,255,0],
                  5:[0,255,255],
                  6:[255,0,255]}
        for i in range(1,4):
            self.imgs.append(cv2.imread(f'images/img{i}.png'))
    def RgbToBinary(self):
        imgQ1 = deepcopy(self.imgs)
        THRESHOLD = 128.0
        for i in range(3):
            imgQ1[i] = imgQ1[i].astype(np.float32)
            imgQ1[i] = 0.11 * imgQ1[i][:,:,0] + 0.59 * imgQ1[i][:,:,1] + 0.3 * imgQ1[i][:,:,2]
            imgQ1[i] = np.clip(imgQ1[i], 0, 255).astype(np.uint8)
            for x in range(imgQ1[i].shape[0]):
                for y in range(imgQ1[i].shape[1]):
                    if imgQ1[i][x][y] > THRESHOLD:
                        imgQ1[i][x][y] = 255
                    else:
                        imgQ1[i][x][y] = 0
        self.binaryImgs=imgQ1



    def ConnectFour(self):

        def DetectFour(img, x, y):
            minNum = [255]
            if img[x, min(img.shape[1]-1, y+1)] > 0:
                minNum.append(img[x, min(img.shape[1]-1, y+1)])
            if img[x, max(y-1, 0)] > 0:
                minNum.append(img[x, max(y-1, 0)])
            if img[max(0,x-1), y] > 0:
                minNum.append(img[max(0,x-1), y])
            if img[min(x+1, img.shape[0]-1), y] > 0:
                minNum.append(img[min(x+1, img.shape[0]-1), y])
            return np.array(minNum).min()
        

        self.RgbToBinary()
        conv = deepcopy(self.binaryImgs)
        count = 1
        # conv = np.array([[[0,255,0,0,0],[255,255,255,0,255],[255,0,0,255,255]]])
        # print(conv.shape[1])
        for _ in range(2):  
            for i in range(len(conv)):
                flag = False
                
                for x in range(self.imgs[i].shape[0]):
                    for y in range(self.imgs[i].shape[1]):
                        if(conv[i][x][y] != 0):
                            flag = True
                            conv[i][x][y] = count
                            minNum = DetectFour(conv[i], x, y)
                            if(minNum != 255):
                                conv[i][x][y] = minNum
                        else:
                            if(flag):
                                count+=1
                            flag = False
        for i in range(len(conv)):
            for x in range(conv[i].shape[0]):
                for y in range(conv[i].shape[1]):
                    conv[i,x,y]=np.array(self.Dye[conv[i,x,y]])
        print(conv)

        
    def ConnectEight(self):
        pass
if __name__== '__main__':
    Ans = Answer()
    Ans.ConnectFour()

