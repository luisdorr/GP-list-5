import numpy as np
import cv2 as cv

img = cv.imread('baboon.png')  # original
img5 = cv.imread('bolinhas.png')  # original
corModificadora = [255, 0, 0]
k = 150


class Filtros:
    def grayscale_media_aritmetica(self, img):
        img2 = img.copy()
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                media = img.item(i, j, 0) * 0.333 + img.item(i, j, 1) * 0.333 + img.item(i, j, 2) * 0.3333
                img2.itemset((i, j, 0), media)
                img2.itemset((i, j, 1), media)
                img2.itemset((i, j, 2), media)
        return img2

    def grayscale_apenas_um_canal(self, img):
        img10 = img.copy()
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                B = img10.item(i, j, 0)
                img10.itemset((i, j, 0), B)
                img10.itemset((i, j, 1), B)
                img10.itemset((i, j, 2), B)
        return img10

    def color_ramp(self, img):
        img7 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img9 = img.copy()
        for i in range(img7.shape[0]):
            for j in range(img7.shape[1]):
                # "color ramp"
                if img7.item(i, j) < 100:
                    img9.itemset((i, j, 0), 255)
                    img9.itemset((i, j, 1), 255)
                    img9.itemset((i, j, 2), 0)
                elif img7.item(i, j) < 150:
                    img9.itemset((i, j, 0), 255)
                    img9.itemset((i, j, 1), 0)
                    img9.itemset((i, j, 2), 255)
                else:
                    img9.itemset((i, j, 0), 0)
                    img9.itemset((i, j, 1), 255)
                    img9.itemset((i, j, 2), 255)
        return img9

    # Exercise list 5:
    def renderizar_canal_vermelho(self, img):
        img_r = img.copy()
        for line in range(img.shape[0]):
            for column in range(img.shape[1]):
                img_r.itemset((line, column, 0), 0)
                img_r.itemset((line, column, 1), 0)
        return img_r

    def renderizar_canal_verde(self, img):
        img_g = img.copy()
        for line in range(img.shape[0]):
            for column in range(img.shape[1]):
                img_g.itemset((line, column, 0), 0)
                img_g.itemset((line, column, 2), 0)
        return img_g

    def renderizar_canal_azul(self, img):
        img_b = img.copy()
        for line in range(img.shape[0]):
            for column in range(img.shape[1]):
                img_b.itemset((line, column, 1), 0)
                img_b.itemset((line, column, 2), 0)
        return img_b

    def grayscale_media_ponderada(self, img):
        img_grayscale = img.copy()
        for line in range(img.shape[0]):
            for column in range(img.shape[1]):
                media_pond = img.item(line, column, 0) * 0.299 + img.item(line, column, 1) * 0.587 + img.item(line,
                                                                                                              column,
                                                                                                              2) * 0.114
                img_grayscale.itemset((line, column, 0), media_pond)
                img_grayscale.itemset((line, column, 1), media_pond)
                img_grayscale.itemset((line, column, 2), media_pond)
        return img_grayscale

    # corUniforme = Uma lista com [R, G, B]
    def colorizar(self, img, corUniforme):
        img_colorized = img.copy()
        for line in range(img.shape[0]):
            for column in range(img.shape[1]):
                B = img.item(line, column, 0) | corUniforme[0]
                G = img.item(line, column, 1) | corUniforme[1]
                R = img.item(line, column, 2) | corUniforme[2]
                img_colorized.itemset((line, column, 0), B)
                img_colorized.itemset((line, column, 1), G)
                img_colorized.itemset((line, column, 2), R)
        return img_colorized

    def inverter(self, img):
        img_inverted = img.copy()
        for line in range(img.shape[0]):
            for column in range(img.shape[1]):
                img_inverted.itemset((line, column, 0), 255 - img.item(line, column, 0))
                img_inverted.itemset((line, column, 1), 255 - img.item(line, column, 1))
                img_inverted.itemset((line, column, 2), 255 - img.item(line, column, 2))
        return img_inverted

    # limiar = 0 e 255
    def binarizar(self, img, limiar):
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img_binarised = img_gray.copy()
        for line in range(img_gray.shape[0]):
            for column in range(img_gray.shape[1]):
                if img_gray.item(line, column) < limiar:
                    img_binarised.itemset((line, column), 0)
                else:
                    img_binarised.itemset((line, column), 255)
        return img_binarised


    def mixed_filter(self, img, raio):
        img_gray = self.grayscale_media_ponderada(img)  # aplica o filtro de grayscale
        img_mixed = self.vignette(img_gray, raio)  # aplica o filtro de vignette
        return img_mixed  # retorna a imagem mista

    def vignette(self, img, raio):
        img_vignette = img.copy()
        h, w = img.shape[:2]  # altura e largura da imagem
        cx, cy = w // 2, h // 2  # centro da imagem
        for line in range(h):
            for column in range(w):
                d = ((line - cy) ** 2 + (column - cx) ** 2) ** 0.5  # distância do pixel ao centro
                f = max(0, 1 - d / raio)  # fator de escurecimento
                img_vignette[line, column] = img_vignette[line, column] * f  # multiplica o pixel pelo fator
        return img_vignette


# Criando um objeto da classe Filtros
filtros = Filtros()

# Aplicando os métodos na imagem original
# img2 = filtros.grayscale_media_aritmetica(img)
# img3 = filtros.grayscale_media_ponderada(img)
# img10 = filtros.grayscale_apenas_um_canal(img)
# img4 = filtros.colorizar(img, corModificadora)
# img6 = filtros.inverter(img5)
# img8 = filtros.binarizar(img, k)
# img9 = filtros.color_ramp(img)

# Exibindo as imagens
# cv.imshow("Original", img)
# cv.imshow("Grayscale - Média Aritmética", img2)
# cv.imshow("Grayscale - Média Ponderada", img3)
# cv.imshow("Grayscale - Apenas um canal", img10)
# cv.imshow("Imagem colorizada", img4)
# cv.imshow("Imagem invertida", img6)
# cv.imshow("Imagem Binarizada", img8)
# cv.imshow("Imagem Color Ramp", img9)

img_r = filtros.renderizar_canal_vermelho(img)
img_g = filtros.renderizar_canal_verde(img)
img_b = filtros.renderizar_canal_azul(img)
img_grayscale = filtros.grayscale_media_ponderada(img)

corUniforme = [50, 100, 200]
img_colorized = filtros.colorizar(img, corUniforme)
img_inverted = filtros.inverter(img)
img_binarised = filtros.binarizar(img, 100)
img_mixed = filtros.mixed_filter(img, 225)
img_vignette = filtros.vignette(img, 274)

cv.imshow("Canal vermelho", img_r)
cv.imshow("Canal verde", img_g)
cv.imshow("Canal azul", img_b)
cv.imshow("Grayscale", img_grayscale)
cv.imshow("Colorized", img_colorized)
cv.imshow("Inverted", img_inverted)
cv.imshow("Binarised", img_binarised)
cv.imshow("Mixed", img_mixed)
cv.imshow("Vignette", img_vignette)

cv.waitKey(0)
cv.destroyAllWindows()
