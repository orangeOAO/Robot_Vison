import cv2
import numpy as np
import math

class Skeleton:
    def __init__(self) -> None:
        self.edge_coordinates = []
        
    def set_images(self,img_path):
        self.img = cv2.imread(img_path)
        self.height, self.width = self.img.shape[:2]
    def binary_image(self):
        gray_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        _, binary_img = cv2.threshold(gray_img, 230, 255, cv2.THRESH_BINARY)
        self.inverse_img = 255 - binary_img
        self.edges = np.zeros_like(binary_img)

    def get_distance(self, originX, originY, targetX, targetY):
        return math.sqrt((originX - targetX) ** 2 + (originY - targetY) ** 2)

    def edge_detect(self):
        for x in range(1, self.height - 1):
            for y in range(1, self.width - 1):
                if np.abs(int(self.inverse_img[x, y]) - int(self.inverse_img[x+1, y])) > 0 or np.abs(int(self.inverse_img[x, y]) - int(self.inverse_img[x, y+1])) > 0:
                    self.edges[x, y] = 255
                    self.edge_coordinates.append([x, y])

    def distance_map(self):
        distance_img = np.zeros_like(self.inverse_img, dtype=float)
        for x in range(1, self.height - 1):
            for y in range(1, self.width - 1):
                if self.inverse_img[x, y] != 0:
                    distances = [self.get_distance(x, y, cx, cy) for cx, cy in self.edge_coordinates]
                    distance_img[x, y] = min(distances) if distances else 0
        self.distance_img_normalized = cv2.normalize(distance_img, None, 0, 255, cv2.NORM_MINMAX)
        self.dist_img_8bit = np.uint8(self.distance_img_normalized)

    def image_process(self,count):
        self.edge_coordinates=[]
        self.binary_image()
        self.edge_detect()
        self.distance_map()
        cv2.imshow("image",self.dist_img_8bit)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite(f"img{count}_q1-1.jpg",self.dist_img_8bit)
        

# Usage
skeleton = Skeleton()
for count in range(1,2):
    skeleton.set_images(f"images/img{count}.jpg")
    skeleton.image_process(count)

