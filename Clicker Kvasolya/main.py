# Импорты
import pygame # Импортирование библиотеки для создания игр и работы с графикой
import random # Импортирование библиотеки для работы со случайными значениями

def respawn_target(): # Функция которая рандомно размещает изображение по экрану
    target_rect.x = random.randint(0, W - target_rect.w) # Разместить рандомно точку по горизонтали
    target_rect.y = random.randint(0, H - target_rect.h) # Разместить рандомно точку по вертикали

#Инициализации
pygame.init() # Инициализация Pygame
pygame.font.init() # Инициализация шрифтов

# Свойства окна
W = 450 # Ширина экрана
H = 800 # Высота экрана
SCREEN_SIZE = (W, H) # Картеж экрана(высоты и ширины)
SCREEN_CENTER = (W // 2, H // 2) # Центр экрана
SCREEN_TOP = (W // 2, 0)

screen = pygame.display.set_mode(SCREEN_SIZE) # Создание окна с заданными размерами

FPS = 60 # Ограничение по кадрам
clock = pygame.time.Clock() # Объект для отслеживания времени и контроля FPS

# Настройка шрифта
ARIAL_FONT_PATH = pygame.font.match_font('arial') # Получение пути к шрифту
ARIAL_64 = pygame.font.Font(ARIAL_FONT_PATH, 64) # Задания размера шрифта на 64
ARIAL_36 = pygame.font.Font(ARIAL_FONT_PATH, 36) # Задания размера шрифта на 36

# Время
INIT_DELAY = 2000 # Время задержки перед началом (в миллисекундах)
finish_delay = INIT_DELAY # Текущая задержка
DECREASE_BASE = 1.002 # Для уменьшения времени между кликами
last_respawn_time = 0 # Время последнего респауна

# Настройки для отображения сообщения о завершении игры
game_over = False # Закончилась ли игра
RETRY_SURFACE = ARIAL_36.render('PRESS ANY KEY', True, (0, 0, 0)) # Создания текста
RETRY_RECT = RETRY_SURFACE.get_rect() # Получение прямоугольной области для текстовой поверхности
RETRY_RECT.midtop = SCREEN_CENTER # Установка верхней средней точки прямоугольника в центр экрана

score = 0 #счёт

# Загрузка и настройка изображения
TARGET_IMAGE = pygame.image.load('Kvasolya.png') # Создание поверхности картинки
TARGET_IMAGE = pygame.transform.scale(TARGET_IMAGE, (100, 100)) # Изменение размера картинки
target_rect = TARGET_IMAGE.get_rect() # Получение прямоугольной области для изображения

respawn_target() # Вызов функции которая рандомно размещает изображение по экрану

# Игровой цикл
running = True # Работает ли цикл
while running: # Цикл
    for i in pygame.event.get(): # Для получения всех происходящих событий внутри
        if i.type == pygame.QUIT: # Если пользователь вышел
            running = False # Остановка цикла
        elif i.type == pygame.KEYDOWN: # Если нажали любую клавишу для рестарта
            if game_over: # Если игра окончена
                score = 0 # Обнулить счётчик
                finish_delay = INIT_DELAY # Сбросить задержку до начального значения
                game_over = False # Вернуть состояние того что мы не проиграли
                last_respawn_time = pygame.time.get_ticks() # Зафиксировать текущее время для отсчёта следующего респауна
        elif i.type == pygame.MOUSEBUTTONDOWN: # Проверка, было ли событие нажатия кнопки мыши
            if i.button == pygame.BUTTON_LEFT:  # Проверка, была ли нажата левая кнопка мыши
                if not game_over and target_rect.collidepoint(i.pos): # Проверка, не окончена ли игра и была ли мышь на цели при нажатии
                    score += 1 # Увеличение счёта на 1
                    respawn_target() # Вызов функции для появления цели в новом месте
                    last_respawn_time = pygame.time.get_ticks()  # Обновление времени последнего появления цели
                    finish_delay = INIT_DELAY / (DECREASE_BASE ** score) # Уменьшение задержки на основе текущего счёта

    clock.tick(FPS)  # Обновление игры с фиксированной частотой кадров

    screen.fill((255, 208, 202)) # Заливание экрана в красный цвет
    score_surface = ARIAL_64.render(str(score), True, (0, 0, 0)) # .render принимает строку, поэтому нужно str которое конвертирует числа в строку
    score_rect = score_surface.get_rect() # Получаем прямоугольную область для размещения текста на экране

    now = pygame.time.get_ticks() # Текущее время
    elapsed = now - last_respawn_time # Сколько прошло времени с предыдущего до текущего
    if elapsed > finish_delay: # Если сейчас прошло больше времени чем задержка на конец игры
        game_over = True # Окончание игры

        score_rect.midbottom = SCREEN_CENTER # Смещение текста в центр

        screen.blit(RETRY_SURFACE, RETRY_RECT) # Отображение текста о проигрыше
    else:
        h = H -  H * elapsed / finish_delay  # Вычисление высоты оставшегося времени
        time_rect = pygame.Rect((0, 0), (W, h))  # Создание прямоугольника для отображения оставшегося времени
        time_rect.bottomleft = (0, H) # Выравнивание прямоугольника по нижней середине экрана
        pygame.draw.rect(screen, (232, 255, 208), time_rect) # Рисование прямоугольника с таймером

        screen.blit(TARGET_IMAGE, target_rect) # Указание, что и где мы хотим нарисовать

        score_rect.midtop = SCREEN_TOP # Указание, где будут показываться очки
    screen.blit(score_surface, score_rect)

    pygame.display.flip() # Обновление дисплея для отображения всех изменений на экране

pygame.quit() # Выход из игры

# Код был взят с канала Sima Games
# Видео - https://www.youtube.com/watch?v=ukYaHhYcvKo&t=906s&ab_channel=SimaGames