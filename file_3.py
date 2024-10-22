import cv2
import math
import numpy as np

"""             !!!Краткое описание лабы!!!

На вход приходит два изображения и мы их сравниваем 
MSE - среднеквадратичное отклонение
PSNR - пиковое отношение сигнала к шуму
ssim - измерение качества на основе исходного изображения

Все формулы есть в лекции

"""



image1 = cv2.imread(r"D:\car.jpg")
image2 = cv2.imread(r"D:\car-min (3).jpg")

def mse(img1, img2):
    abs_diff = cv2.absdiff(img1, img2)
    return (abs_diff ** 2).sum() / (image1.shape[0] * image1.shape[1] *image1.shape[2])

def psnr(img1, img2):
    mse_im = mse(img1, img2)
    if (mse_im == 0):
        return 100
    return 20 * math.log10(255.0 / math.sqrt(mse_im))

def ssim(img1, img2):
    C1 = 6.5025
    C2 = 58.5225
    img1 = np.float32(img1)
    img2 = np.float32(img2)
    mu_K = cv2.GaussianBlur(img1, (11, 11), 1.5)
    mu_I = cv2.GaussianBlur(img2, (11, 11), 1.5)

    o_KI = cv2.GaussianBlur(img1 * img2, (11, 11), 1.5) - mu_K * mu_I
    o_K_2 = cv2.GaussianBlur(img1 ** 2, (11, 11), 1.5) - mu_K ** 2
    o_I_2 = cv2.GaussianBlur(img2 ** 2, (11, 11), 1.5) - mu_I ** 2

    SSIM = ((2 * mu_K * mu_I + C1) * (2 * o_KI + C2)) / ((mu_K ** 2 +mu_I ** 2 + C1) * (o_K_2+ o_I_2 + C2))
    return SSIM.mean()

print("MSE = {}".format(mse(image1, image2)))
print("PSNR = {}".format(psnr(image1, image2)))
print("SSIM = {}".format(ssim(image1, image2)))