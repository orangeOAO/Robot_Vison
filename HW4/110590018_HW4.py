import cv2
import numpy as np
import random
from heapq import heappop, heappush

# 提供图像文件的正确路径
image_name = "img3"
image_path = f'images/{image_name}.jpg'

# 加载图像并转换为灰度图像
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 创建用于存储标记的二维数组
markers = np.zeros_like(gray, dtype=np.int32)

# 定义用于绘制的函数
def draw(event, x, y, flags, param):
    global drawing, label
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        cv2.circle(image, (x, y), 5, colors[label], -1)
        cv2.circle(markers, (x, y), 5, label, -1)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.circle(image, (x, y), 5, colors[label], -1)
            cv2.circle(markers, (x, y), 5, label, -1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(image, (x, y), 5, colors[label], -1)
        cv2.circle(markers, (x, y), 5, label, -1)

# 初始化变量
drawing = False
label = 1  # 从标签 1 开始
colors = [tuple((random.randint(0, 255) for _ in range(3))) for _ in range(15)]

# 设置绘图窗口
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw)

while True:
    cv2.imshow('image', image)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):  # 按 'q' 键退出
        break
    elif key == ord('n'):  # 按 'n' 键使用下一个标签
        label = (label + 1) % len(colors)


# cv2.imwrite(f'{image_name}_Q1_1.jpg', image)
cv2.destroyAllWindows()

grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
gradient = cv2.magnitude(grad_x, grad_y)

priority_queue = []
for y in range(markers.shape[0]):
    for x in range(markers.shape[1]):
        if markers[y, x] > 0:  # 如果是标记像素
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]: 
                ny, nx = y + dy, x + dx
                if 0 <= ny < markers.shape[0] and 0 <= nx < markers.shape[1] and markers[ny, nx] == 0:
                    markers[ny, nx] = -2
                    heappush(priority_queue, (gradient[ny, nx], ny, nx))

while priority_queue:
    _, y, x = heappop(priority_queue)
    neighbor_labels = set()
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny, nx = y + dy, x + dx
        if 0 <= ny < markers.shape[0] and 0 <= nx < markers.shape[1]:
            if markers[ny, nx] > 0:
                neighbor_labels.add(markers[ny, nx])
    if len(neighbor_labels) == 1:
        markers[y, x] = neighbor_labels.pop()
    else:
        markers[y, x] = -1  # 标记为边缘
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny, nx = y + dy, x + dx
        if 0 <= ny < markers.shape[0] and 0 <= nx < markers.shape[1] and markers[ny, nx] == 0:
            markers[ny, nx] = -2
            heappush(priority_queue, (gradient[ny, nx], ny, nx))

visual_markers = np.zeros((markers.shape[0], markers.shape[1], 3), dtype=np.uint8)
for i in range(1, len(colors)):
    visual_markers[markers == i] = colors[i]
visual_markers[markers == -1] = [0, 0, 0]  # 用黑色标记边缘

# cv2.imwrite(f'{image_name}_Q1_2.jpg', visual_markers)

cv2.imshow('Final Marked Image', visual_markers)
cv2.waitKey(0)
cv2.destroyAllWindows()
