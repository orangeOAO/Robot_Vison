import cv2
import numpy as np

def zhang_suen_thinning(img):
    # Function to do one thinning iteration
    def thinning_iteration(im, iter):
        marker = np.zeros(im.shape, np.uint8)
        for i in range(1, im.shape[0] - 1):
            for j in range(1, im.shape[1] - 1):
                p2, p3, p4 = im[i-1, j], im[i-1, j+1], im[i, j+1]
                p5, p6, p7 = im[i+1, j+1], im[i+1, j], im[i+1, j-1]
                p8, p9, p1 = im[i, j-1], im[i-1, j-1], im[i, j]
                A  = (p2 == 0 and p3 == 1) + (p3 == 0 and p4 == 1) + \
                     (p4 == 0 and p5 == 1) + (p5 == 0 and p6 == 1) + \
                     (p6 == 0 and p7 == 1) + (p7 == 0 and p8 == 1) + \
                     (p8 == 0 and p9 == 1) + (p9 == 0 and p1 == 1)
                B  = sum([p2, p3, p4, p5, p6, p7, p8, p9])
                m1 = (p2 * p4 * p6) if iter == 0 else (p2 * p4 * p8)
                m2 = (p4 * p6 * p8) if iter == 0 else (p2 * p6 * p8)
                if A == 1 and B >= 2 and B <= 6 and m1 == 0 and m2 == 0:
                    marker[i, j] = 1
        return im & ~marker

    # Convert image to binary
    _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
    img = img // 255

    prev = np.zeros(img.shape, np.uint8)
    diff = None

    while True:
        img = thinning_iteration(img, 0)
        img = thinning_iteration(img, 1)
        diff = np.sum(np.abs(prev - img))
        if diff == 0:
            break
        prev = img.copy()

    return img * 255

# Usage
img = cv2.imread("images/img3.jpg", 0)
skeleton = zhang_suen_thinning(img)
cv2.imshow("Skeleton", skeleton)
cv2.waitKey(0)
cv2.destroyAllWindows()
