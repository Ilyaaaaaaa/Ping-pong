import pygame
import random
import pygame.mixer

# Настройки
r1, g1, b1 = random.randint(0, 80), random.randint(0, 80), random.randint(0, 80)
r2, g2, b2 = random.randint(175, 255), random.randint(175, 255), random.randint(175, 255)
WIDTH, HEIGHT = 1280, 800
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 120
BALL_SIZE = 15
WHITE = (r1, g1, b1)
BG_COLOR = (r2, g2, b2)
PADDLE_SPEED = 7
BALL_SPEED = 5
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг")

font_score = pygame.font.Font(None, 36)
font_pause = pygame.font.Font(None, 70)

pygame.mixer.init()
pygame.mixer.music.load("music.wav")
pygame.mixer.music.play(-1)
rebound = pygame.mixer.Sound("rebound.wav")
score = pygame.mixer.Sound("score.wav")
teleport = pygame.mixer.Sound("teleport.wav")

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

    paddle1 = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    paddle2 = Paddle(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and not finish and not paused:
                    pygame.mixer.music.pause()
                    paused = True
                elif event.key == pygame.K_p and not finish and paused:
                    pygame.mixer.music.unpause()
                    paused = False
                if event.key == pygame.K_r:
                    teleport.play()
                    score1 = score2 = 0
                    ball.reset()
                    paddle1 = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
                    paddle2 = Paddle(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
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

            # Обработка столкновений мяча с краями
            if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
                rebound.play()
                ball.dy *= -1

            # Обработка столкновений мяча с ракетками
            if ball.rect.colliderect(paddle1) or ball.rect.colliderect(paddle2):
                rebound.play()
                ball.dx *= -1

            # Обработка случайного счета
            if ball.rect.left <= 0:
                score2 += 1
                score.play()
                ball.reset()
            elif ball.rect.right >= WIDTH:
                score1 += 1
                score.play()
                ball.reset()

            # Определение завершения игры
            if score1 == max_score or score2 == max_score:
                finish = True

        # Отрисовка
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, WHITE, paddle1.rect)
        pygame.draw.rect(screen, WHITE, paddle2.rect)
        pygame.draw.ellipse(screen, WHITE, ball.rect)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Отображение счета
        score_display = font_score.render(f'{score1} : {score2}', True, WHITE)
        screen.blit(score_display, (WIDTH // 2 - score_display.get_width() // 2, 20))

        # Отображение паузы
        if paused:
            pause_text = font_pause.render('Пауза', True, WHITE)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))

        # Отображение окончания игры
        if finish:
            finish_text = font_pause.render('Игра окончена,', True, WHITE)
            screen.blit(finish_text, (WIDTH // 2 - finish_text.get_width() // 2, HEIGHT // 2 - finish_text.get_height() // 2))
            if score1 > score2:
                restart_text = font_pause.render('Игрок №1 победил!', True, WHITE)
            else:
                restart_text = font_pause.render('Игрок №1 победил!', True, WHITE)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
