# -*- coding: utf-8 -*-
"""dct_expansion.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XBU5c1rtxpEINW9DlwEhp7u8-oE7sceC
"""

import cv2
import numpy as np
import time

import csv
import pprint

def create_custom_left_matrix(m, scale_factor):
    # 2m x m 行列を作成し、すべての要素を0で初期化
    custom_matrix = np.zeros((int(scale_factor * m), m))

    # m x m の単位行列を挿入
    custom_matrix[:m, :m] = (1.5 + 0.3*(scale_factor-2))*np.eye(m)

    #print(custom_matrix)

    #print(custom_matrix.shape)

    return np.float32(custom_matrix)  # データ型を変換

def create_custom_right_matrix(n, scale_factor):
    # m x 2m 行列を作成し、すべての要素を0で初期化
    custom_matrix = np.zeros((n, int(scale_factor * n)))

    # m x m の単位行列を挿入
    custom_matrix[:n, :n] = (1.5 + 0.3*(scale_factor-2))*np.eye(n)

    #print(custom_matrix)

    #print(custom_matrix.shape)

    return np.float32(custom_matrix)  # データ型を変換

def dct_expansion(dct_image, scale_factor):
    left_matrix = create_custom_left_matrix(dct_image.shape[0], scale_factor)
    right_matrix = create_custom_right_matrix(dct_image.shape[1], scale_factor)

    # 拡大後の画像を初期化
    #result_image = np.zeros((dct_image.shape[0] * scale_factor, dct_image.shape[1] * scale_factor, 3), dtype=np.float32)

    # 行列の掛け算
    result_image = np.dot(np.dot(left_matrix, dct_image), right_matrix)

    return result_image

# 画像読み込み
image_path = 'kit.jpg'
original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
print(original_image.shape)
print(original_image[0,0])
cv2.imwrite('kit_gray.jpg', original_image)


# DCT変換
dct_image1 = cv2.dct(np.float32(original_image))
dct_image2 = dct_image1

# 拡大倍率
scale_factor = 2.0

#提案手法
start = time.time()
result_image1_dct = dct_expansion(dct_image1, scale_factor)
end = time.time()
print("Proposed method")
print(end - start)
result_image1_idct = cv2.idct(result_image1_dct)
#デバッグ
print(result_image1_idct.shape)
print(result_image1_idct[0,0])

#従来手法
start = time.time()
result_image2_idct = cv2.idct(dct_image2)
enlarged_image = cv2.resize(result_image2_idct, None, fx=scale_factor, fy=scale_factor)
result_image2_dct = cv2.dct(np.float32(enlarged_image))
end = time.time()
print("Conventional method")
print(end - start)

# 結果を出力
cv2.imwrite('ResultImage.jpg', result_image1_idct)
