import pygame
import random
import sys
from enum import Enum
from collections import deque

# 初始化 Pygame
pygame.init()

# 游戏常量
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 180, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

# 方向枚举
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("贪吃蛇游戏")
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 48)
        
        self.reset_game()
        
    def reset_game(self):
        """重置游戏状态"""
        # 蛇初始位置：从中间开始，长度为3
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.snake = deque([
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y)
        ])
        
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.speed = 8  # 初始速度
        
    def spawn_food(self):
        """随机生成食物"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                # 方向控制
                if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.next_direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.next_direction = Direction.DOWN
                elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.next_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.next_direction = Direction.RIGHT
                
                # 暂停/继续
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                
                # 重新开始
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                
                # 退出
                elif event.key == pygame.K_ESCAPE:
                    return False
        
        return True
    
    def update(self):
        """更新游戏状态"""
        if self.game_over or self.paused:
            return
        
        # 更新方向
        self.direction = self.next_direction
        
        # 计算新的蛇头位置
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # 检查碰撞：撞墙
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.game_over = True
            return
        
        # 检查碰撞：咬到自己
        if new_head in self.snake:
            self.game_over = True
            return
        
        # 添加新的蛇头
        self.snake.appendleft(new_head)
        
        # 检查是否吃到食物
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
            # 随着分数增加，速度也增加
            self.speed = min(15, 8 + self.score // 100)
        else:
            # 如果没有吃到食物，移除蛇尾
            self.snake.pop()
    
    def draw(self):
        """绘制游戏画面"""
        self.screen.fill(BLACK)
        
        # 绘制网格（可选，用于参考）
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_HEIGHT), 1)
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_WIDTH, y), 1)
        
        # 绘制蛇
        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(x * GRID_SIZE + 2, y * GRID_SIZE + 2, 
                              GRID_SIZE - 4, GRID_SIZE - 4)
            if i == 0:
                # 蛇头用更深的绿色
                pygame.draw.rect(self.screen, DARK_GREEN, rect)
            else:
                # 蛇身用绿色
                pygame.draw.rect(self.screen, GREEN, rect)
        
        # 绘制食物
        food_rect = pygame.Rect(self.food[0] * GRID_SIZE + 2, 
                               self.food[1] * GRID_SIZE + 2,
                               GRID_SIZE - 4, GRID_SIZE - 4)
        pygame.draw.rect(self.screen, RED, food_rect)
        
        # 绘制分数
        score_text = self.font_small.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 绘制速度
        speed_text = self.font_small.render(f"Speed: {self.speed}", True, WHITE)
        self.screen.blit(speed_text, (WINDOW_WIDTH - 150, 10))
        
        # 绘制暂停提示
        if self.paused:
            pause_text = self.font_large.render("PAUSED", True, YELLOW)
            text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(pause_text, text_rect)
        
        # 绘制游戏结束画面
        if self.game_over:
            # 半透明背景
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # 游戏结束文字
            game_over_text = self.font_large.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
            self.screen.blit(game_over_text, game_over_rect)
            
            # 分数显示
            final_score_text = self.font_small.render(f"Final Score: {self.score}", True, WHITE)
            final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(final_score_text, final_score_rect)
            
            # 重新开始提示
            restart_text = self.font_small.render("Press R to Restart or ESC to Quit", True, YELLOW)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def run(self):
        """游戏主循环"""
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.speed)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
