from PIL import Image


# функция для чтения координат
def read_coordinates():
    coords = []
    f = open('keys1.txt', 'r')
    for line in f:
        line = line.strip()
        if line != '':
            # убираем скобки
            line = line.replace('(', '')
            line = line.replace(')', '')
            # разделяем по запятой
            parts = line.split(', ')
            x = int(parts[0])
            y = int(parts[1])
            coords.append((x, y))
    f.close()
    print('Координат прочитано:', len(coords))
    return coords


# декодирование из картинки
def decode_message():
    print('=== ДЕКОДИРОВАНИЕ ===')

    # открываем картинку
    img = Image.open('new1.png')
    print('Размер картинки:', img.size)

    # читаем координаты
    coordinates = read_coordinates()

    message = ''

    # проходим по всем координатам
    for i in range(len(coordinates)):
        x = coordinates[i][0]
        y = coordinates[i][1]

        # получаем цвет пикселя
        pixel = img.getpixel((x, y))

        # берем синий канал
        blue = pixel[2]

        # переводим в символ
        symbol = chr(blue)
        message = message + symbol

        # выводим первые 3 для проверки
        if i < 3:
            print(f'Пиксель ({x}, {y}) - цвет: {pixel}, синий: {blue}, символ: "{symbol}"')

    print('Декодированное сообщение:', message)
    print('Длина сообщения:', len(message))
    return message


# кодирование в картинку
def encode_message():
    print('=== КОДИРОВАНИЕ ===')

    # сообщение для кодирования
    text = 'Beautiful'
    print('Кодируем:', text)

    # открываем картинку
    img = Image.open('new1.png')
    new_img = img.copy()

    # читаем координаты
    coordinates = read_coordinates()

    # переводим текст в биты
    bits = []
    for char in text:
        # получаем ASCII код
        ascii_code = ord(char)

        # переводим в биты (8 бит на символ)
        char_bits = []
        for bit_pos in range(8):
            bit = (ascii_code >> bit_pos) & 1
            char_bits.append(bit)

        # показываем биты первого символа
        if char == text[0]:
            bit_string = ''
            for b in char_bits:
                bit_string = bit_string + str(b)
            print(f'Биты символа "{char}" (ASCII {ascii_code}): {bit_string}')

        # добавляем биты в общий список
        for bit in char_bits:
            bits.append(bit)

    print('Всего битов:', len(bits))

    # кодируем биты в пиксели
    for i in range(len(bits)):
        x = coordinates[i][0]
        y = coordinates[i][1]
        bit = bits[i]

        # получаем старый цвет
        old_pixel = new_img.getpixel((x, y))
        old_red = old_pixel[0]
        old_green = old_pixel[1]
        old_blue = old_pixel[2]

        # меняем младший бит красного канала
        if bit == 1:
            new_red = old_red | 1  # ставим 1
        else:
            new_red = old_red & 254  # ставим 0

        # показываем изменения для первых пикселей
        if i < 3:
            print(f'Пиксель ({x}, {y}) - красный было: {old_red}, стало: {new_red}, бит: {bit}')

        # сохраняем новый цвет
        if len(old_pixel) == 4:  # RGBA
            new_pixel = (new_red, old_green, old_blue, old_pixel[3])
        else:  # RGB
            new_pixel = (new_red, old_green, old_blue)

        new_img.putpixel((x, y), new_pixel)

    # сохраняем
    new_img.save('encoded_image.png')
    print('Сохранено в encoded_image.png')


# проверка кодирования
def check_decode():
    print('=== ПРОВЕРКА ===')

    # открываем закодированную картинку
    img = Image.open('encoded_image.png')

    # читаем координаты
    coordinates = read_coordinates()

    # извлекаем биты
    bits = []
    # для Beautiful нужно 72 бита (9 символов * 8 бит)
    for i in range(72):
        x = coordinates[i][0]
        y = coordinates[i][1]

        pixel = img.getpixel((x, y))
        red = pixel[0]
        bit = red & 1  # младший бит
        bits.append(bit)

        # показываем первые пиксели
        if i < 3:
            print(f'Пиксель ({x}, {y}) - красный: {red}, бит: {bit}')

    # собираем биты обратно в текст
    result = ''

    # берем по 8 битов
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i + 8]

        # показываем биты первого символа
        if i == 0:
            bit_str = ''
            for b in byte_bits:
                bit_str = bit_str + str(b)
            print('Биты первого символа:', bit_str)

        # переводим биты в число
        ascii_code = 0
        for j in range(8):
            if byte_bits[j] == 1:
                ascii_code = ascii_code + (2 ** j)

        # переводим в символ
        char = chr(ascii_code)
        result = result + char

    print('Результат проверки:', result)

    # проверяем
    if result == 'Beautiful':
        print('Проверка прошла успешно!')
    else:
        print('Ошибка при проверке')


# основная программа
print('Лабораторная работа №3 - Стеганография')
print('Вариант 1')
print()

# выполняем задания
decode_message()
print()
encode_message()
print()
check_decode()

print()
print('Работа завершена')