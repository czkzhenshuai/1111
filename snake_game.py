import pygame
import random
from enum import Enum
from collections import deque

# 初始化Pygame
pygame.init()

# 定义颜色
class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)

# 定义方向
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class SnakeGame:
    def __init__(self, width=800, height=600, block_size=20):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.grid_width = width // block_size
        self.grid_height = height // block_size
        
        # 初始化屏幕
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('贪吃蛇游戏')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        # 游戏状态
        self.reset_game()
    
    def reset_game(self):
        """重置游戏"""
        # 蛇的初始位置（使用deque以便快速移除尾部）
        self.snake = deque([
            (self.grid_width // 2, self.grid_height // 2),
            (self.grid_width // 2 - 1, self.grid_height // 2),
            (self.grid_width // 2 - 2, self.grid_height // 2)
        ])
        
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
    
    def spawn_food(self):
        """生成食物"""
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def handle_input(self):
        """处理输入"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.next_direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.next_direction = Direction.DOWN
                elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.next_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.next_direction = Direction.RIGHT
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
        
        return True
    
    def update(self):
        """更新游戏逻辑"""
        if self.game_over:
            return
        
        self.direction = self.next_direction
        
        # 计算蛇头的新位置
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # 检查碰撞（边界）
        if (new_head[0] < 0 or new_head[0] >= self.grid_width or
            new_head[1] < 0 or new_head[1] >= self.grid_height):
            self.game_over = True
            return
        
        # 检查碰撞（自身）
        if new_head in self.snake:
            self.game_over = True
            return
        
        # 添加新的蛇头
        self.snake.appendleft(new_head)
        
        # 检查是否吃到食物
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
        else:
            # 没有吃到食物，移除蛇尾
            self.snake.pop()
    
    def draw(self):
        """绘制游戏"""
        self.screen.fill(Color.BLACK)
        
        # 绘制蛇
        for i, segment in enumerate(self.snake):
            x = segment[0] * self.block_size
            y = segment[1] * self.block_size
            
            if i == 0:  # 蛇头为绿色
                pygame.draw.rect(self.screen, Color.GREEN, 
                               (x, y, self.block_size, self.block_size))
            else:  # 蛇身为黄色
                pygame.draw.rect(self.screen, Color.YELLOW, 
                               (x, y, self.block_size, self.block_size))
        
        # 绘制食物
        food_x = self.food[0] * self.block_size
        food_y = self.food[1] * self.block_size
        pygame.draw.rect(self.screen, Color.RED, 
                       (food_x, food_y, self.block_size, self.block_size))
        
        # 绘制分数
        score_text = self.font.render(f'Score: {self.score}', True, Color.WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 如果游戏结束，显示消息
        if self.game_over:
            game_over_text = self.font.render('Game Over! Press SPACE to restart', True, Color.RED)
            text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(10)  # 每秒10帧
        
        pygame.quit()

if __name__ == '__main__':
    game = SnakeGame()
    game.run()
