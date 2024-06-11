import numpy as np
from copy import deepcopy
import cv2
import math

class ImageProcessor:
    def __init__(self):
        self.__sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        self.__sobel_y = np.array([[-1, -2, -1], [ 0,  0,  0], [ 1,  2,  1]])

    def Gray(self, img):
        gray_image = deepcopy(img)
        gray_image = gray_image.astype(np.float32)
        gray_image = 0.11 * gray_image[:,:,0] + 0.59 * gray_image[:,:,1] + 0.3 * gray_image[:,:,2]
        gray_image = np.clip(gray_image, 0, 255).astype(np.uint8)
        return gray_image

    def GaussianFilter(self, image, num=1, filter_size=5,sigma=1.1):
        mask = np.zeros((filter_size,filter_size),dtype=np.float64)
        image = self.Gray(image)
        def G(x,y):
            return (1/(2*math.pi*sigma**2)) * math.exp(-(x**2+y**2)/(2*sigma**2))
        for y in range(filter_size):
            for x in range(filter_size):
                mask[y,x] = G((y-filter_size//2),(x-filter_size//2))
        
        pad_size = filter_size // 2
        padding_image = np.pad(image, pad_size, mode='constant', constant_values=0)
        self.__filtered_image = np.zeros_like(image,dtype=np.uint8)

        for y in range(pad_size, padding_image.shape[0] - pad_size):
            for x in range(pad_size, padding_image.shape[1] - pad_size):
                neighborhood = padding_image[y - pad_size:y + pad_size + 1, x - pad_size:x + pad_size + 1]
                value = np.sum(neighborhood * mask, axis=None)
                self.__filtered_image[y - pad_size, x - pad_size] = value

    def Gradient(self):
        filter_size = 3
        pad_size = filter_size // 2
        padding_image = np.pad(self.__filtered_image, pad_size, mode='constant', constant_values=0)
        self.__gradient = np.zeros(self.__filtered_image.shape, dtype=np.float64)
        self.__direction = np.zeros(self.__filtered_image.shape, dtype=np.float64)
        for y in range(pad_size, padding_image.shape[0] - pad_size):
            for x in range(pad_size, padding_image.shape[1] - pad_size):
                self.__gradient[y-pad_size,x-pad_size], self.__direction[y-pad_size,x-pad_size] = self.Sobel(padding_image, y, x)

    def Sobel(self, padding_image, y, x):
        filter_size = 3
        pad_size = filter_size // 2
        neighborhood = padding_image[y - pad_size:y + pad_size + 1, x - pad_size:x + pad_size + 1]
        value_x = np.sum(neighborhood * self.__sobel_x, axis=None)
        value_y = np.sum(neighborhood * self.__sobel_y, axis=None)
        direction = np.arctan2(value_y, value_x) * 180 / np.pi
        magnitude = np.sqrt(value_x**2 + value_y**2)
        return magnitude, direction

    def Suppress_nonMaximum(self):
        rows, cols = self.__gradient.shape
        suppressed = np.zeros((rows, cols), dtype=np.float64)
        angle = self.__direction.copy()
        angle = abs(angle)% 180

        for y in range(1, rows - 1):
            for x in range(1, cols - 1):

                if (0 <= angle[y, x] < 45 or (135 <= angle[y, x] <= 180)):
                    q = self.__gradient[y, x + 1]
                    r = self.__gradient[y, x - 1]
                elif 45 <= angle[y, x] < 90:
                    q = self.__gradient[y + 1, x]
                    r = self.__gradient[y - 1, x]
                elif 90 <= angle[y, x] < 135:
                    q = self.__gradient[y - 1, x - 1]
                    r = self.__gradient[y + 1, x + 1]


                if self.__gradient[y, x] >= q and self.__gradient[y, x] >= r:
                    suppressed[y, x] = self.__gradient[y, x]
                else:
                    suppressed[y, x] = 0

        self.__suppress_image = suppressed

    def Double_threshold(self,high_threshold,low_threshold):

        result = np.zeros_like(self.__suppress_image, dtype=np.uint8)
        result[self.__suppress_image >= high_threshold] = 255
        result[(self.__suppress_image <= high_threshold) & (self.__suppress_image >= low_threshold)] = 50
        cv2.imshow("debug",result)
        cv2.waitKey(0)
        self.__double_threashold = result

    def Edge_tracking_by_hysteresis(self):
        
        img = self.__double_threashold.copy()
        visited = np.zeros_like(img)
        def dfs(q:list):
            while(len(q)>0):
                ner_x,ner_y = q.pop()
                for x in range(-1,2):
                    for y in range(-1,2):
                        if(visited[x+ner_x,y+ner_y]==0 and img[x+ner_x,y+ner_y]==50):
                            visited[x+ner_x,y+ner_y] = 1
                            img[x+ner_x,y+ner_y] = 255
                            q.append((x+ner_x,y+ner_y)) 
        for y in range(1,img.shape[0]-1):
            for x in range(1,img.shape[1]-1):
                if(img[y,x]==255 and visited[y,x]==0):
                    visited[y,x]=1
                    dfs([(y,x)])
        for y in range(1,img.shape[0]-1):
            for x in range(1,img.shape[1]-1):
                if(img[y,x]==50):
                    img[y,x]=0
        self.__result = img

    def Process(self, image,num):
        self.GaussianFilter(image)
        self.Gradient()
        self.Suppress_nonMaximum()
        self.Double_threshold(140,50)
        self.Edge_tracking_by_hysteresis()
        self.Write_image(num)

    def Show(self):
        cv2.imshow("Edges", self.__result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def Write_image(self,num):
        cv2.imwrite(f"results/img{num}_sobel.jpg",self.__result)

if __name__ == "__main__":
    
    processor = ImageProcessor()
    for num in range(1,4):
        img = cv2.imread(f"images/img{num}.jpg")
        processor.Process(img,num)
