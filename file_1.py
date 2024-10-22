import cv2
import numpy as np
import random


"""             !!!Краткое описание лабы!!!

На вход приходит изображение, открывается два окна (Одно сортирует по яркости, второе рандомно перемешивает строки),
на каждом окне есть трекбар, с помощью которого регулируется количество строк, на которые нужно нарезать картинку

Случайное перемешивание:
Получаем размеры картинки, создаем список, где будем хранить нарезанные строки
Нарезаем строки по размеру(изображение тоже являетя списком)
Перемешиваем в слуайном порядке массив с нарезками с помощью random shuffle
Создаем матрицу, заполненную нулями (она нужна для создания нового изображения из нарезки)
Затем заполняем матрицу строками, пока не соберем изображение такого же рамзера, что и исходное
Ну и выводим его)

Сортировка по яркости:
Получаем размеры картинки, создаем список, где будем хранить нарезанные строки
Нарезаем строки по размеру(изображение тоже являетя списком)
Переводим картинку из BGR в YUV (Y-яркость, U,V - цвета)
С помощью mean ищем среднее значение яркости(Y)
Заполняем список со значениями яркости (нужен, чтобы потом расставлять по яркости)
Создаем словарь для хранения Яркость: строка
Сортируем список яркости
Создаем матрицу, заполненную нулями (она нужна для создания нового изображения из нарезки)
Затем заполняем матрицу строками по ярксоит, пока не соберем изображение такого же рамзера, что и исходное
Ну и выводим его)

"""



im = cv2.imread(r'C:\\Program Files (x86)\\Common Files\\da wae.jpg') 
winNameBright = 'Bright'
cv2.namedWindow(winNameBright)
winNameRandom = 'Random'
cv2.namedWindow(winNameRandom)



def random_sort(size):
    size = size + 1
    width = im.shape[1]
    height = im.shape[0]
    image_list = []
    y = 0
    while(y < height):
        image_list.append(im[y:y+size])
        y += size
    random.shuffle(image_list)
    vv = np.zeros((height, width, 3), np.uint8)
    y = 0
    for i in image_list:
        img= i
        y_old = y
        y += img.shape[0]
        vv[y_old:y, :width, :3] = img
    cv2.imshow(winNameRandom, vv)

def brightness_sort(size):
    size = size + 1
    width = im.shape[1]
    height = im.shape[0]
    image_list = []
    y = 0
    while(y < height):
        image_list.append(im[y:y+size])
        y += size
    list_y = []
    for i in image_list:
        img_yuv = cv2.cvtColor(i, cv2.COLOR_BGR2YUV)
        y_averge = cv2.mean(img_yuv)
        list_y.append(y_averge[0])
    dict_img = dict(zip(list_y, image_list))
    list_y.sort()
    vv = np.zeros((height, width, 3), np.uint8)
    y = 0
    for i in list_y:
        img= dict_img[i]
        y_old = y
        y += img.shape[0]
        vv[y_old:y, :width, :3] = img
    cv2.imshow(winNameBright, vv)

cv2.createTrackbar("szie", winNameBright, 1, im.shape[0] - 1,brightness_sort)

cv2.createTrackbar("size", winNameRandom, 1, im.shape[0] - 1,random_sort)

cv2.waitKey(0)