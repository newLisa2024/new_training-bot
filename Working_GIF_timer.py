from PIL import Image, ImageDraw, ImageFont
from wand.image import Image as WandImage
import os

#УСТАНАВЛИВАЕМ СЕКУНДЫ НА ТАЙМЕР
timer_seconds = 120


def create_frame(minutes, seconds, width=150, height=50):
    # Создаем изображение
    img = Image.new('RGB', (width, height), color='lightgrey')
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

    # Добавляем текст на изображение
    d.text(text_position, timer_text, fill="indianred", font=font)

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

    # Сохраняем кадры во временные файлы
    temp_dir = os.path.join(output_dir, 'temp_frames')
    os.makedirs(temp_dir, exist_ok=True)
    frame_paths = []
    for idx, frame in enumerate(frames):
        frame_path = os.path.join(temp_dir, f'frame_{idx:04d}.png')
        frame.save(frame_path)
        frame_paths.append(frame_path)

    # Используем ImageMagick через wand для создания GIF
    with WandImage() as wand_img:
        for frame_path in frame_paths:
            with WandImage(filename=frame_path) as frame:
                wand_img.sequence.append(frame)

        for cursor in range(len(wand_img.sequence)):
            with wand_img.sequence[cursor] as frame:
                frame.delay = 1000  # задержка в миллисекундах для каждого кадра (1 секунда)

        wand_img.type = 'optimize'
        wand_img.save(filename=output_path)

    # Удаляем временные файлы
    for frame_path in frame_paths:
        os.remove(frame_path)
    os.rmdir(temp_dir)

# Генерируем GIF с обратным отсчетом на 2 минуты (120 секунд)
generate_countdown_gif(duration=timer_seconds, step=1, output_path='GIF_timer/countdown.gif')
