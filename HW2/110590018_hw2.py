import numpy as np
import cv2
import random

def generate_random_color():
    return [random.randint(0, 255) for _ in range(3)]

def label_connected4_components(img):
    labeled_img = np.zeros_like(img, dtype=np.int32)
    label = 1
    rows, cols = img.shape[:2]
    for x in range(rows):
        for y in range(cols):
            if img[x, y] != 0 and labeled_img[x, y] == 0:
                stack = [(x, y)]
                while stack:
                    cx, cy = stack.pop()
                    if 0 <= cx < rows and 0 <= cy < cols and img[cx, cy] != 0 and labeled_img[cx, cy] == 0:
                        labeled_img[cx, cy] = label
                        stack.extend([(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)])
                label += 1

    # 染色
    colored_labeled_img = np.zeros((rows, cols, 3), dtype=np.uint8)
    for lbl in range(1, label):
        color = generate_random_color()
        colored_labeled_img[labeled_img == lbl] = color

    return colored_labeled_img

def label_connected8_components(img):
    labeled_img = np.zeros_like(img, dtype=np.int32)
    label = 1
    rows, cols = img.shape[:2]
    for x in range(rows):
        for y in range(cols):
            if img[x, y] != 0 and labeled_img[x, y] == 0:
                stack = [(x, y)]
                while stack:
                    cx, cy = stack.pop()
                    if 0 <= cx < rows and 0 <= cy < cols and img[cx, cy] != 0 and labeled_img[cx, cy] == 0:
                        labeled_img[cx, cy] = label
                        stack.extend([(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1),(cx-1, cy-1), (cx+1, cy-1), (cx+1, cy+1), (cx-1, cy+1)])
                label += 1
    # 染色
    colored_labeled_img = np.zeros((rows, cols, 3), dtype=np.uint8)
    for lbl in range(1, label):
        color = generate_random_color()
        colored_labeled_img[labeled_img == lbl] = color

    return colored_labeled_img

if __name__ == "__main__":
    for i in range(1,5):
        img_path = f'images/img{i}.png'
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        _, binary_img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
        colored_labeled_img = label_connected4_components(binary_img)
        cv2.imwrite(f'img{i}_4.png',colored_labeled_img)
        colored_labeled_img = label_connected8_components(binary_img)
        cv2.imwrite(f'img{i}_8.png',colored_labeled_img)
    
