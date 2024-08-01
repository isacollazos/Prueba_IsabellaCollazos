import pygame
import sys
import random

def juego():
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (159, 163, 168)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    CAR_COLOR = (181, 230, 29)
    TEXT_COLOR = (250, 105, 10)
    width = 30

    pygame.init()

    class Car:
        def __init__(self, x=0, y=0, dx=0, dy=0, width=70, height=131, color=RED, image_path=None):
            self.x = x
            self.y = y
            self.dx = dx
            self.dy = dy
            self.width = width
            self.height = height
            self.color = color
            if image_path:
                self.load_image(image_path)

        def load_image(self, filename):
            self.image = pygame.image.load(filename).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        def draw_image(self):
            screen.blit(self.image, [self.x, self.y])

        def check_out_of_screen(self):
            if self.x + self.width > 400 or self.x < 0:
                self.x -= self.dx
            if self.y + self.height > 700 or self.y < 0:
                self.y -= self.dy

    class Coin:
        def __init__(self, x=0, y=0, dy=3, width=50, height=50, image_path=None):
            self.x = x
            self.y = y
            self.dy = dy
            self.width = width
            self.height = height
            if image_path:
                self.load_image(image_path)

        def load_image(self, filename):
            self.image = pygame.image.load(filename).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        def draw_image(self):
            screen.blit(self.image, [self.x, self.y])

        def move_down(self):
            self.y += self.dy

        def reset_position(self, cars):
            while True:
                self.y = random.randrange(-150, -50)
                self.x = random.randrange(0, size[0] - self.width)
                overlap = False
                for car in cars:
                    if (self.x < car.x + car.width and self.x + self.width > car.x and
                        self.y < car.y + car.height and self.y + self.height > car.y):
                        overlap = True
                        break
                if not overlap:
                    break

    def check_collision(player, item):
        if (player.x + player.width > item.x) and (player.x < item.x + item.width) and (player.y < item.y + item.height) and (player.y + player.height > item.y):
            return True
        else:
            return False

    def draw_text(screen, text, font, color, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x, y))
        screen.blit(text_obj, text_rect)

    def draw_button(screen, text, font, color, rect_color, x, y, width, height):
        pygame.draw.rect(screen, rect_color, [x, y, width, height])
        draw_text(screen, text, font, color, x + width / 2, y + height / 2)

    def draw_game_over():
        screen.fill(BLACK)
        draw_text(screen, "GAME OVER", font_40, TEXT_COLOR, size[0] / 2, size[1] / 2 - 50)
        draw_button(screen, "Reiniciar", font_30, TEXT_COLOR, WHITE, size[0] / 2 - 60, size[1] / 2 + 20, 120, 50)
        pygame.display.flip()

    def draw_win_message():
        screen.fill(BLACK)
        draw_text(screen, "¡Ganaste!", font_40, TEXT_COLOR, size[0] / 2, size[1] / 2 - 50)
        draw_button(screen, "Reiniciar", font_30, TEXT_COLOR, WHITE, size[0] / 2 - 60, size[1] / 2 + 20, 120, 50)
        pygame.display.flip()

    def draw_main_menu():
        screen.fill(BLACK)
        draw_text(screen, "Menu Principal", font_40, WHITE, size[0] / 2, size[1] / 2 - 100)
        draw_button(screen, "Nivel 1", font_30, WHITE, BLACK, size[0] / 2 - 60, size[1] / 2 - 40, 120, 50)
        draw_button(screen, "Nivel 2", font_30, WHITE, BLACK, size[0] / 2 - 60, size[1] / 2 + 20, 120, 50)
        pygame.display.flip()

    def main_menu_click(pos):
        x, y = pos
        if size[0] / 2 - 60 <= x <= size[0] / 2 + 60:
            if size[1] / 2 - 40 <= y <= size[1] / 2 + 10:
                return 1 
            elif size[1] / 2 + 20 <= y <= size[1] / 2 + 70:
                return 2  
        return None

    def check_button_click(pos):
        x, y = pos
        if size[0] / 2 - 60 <= x <= size[0] / 2 + 60 and size[1] / 2 + 20 <= y <= size[1] / 2 + 70:
            return True
        return False

    def generate_enemy_positions(car_count, car_width, car_height):
        positions = []
        attempts = 0
        while len(positions) < car_count and attempts < 1000:
            x = random.randrange(0, 400 - car_width)
            y = random.randrange(-150, -50)
            overlap = False
            for pos in positions:
                if x < pos[0] + car_width and x + car_width > pos[0] and y < pos[1] + car_height and y + car_height > pos[1]:
                    overlap = True
                    break
            if not overlap:
                positions.append((x, y))
            attempts += 1
        return positions

    size = (400, 700)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Ride the Road")

   
    done = False
    game_over = False  
    win = False  

    clock = pygame.time.Clock()

  
    player_image_path = "Assets/player.png"
    player = Car(175, 475, 0, 0, 70, 131, RED, player_image_path)

    heart_image_path = "Assets/heart.png"
    heart_image = pygame.image.load(heart_image_path).convert_alpha()
    heart_image = pygame.transform.scale(heart_image, (30, 30))  

    money_image_path = "Assets/money.png"
    money_image = pygame.image.load(money_image_path).convert_alpha()
    money_image = pygame.transform.scale(money_image, (50, 50))  

    
    coins = 0

    player_lives = 5
    invulnerable = False  
    invulnerable_time = 2000 
    last_hit_time = 0  


    font_40 = pygame.font.SysFont("Arial", 40, True, False)
    font_30 = pygame.font.SysFont("Arial", 30, True, False)
    text_title = font_40.render("Ride the Road", True, TEXT_COLOR)
    text_ins = font_30.render("Click to Play!", True, TEXT_COLOR)

    cars = []
    car_count = 1
    for i in range(car_count):
        x = random.randrange(0, 340)
        car = Car(x, random.randrange(-150, -50), 0, random.randint(5, 10), 70, 131, CAR_COLOR, player_image_path)
        cars.append(car)

    stripes = []
    stripe_count = 20
    stripe_x = 185
    stripe_y = -10
    stripe_width = 20
    stripe_height = 80
    space = 20
    for i in range(stripe_count):
        stripes.append([190, stripe_y])
        stripe_y += stripe_height + space

    coin = Coin(random.randrange(0, size[0] - 50), random.randrange(-150, -50), 3, 50, 50, money_image_path)

    def game(level):
        nonlocal coins, player_lives, done, game_over, win, invulnerable, last_hit_time

        car_speed = 3 if level == 1 else 6
        
        coins = 0
        player_lives = 5
        player.x = 175
        player.y = 475
        player.dx = 0
        player.dy = 0
        invulnerable = False
        game_over = False
        win = False
        pygame.mouse.set_visible(False)

        cars.clear()
        positions = generate_enemy_positions(car_count * level, 70, 131)
        for pos in positions:
            x, y = pos
            car = Car(x, y, 0, car_speed, 70, 131, CAR_COLOR, player_image_path)
            cars.append(car)

        coin.reset_position(cars)

        # -------- Main Program Loop -----------
        while not done:
            current_time = pygame.time.get_ticks() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        player.dx = 3
                    elif event.key == pygame.K_LEFT:
                        player.dx = -3
                    elif event.key == pygame.K_UP:
                        player.dy = -3 
                    elif event.key == pygame.K_DOWN:
                        player.dy = 3
                    elif event.key == pygame.K_SPACE:
                        player.dy = 0
                        player.dx = 0

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player.dx = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player.dy = 0

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game_over or win:
                        if check_button_click(event.pos):
                            return 

            if game_over:
                draw_game_over()
                continue

            if win:
                draw_win_message()
                continue

            screen.fill(GRAY)

            for i in range(stripe_count):
                pygame.draw.rect(screen, WHITE, [stripes[i][0], stripes[i][1], stripe_width, stripe_height])
           
            for i in range(stripe_count):
                stripes[i][1] += 3
                if stripes[i][1] > size[1]:
                    stripes[i][1] = -40 - stripe_height

            player.x += player.dx
            player.y += player.dy

            player.draw_image()
            player.check_out_of_screen()

            for i in range(len(cars)):
                cars[i].draw_image()
                cars[i].y += cars[i].dy
                if cars[i].y > size[1]:
                    cars[i].y = random.randrange(-150, -50)
                    cars[i].x = random.randrange(0, 340)
                    cars[i].dy = car_speed

            if not invulnerable:  
                for i in range(len(cars)):
                    if check_collision(player, cars[i]):
                        player_lives -= 1
                        invulnerable = True  
                        last_hit_time = current_time  
                        break

            if invulnerable and (current_time - last_hit_time > invulnerable_time):
                invulnerable = False

            if check_collision(player, coin):
                coins += 1
                coin.reset_position(cars)

            coin.move_down()
            coin.draw_image()
            if coin.y > size[1]:
                coin.reset_position(cars)

            
            txt_coins = font_30.render("Coins: " + str(coins), True, WHITE)
            screen.blit(txt_coins, [15, 15])

            for i in range(player_lives):
                screen.blit(heart_image, [size[0] - 185 + i * 35, 15])

            if coins >= 10:
                win = True

            if player_lives <= 0:
                game_over = True

            pygame.display.flip()
            clock.tick(60)

    def main_menu():
        nonlocal done
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    level = main_menu_click(event.pos)
                    if level is not None:
                        game(level)

            draw_main_menu()
            clock.tick(60)

        pygame.quit()

    main_menu()

if __name__ == "__main__":
    juego()
