import sys
import pygame
import random

blue = (0, 191, 255)
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)
purple = (106, 90, 205)

display_width = 500
half_w = display_width / 2
display_height = 600
half_h = display_height / 2
display_height += 75


#-----------------------------------------------------------------------------
# Snake body and snake unit 
class Snake:
    def __init__(self) -> None:
        self.block_size = 10
        snake_unit = []
        self.snake_body = []
        snake_body_size = 5
        for i in range(0, snake_body_size):
            snake_unit = [half_w + i * self.block_size, half_h]
            self.snake_body.append(snake_unit)
        
    def move(self, move_step, eat_food):
        snake_body_size = len(self.snake_body)
        snake_head = self.snake_body[snake_body_size -1]
        snake_head_new = [snake_head[0] + move_step[0], snake_head[1] + move_step[1]]
        self.snake_body.append(snake_head_new)
        if not eat_food:
            del self.snake_body[0]
        return self.snake_body
    
    def get_snake_body(self):
        return self.snake_body
    
    def get_snake_unit_size(self):
        return self.block_size
    
    def get_snake_size(self):
        return len(self.snake_body)
    
    def get_snake_head(self):
        return self.snake_body[len(self.snake_body) -1]
    
    def draw(self, gameDisplay):
        for i in self.snake_body:
            pygame.draw.rect(gameDisplay, blue, [i[0], i[1], self.block_size, self.block_size])

class Food:
    def __init__(self, x, y, basic_color) -> None:
        self.block_size = 10
        self.x = x
        self.y = y
        self.count = 0
        self.basic_color = basic_color
        self.food_color_incr = 255
        food_cod_temp = self.__gen_cod()
        self.food_cod = [food_cod_temp[0], food_cod_temp[1]]

    def __gen_cod(self):
        food_x = round(random.randrange(0, self.x - self.block_size - 75) / 10) * 10
        food_y = round(random.randrange(0, self.y - self.block_size - 75) / 10) * 10
        return [food_x, food_y]
    
    def refresh(self):
        food_cod_temp = self.__gen_cod()
        self.food_cod = [food_cod_temp[0], food_cod_temp[1]]
        return self.food_cod
    
    def food_eaten(self):
        self.count += 1
        self.refresh()
    
    def get_food_count(self):
        return self.count
    
    def get_food_cod(self):
        return self.food_cod
    
    def draw(self, gameDisplay):
        self.food_color_incr -= 30
        if self.food_color_incr <= 0:
            self.food_color_incr = 255
        pygame.draw.rect(gameDisplay, (255, self.food_color_incr, self.food_color_incr), \
                         [self.food_cod[0], self.food_cod[1], self.block_size, self.block_size])
        
class GameInfo:
    def __init__(self, y) -> None:
        self.y = y

    def draw(self, gameDisplay, font, score, level, snake_head, message):
        pygame.draw.line(gameDisplay, purple, [0, display_height - self.y], [display_width, display_height - self.y], 2)
        msg = font.render(f"Message: {message}", True, purple)
        info = font.render(f"Score: {score}|Level: {level+1}| X:{snake_head[0]} Y:{snake_head[1]}", True, purple)
        help_msg = font.render(f"Press Q to quit, SPACE to replay", True, purple)
        gameDisplay.blit(msg, [10, display_height - (self.y - 50)])
        gameDisplay.blit(info, [10, display_height - (self.y - 30)])
        gameDisplay.blit(help_msg, [10, display_height - (self.y - 10)])

class GameManager:
    def __init__(self, game_display) -> None:
        self.snake = Snake()
        self.food = Food(display_width, display_height, 255)
        self.game_display = game_display
        self.move_step = [self.snake.get_snake_unit_size(), 0]
        self.game_info = GameInfo(75)
        self.font = pygame.font.SysFont(None, 20)
        
    
    def work(self):
        if not self.check_game_over():
            message = "Running..."
            if self.check_eat_food():
                self.snake.move(self.move_step, True)
                self.food.food_eaten()
            else:
                self.snake.move(self.move_step, False)
            self.food.draw(self.game_display)

        else:
            message = "Game Over"
        
        self.snake.draw(self.game_display)
        self.game_info.draw(self.game_display, self.font, self.food.get_food_count() * 10, \
                            int(self.food.get_food_count() / 10), self.snake.get_snake_head(), message)
        
    def handle_key_down(self, key):
        if key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
            if key == pygame.K_DOWN:
                move_step = [0, self.snake.get_snake_unit_size()]
            elif key == pygame.K_UP:
                move_step = [0, -self.snake.get_snake_unit_size()]
            elif key == pygame.K_LEFT:
                move_step = [-self.snake.get_snake_unit_size(), 0]
            elif key == pygame.K_RIGHT:
                move_step = [self.snake.get_snake_unit_size(), 0]
            self.move_step = move_step
    
    def check_eat_food(self):
        if self.snake.get_snake_head()[0] == self.food.get_food_cod()[0] and \
            self.snake.get_snake_head()[1] == self.food.get_food_cod()[1]:
            return True
        else:
            return False
        
    def check_game_over(self):
        if self.snake.get_snake_head()[0] <= 0 or self.snake.get_snake_head()[0] >= display_width or \
            self.snake.get_snake_head()[1] <= 0 or self.snake.get_snake_head()[1] >= display_height-85:
            return True
        else:
            return False
        
class Game:
    def __init__(self) -> None:
        
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('Snake Game')
        self.game_display = pygame.display.set_mode((display_width, display_height))
        self.clock = pygame.time.Clock()
        font = pygame.font.SysFont(None, 20)
        self.gameManager = GameManager(self.game_display)

        bg_img = pygame.image.load("nyu.jpg")
        self.bg_image = pygame.transform.scale(bg_img, (display_width, display_height))

    def play(self):
        while True:
            self.clock.tick(20)
            self.game_display.fill(black)
            self.game_display.blit(self.bg_image, (0, 0))
            for event in pygame.event.get():
                #if event.type == pygame.QUIT:
                   # print("Close the window!")
                    #pygame.quit()
                    #sys.exit(0)
                    

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        #sys.exit(0)
                        return("Snake")
                    elif event.key == pygame.K_SPACE:
                        self.gameManager = GameManager(self.game_display)
                    else:
                        self.gameManager.handle_key_down(event.key)

            self.gameManager.work()
            pygame.display.update()
            pygame.display.flip()

if __name__ == "__main__":
    #game = Game()
    #game.play()
    pass