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
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.dx = BALL_SPEED * random.choice([-1, 1])
        self.dy = BALL_SPEED * random.choice([-1, 1])
    
    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def reset(self):
        self.rect.x = WIDTH // 2 - BALL_SIZE // 2
        self.rect.y = HEIGHT // 2 - BALL_SIZE // 2
        self.dx *= random.choice([-1, 1])
        self.dy *= random.choice([-1, 1])

def main():
    clock = pygame.time.Clock()
    running = True
    paused = False
    finish = False
    score1 = 0
    score2 = 0
    max_score = 9  # Define maximum score for game over

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
            # Paddle movement
            if keys[pygame.K_w]:
                paddle1.move(-PADDLE_SPEED)
            if keys[pygame.K_s]:
                paddle1.move(PADDLE_SPEED)
            if keys[pygame.K_UP]:
                paddle2.move(-PADDLE_SPEED)
            if keys[pygame.K_DOWN]:
                paddle2.move(PADDLE_SPEED)

            # Ball movement
            ball.move()

            # Ball collision with the edges
            if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
                rebound.play()
                ball.dy *= -1

            # Ball collision with paddles
            if ball.rect.colliderect(paddle1.rect) or ball.rect.colliderect(paddle2.rect):
                rebound.play()
                ball.dx *= -1
                angle = random.randint(35, 55)
                ball.dy = BALL_SPEED * (random.choice([1, -1]) * (angle / 90))

            # Scoring
            if ball.rect.x < 15 or ball.rect.x > WIDTH - 15:
                score.play()
                if ball.rect.x < 15:
                    score2 += 1
                else:
                    score1 += 1
                ball.reset()


            # Game over check
            if score1 >= max_score or score2 >= max_score:
                paused = True  # Pause the game when there's a winner
                finish = True
                if score1 >= max_score:
                    winner_text = "Игрок 1 выиграл!"  
                else:
                    winner_text = "Игрок 2 выиграл!" 
                game_over_text = font_pause.render(winner_text, True, WHITE)
            else:
                game_over_text = None

        # Render
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, WHITE, paddle1.rect)
        pygame.draw.rect(screen, WHITE, paddle2.rect)
        pygame.draw.ellipse(screen, WHITE, ball.rect)

        # Display score
        score_text = font_score.render(f"{score1}:{score2}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 15))

        # Show pause message
        if paused and not finish:
            pause_text = font_pause.render("ПАУЗА", True, WHITE)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))
        if game_over_text:
            pygame.mixer.music.pause()
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 + 50))
        else:
            if not paused and not finish:
                pygame.mixer.music.unpause()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
