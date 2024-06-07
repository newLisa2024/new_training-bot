import logging
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Настройка логирования
logging.basicConfig(level=logging.ERROR, filename='bot_errors.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def draw_progress_bar(user_id, current, total, topic):
    if user_id is None:
        raise ValueError("user_id cannot be None")

    progress = current / total
    #fig, ax = plt.subplots(figsize=(8, 2))  # Уменьшить ширину фигуры

    fig, ax = plt.subplots(figsize=(2.5, 1))

    # Устанавливаем цвет фона для всей фигуры
    fig.patch.set_facecolor('#d0f0c0')#ABEBC6 #F0FFBF'

    # Устанавливаем цвет фона осей
    ax.set_facecolor('#000000')

    # Размеры и координаты
    bar_height = 0.2  # Установить высоту бара
    bar_width = 1.0
    progress_width = progress * bar_width

    # Отступ слева
    left_margin = 0.02

    # Фон прогресс-бара
    # Фон прогресс-бара с фиолетовой рамкой
    background_bar = patches.Rectangle((left_margin, 0.5 - bar_height / 2),
                                       bar_width, bar_height,
                                       linewidth=1, edgecolor='#6C3483', facecolor='#D3D3D3')
    ax.add_patch(background_bar)

    # Прогресс
    if progress > 0:
        progress_bar = patches.Rectangle((left_margin, 0.5 - bar_height / 2),
                                         progress_width, bar_height,
                                         linewidth=0, edgecolor='none', facecolor='#6C3483', alpha=0.7)
        ax.add_patch(progress_bar)

    # Текст внутри шкалы прогресса (пройденные вопросы)
    if progress_width < 0.08:  # Если прогресс слишком мал для текста внутри бара
        ax.text(left_margin + progress_width + 0.01, 0.5, f'{current}', horizontalalignment='left', verticalalignment='center',
                fontsize=8, color='black')
    else:
        ax.text(left_margin + progress_width - 0.02, 0.5, f'{current}', horizontalalignment='right', verticalalignment='center',
                fontsize=8, color='black')

    # Текст справа от шкалы (всего вопросов)
    ax.text(left_margin + bar_width + 0.01, 0.5, f'{total}', horizontalalignment='left', verticalalignment='center', fontsize=8,
            color='black')

    # Настройки осей
    ax.set_xlim(0, left_margin + bar_width + 0.2)  # Увеличиваем ограничение по x для большего пространства для текста
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Создание папки, если она не существует
    output_dir = 'user_graphs'
    os.makedirs(output_dir, exist_ok=True)

    # Сохранение в файл с прозрачным фоном
    filename = os.path.join(output_dir, f'transparent_progress_bar_{user_id}.png')

    # Проверка, что filename не None
    if filename is None or filename == '':
        raise ValueError("Filename cannot be None or empty")

    plt.savefig(filename, bbox_inches='tight', pad_inches=0, facecolor=fig.get_facecolor(), dpi=300)

    # Закрыть фигуру
    plt.close()

    return filename