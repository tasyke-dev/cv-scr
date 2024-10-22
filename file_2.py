import cv2
import numpy as np

"""                  !!!Краткое описание лабы!!!

На вход приходит изображение, открывается окно
На экране два трекбара, один отвечает за размер кисти, второй за ее "мягкость"

Размываем изображение А

Изображение Б переводим в градации серого,
Создаем копию Б и добавляем туда третий канал

Создаем маску, которая будет накладыватся на исходное изображение
При движении мыши по изображению, ловим значения мягкости и радиуса
Накладываем изображение сверху
convertScaleAbs нужен чтобы конвертировать эти даннные в 8 бит (хз зачем)))
"""




im = cv2.imread(r'C:\Users\artyo\Desktop\ja.jpeg')

winName = 'Main Window'
cv2.namedWindow(winName)

image_a = cv2.GaussianBlur(im, ksize=(31,31), sigmaX=15, sigmaY=15)
image_b = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
image_b = cv2.cvtColor(image_b, cv2.COLOR_GRAY2BGR) # что бы было 3 канала

result_old = image_a.copy()

def nope(r):
    pass

def update_image(event, x, y, flags, param):

    if event==cv2.EVENT_MOUSEMOVE:
        radius = cv2.getTrackbarPos("R", winName)
        blur = cv2.getTrackbarPos("BLUR", winName)

    if blur % 2 == 0:
        blur += 1

    global result_old

    mask1 = np.zeros(shape=result_old.shape[:2], dtype=np.uint8)
    cv2.circle(mask1, (x, y), radius, (255), -1)

    mask1 = cv2.GaussianBlur(mask1, (blur, blur), 11)

    alpha = cv2.cvtColor(mask1, cv2.COLOR_GRAY2BGR)/255
    result_old = cv2.convertScaleAbs(result_old*(1-alpha) + image_b*alpha)
    cv2.imshow(winName, result_old)


cv2.setMouseCallback(winName, update_image)
cv2.createTrackbar("R", winName, 20, 500, nope)
cv2.createTrackbar("BLUR", winName, 10, 100, nope)
cv2.imshow(winName, image_a)
cv2.waitKey(0)
