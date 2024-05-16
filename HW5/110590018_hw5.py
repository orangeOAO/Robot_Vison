import cv2
import numpy as np
import math
import time

class HW5:
    def __init__(self):
        self.padding_image = None
        self.filtered_image = None

    def MeanFilter(self, image,num, filter_size=3):
        pad_size = filter_size // 2
        self.padding_image = np.pad(image, pad_size, mode='constant', constant_values=0)
        self.filtered_image = np.zeros_like(image)
        
        for y in range(pad_size, self.padding_image.shape[0] - pad_size):
            for x in range(pad_size, self.padding_image.shape[1] - pad_size):
                self.filtered_image[y - pad_size, x - pad_size] = np.mean(self.padding_image[y - pad_size:y + pad_size + 1, x - pad_size:x + pad_size + 1])
        cv2.imwrite(f"results/img{num}Q1_{filter_size}.jpg",self.filtered_image)

    def MedianFilter(self, image, num, filter_size=3):
        pad_size = filter_size // 2
        self.padding_image = np.pad(image, pad_size, mode='constant', constant_values=0)
        self.filtered_image = np.zeros_like(image)

        for y in range(pad_size, self.padding_image.shape[0] - pad_size):
            for x in range(pad_size, self.padding_image.shape[1] - pad_size):
                neighborhood = self.padding_image[y - pad_size:y + pad_size + 1, x - pad_size:x + pad_size + 1]
                sorted_array = np.sort(neighborhood, axis=None)
                median_value = sorted_array[filter_size * filter_size // 2]
                self.filtered_image[y - pad_size, x - pad_size] = median_value
        
        # 确保保存时图像在0-255范围内
        output_image = np.clip(self.filtered_image, 0, 255).astype(np.uint8)
        
        cv2.imwrite(f"results/img{num}Q2_{filter_size}.jpg", output_image)
        
    def GaussianFilter(self, image, num, filter_size=3):
        mask = np.zeros((filter_size,filter_size),dtype=np.float64)
        
        def G(x,y):
            return (1/(2*math.pi)) * math.exp(-(x**2+y**2)/2)
        for y in range(filter_size):
            for x in range(filter_size):
                mask[y,x] = G((y-filter_size//2),(x-filter_size//2))
        
        pad_size = filter_size // 2
        self.padding_image = np.pad(image, pad_size, mode='constant', constant_values=0)
        self.filtered_image = np.zeros_like(image,dtype=np.uint8)

        for y in range(pad_size, self.padding_image.shape[0] - pad_size):
            for x in range(pad_size, self.padding_image.shape[1] - pad_size):
                neighborhood = self.padding_image[y - pad_size:y + pad_size + 1, x - pad_size:x + pad_size + 1]
                value = np.sum(neighborhood * mask,axis=None)
                self.filtered_image[y - pad_size, x - pad_size] = value
        cv2.imwrite(f"results/img{num}Q3_{filter_size}.jpg", self.filtered_image)

    def Q1(self,image,num):
        self.MeanFilter(image,num,3)
        self.MeanFilter(image,num,7)

    def Q2(self,image,num):
        self.MedianFilter(image,num,3)
        self.MedianFilter(image,num,7)

    def Q3(self,image,num):
        self.GaussianFilter(image,num)

if __name__ == '__main__':
    image = np.array([
        [0, 2, 1, 0, 0],
        [7, 3, 4, 1, 6],
        [0, 6, 5, 4, 5],
        [0, 0, 0, 0, 0],
        [1, 1, 0, 1, 0]
    ], dtype=np.float32) 
    hw5 = HW5()
    for num in range(3):
        image = cv2.imread(f"images/img{num+1}.jpg", cv2.IMREAD_GRAYSCALE)
        hw5.Q1(image,num+1)
        hw5.Q2(image,num+1)
        hw5.Q3(image,num+1)
    

    
