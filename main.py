import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

max_img_size = 300  # Максимальный размер изображения
red_color = (255, 0, 0)  # Цвет для рисования границ
img_name = input("input imgage name: ")


# Функция для изменения размера изображения до заданного максимального размера
def resize_to_const(img):
    m = max(img.size)
    if m <= max_img_size:
        return img
    comp_ratio = int(m / max_img_size) + 1
    new_size = (img.size[0] // comp_ratio, img.size[1] // comp_ratio)
    return img.resize(new_size)


# Функция для вычисления сумм пикселей
def calc_sums(img, xmin, xmax, H):
    res = np.zeros([H, H])
    if xmax - xmin == 1:
        for x in range(H):
            res[:, x] = 1 - img[:, xmin] / 255
    else:
        mid = (xmin + xmax) // 2
        ans1 = calc_sums(img, xmin, mid, H)
        ans2 = calc_sums(img, mid, xmax, H)
        for x in range(H):
            for y in range(H):
                res[x, y] = ans1[x, (x + y) // 2] + ans2[(x + y) // 2, y]
    return res


# Открываем изображение и приводим его к черно-белому
color_image = Image.open(img_name)
color_image = resize_to_const(color_image)
gray_image = color_image.convert('L')

# Применяем фильтр для поиска границ
edges = gray_image.filter(ImageFilter.FIND_EDGES())
wb_image = ImageOps.invert(edges)

# Устанавливаем ширину и высоту изображения
W, H = wb_image.size

# Рисуем белую рамку вокруг изображения
for x in range(W):
    wb_image.putpixel((x, 0), 255)  # Верхняя граница
    wb_image.putpixel((x, H - 1), 255)  # Нижняя граница
for y in range(H):
    wb_image.putpixel((0, y), 255)  # Левая граница
    wb_image.putpixel((W - 1, y), 255)  # Правая граница

# Преобразуем изображение в массив NumPy
wb_array = np.array(wb_image)

# Поворачиваем изображение и рисуем прямые на повернутых изображениях
for theta in (0, 15, 30, 45, 60, 75, 90):
    # Поворачиваем цветное изображение
    transparent_image = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    rot_tr_img = transparent_image.rotate(theta, fillcolor=(0, 0, 0, 0))
    draw = ImageDraw.Draw(rot_tr_img)

    # Поворачиваем черно-белое изображение
    rotated_image = wb_image.rotate(theta, fillcolor="white")
    rotated_array = np.array(rotated_image)

    # Вычисляем суммы
    result = calc_sums(rotated_array, 0, W, H)

    # Рисуем красные прямые на повернутом изображении в местах с максимальными суммами
    for i in range(2, H - 2):
        for j in range(2, H - 2):
            if result[i][j] >= max(np.max(result[i - 2:i + 2, :]), np.max(result[:, j - 2:j + 2]), 100):
                draw.line([(0, i), (W - 1, j)], fill="red", width=2)

    transparent_image = rot_tr_img.rotate(-theta, fillcolor=(0, 0, 0, 0))
    color_image.paste(transparent_image, (0, 0), transparent_image)

color_image.show()


