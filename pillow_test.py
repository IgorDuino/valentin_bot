from PIL import Image, ImageDraw, ImageFont
im = Image.open('img/1.jpg')

font = ImageFont.truetype('font.ttf', size=18)
draw_text = ImageDraw.Draw(im)
draw_text.text(
    (100, 100),
    'Текст 18px',
    # Добавляем шрифт к изображению
    font=font,
    fill='#1C0606')
im.show()
