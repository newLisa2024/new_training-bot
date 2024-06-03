from PIL import Image, ImageDraw, ImageFont
import os

def create_frame(minutes, seconds, width=150, height=50):

    # Создаем изображение с фоном цвета #90EE90
    img = Image.new('RGB', (width, height), color='#D3D3D3')#D3D3D3
    d = ImageDraw.Draw(img)

    # Настраиваем шрифт
    font_path = "arialbd.ttf"  # путь к шрифту Arial Bold
    font = ImageFont.truetype(font_path, 40)

    # Создаем текст для минут и секунд
    timer_text = f'{minutes:02}:{seconds:02}'

    # Вычисляем размеры текста
    text_bbox = d.textbbox((0, 0), timer_text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

    # Позиция текста (центрирование по ширине и высоте)
    text_position = ((width - text_width) / 2, (height - text_height) / 2 - text_bbox[1])

    # Добавляем текст на изображение с цветом #8A2BE2
    d.text(text_position, timer_text, fill='#6C3483', font=font)#8A2BE2

    return img

def generate_countdown_gif(duration, step=1, output_path='GIF_timer/countdown.gif'):
    frames = []

    # Создаем папку для сохранения кадров и итогового файла, если ее нет
    output_dir = 'GIF_timer'
    os.makedirs(output_dir, exist_ok=True)

    # Создаем кадры для каждого шага
    for i in range(duration, -1, -step):
        minutes = i // 60
        seconds = i % 60
        frame = create_frame(minutes, seconds)
        frames.append(frame)

    # Сохраняем кадры в GIF
    frame_one = frames[0]
    frame_one.save(output_path, save_all=True, append_images=frames[1:], duration=1000, loop=0)

# Генерируем GIF с обратным отсчетом на 2 минуты (120 секунд)
generate_countdown_gif(duration=120, step=1, output_path='GIF_timer/countdown.gif')
