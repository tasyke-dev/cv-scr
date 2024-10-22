import numpy as np
import cv2

"""             !!!Краткое описание лабы!!!

На входе у нас картинка с цветом, что мы ищем и видео с вебки
по нажатию кнопки, мы останавливаем видео и получаем изображение сцены

Выделяем прямоугольник на сцене

переводим сцену в HSV (Hue, Saturation, Value — тон, насыщенность, значение) и исходное изображение
рассчитываем гистограмму, затем применяем обратную проекцию (применяем к исходному изображению гистограмму)

Обратная проекция гистограммы используется для сегментации изображения или для поиска интересующих объектов на изображении. 
Проще говоря, она создает изображение с тем же размером (один канал),
что и входное изображение, где каждый пиксель соответствует пикселю нашего объекта.

getStructuringElement - создаем эллипсы, для заполенения пространства между полученными контурами на сцене
treshhold  - пиксели, темнее 50 переводим в черный, остальные в белый
bitwise_and - ищем побитовое совпадение пикселей
Подгоняем гистограмму по размеру, накладываем на картинки

Код после def create_mouse_input(): - обработка нажатий на клавиши клавиатуры
"""

def scary():
    roi = cv2.imread("544.png")
    hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
    target = cv2.imread('sceneImg.jpg')
    hsvt = cv2.cvtColor(target,cv2.COLOR_BGR2HSV)
    #расчет гистограммы
    # calculating object histogram
    roihist = cv2.calcHist([hsv],[0, 1], None, [180, 256], [0, 180, 0, 256] )
    #нормализация гистограммы и применение обратной проекции
    # normalize histogram and apply backprojection
    cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)
    dst = cv2.calcBackProject([hsvt],[0,1],roihist,[0,180,0,256],1)
    # Now convolute with circular disc
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    cv2.filter2D(dst,-1,disc,dst)
    # threshold and binary AND
    ret,thresh = cv2.threshold(dst,50,255,0)
    thresh = cv2.merge((thresh,thresh,thresh))
    res = cv2.bitwise_and(target,thresh)
    h,w = res.shape[:2]
    new_roi = cv2.resize(roi, (w, h))
    first_res = np.hstack((target,new_roi))
    second_res = np.hstack((thresh,res))
    res = np.vstack((first_res, second_res))
    cv2.imwrite('res.jpg',res)
    cv2.imshow('res',res)




rect = (0,0,1,1)
rectangle = False
rect_over = False



def onmouse(event,x,y,flags,params):
    global sceneImg, rectangle, rect, ix, iy, drect_over, roi

    # Draw Rectangle
    if event == cv2.EVENT_LBUTTONDOWN:
        rectangle = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if rectangle == True:
#            cv2.rectangle(sceneCopy,(ix,iy),(x,y),(0,255,0),1)
            rect = (min(ix,x),min(iy,y),abs(ix-x),abs(iy-y))

    elif event == cv2.EVENT_LBUTTONUP:
        rectangle = False
        rect_over = True

        sceneCopy = sceneImg.copy()
        cv2.rectangle(sceneCopy,(ix,iy),(x,y),(0,255,0),1)

        rect = (min(ix,x),min(iy,y),abs(ix-x),abs(iy-y))       
        roi = sceneImg[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]

        cv2.imshow('mouse input', sceneCopy)
        cv2.imwrite('roi.jpg', roi)


def create_mouse_input():
    # Named window and mouse callback
    cv2.namedWindow('mouse input')
    cv2.setMouseCallback('mouse input',onmouse)

cv2.namedWindow('video')

camObj = cv2.VideoCapture(0)
keyPressed = None
running = True
scene = False
# Start video stream
while running:
    readOK, frame = camObj.read()

    keyPressed = cv2.waitKey(5)
    if keyPressed == ord('s'):
        scene = True
        cv2.destroyWindow('video')

        create_mouse_input()

        cv2.imwrite('sceneImg.jpg',frame)
        sceneImg = cv2.imread('sceneImg.jpg')

        cv2.imshow('mouse input', sceneImg)

    elif keyPressed == ord('r') and scene:
        scene = False
        cv2.destroyWindow('mouse input')

    elif keyPressed == ord('q'):
        running = False

    elif keyPressed == ord('g'):
        scary()

    if not scene:
        cv2.imshow('video', frame)

cv2.destroyAllWindows()
camObj.release()