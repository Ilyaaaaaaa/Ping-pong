import pygame
import random

# Определение размеров и характеристик
WIDTH, HEIGHT = 1120, 700
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 120
BALL_SIZE = 15
PADDLE_SPEED = 7
BALL_SPEED = 5
FPS = 60

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг")

# Функция для генерации цветов
def random_color():
    r1, g1, b1 = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    r2, g2, b2 = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    while (abs(r1 - r2) < 150 and abs(g1 - g2) < 150 and abs(b1 - b2) < 150) or \
          (abs(r1 - r2) > 150 and abs(g1 - g2) > 150 and abs(b1 - b2) > 150):
        r2, g2, b2 = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    return (r1, g1, b1), (r2, g2, b2)

# Определение классов
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, dy):
        self.rect.y += dy
        # Ограничение движения ракетки
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Ball:
    def __init__(self):
        self.reset()

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def reset(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.dx = BALL_SPEED * random.choice([-1, 1])
        self.dy = BALL_SPEED * random.choice([-1, 1])

def main():
    clock = pygame.time.Clock()
    running = True
    paused = False
    finish = False
    score1 = 0
    score2 = 0
    max_score = 9

    color1, color2 = random_color()  # Генерация цветов
    paddle1 = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    paddle2 = Paddle(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball()

    font_score = pygame.font.Font(None, 36)
    font_pause = pygame.font.Font(None, 70)

    pygame.mixer.init()
    pygame.mixer.music.load("music.wav")
    pygame.mixer.music.play(-1)
    rebound = pygame.mixer.Sound("rebound.wav")
    score_sound = pygame.mixer.Sound("score.wav")
    teleport = pygame.mixer.Sound("teleport.wav")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and not finish:
                    paused = not paused
                    if paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                if event.key == pygame.K_r:
                    color1, color2 = random_color()
                    score1 = score2 = 0
                    ball.reset()
                    paddle1.rect.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
                    paddle2.rect.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
                    paused = False
                    finish = False

        keys = pygame.key.get_pressed()
        if not paused and not finish:
            # Движение ракеток
            if keys[pygame.K_w]:
                paddle1.move(-PADDLE_SPEED)
            if keys[pygame.K_s]:
                paddle1.move(PADDLE_SPEED)
            if keys[pygame.K_UP]:
                paddle2.move(-PADDLE_SPEED)
            if keys[pygame.K_DOWN]:
                paddle2.move(PADDLE_SPEED)

            # Движение мяча
            ball.move()

            # Столкновения мяча с краями
            if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
                rebound.play()
                ball.dy *= -1

            # Столкновения мяча с ракетками
            if ball.rect.colliderect(paddle1) or ball.rect.colliderect(paddle2):
                rebound.play()
                ball.dx *= -1

            # Проверка счета
            if ball.rect.left <= 0:
                score2 += 1
                score_sound.play()
                ball.reset()
            elif ball.rect.right >= WIDTH:
                score1 += 1
                score_sound.play()
                ball.reset()

            # Проверка конца игры
            if score1 == max_score or score2 == max_score:
                finish = True

        # Отрисовка
        screen.fill(color2)
        pygame.draw.rect(screen, color1, paddle1.rect)
        pygame.draw.rect(screen, color1, paddle2.rect)
        pygame.draw.ellipse(screen, color1, ball.rect)
        pygame.draw.aaline(screen, color1, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Отображение счета
        score_display = font_score.render(f'{score1} : {score2}', True, color1)
        screen.blit(score_display, (WIDTH // 2 - score_display.get_width() // 2, 20))

        # Сообщение паузы
        if paused:
            pause_text = font_pause.render('Пауза', True, color1)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))

        # Сообщение окончания игры
        if finish:
            finish_text = font_pause.render('Игра окончена,', True, color1)
            screen.blit(finish_text, (WIDTH // 2 - finish_text.get_width() // 2, HEIGHT // 2 - finish_text.get_height() // 2))
            if score1 > score2:
                restart_text = font_pause.render('Игрок 1 победил!', True, color1)
            else:
                restart_text = font_pause.render('Игрок 2 победил!', True, color1)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
