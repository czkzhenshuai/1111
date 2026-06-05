#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <conio.h>
#include <time.h>

#define WIDTH 40
#define HEIGHT 20
#define MAX_SNAKE 100

typedef struct {
    int x;
    int y;
} Point;

typedef struct {
    Point body[MAX_SNAKE];
    int length;
    int dx;
    int dy;
} Snake;

typedef struct {
    int x;
    int y;
} Food;

int gameOver = 0;
int score = 0;

void init(Snake *snake, Food *food) {
    // 初始化蛇
    snake->length = 3;
    snake->body[0].x = WIDTH / 2;
    snake->body[0].y = HEIGHT / 2;
    snake->body[1].x = WIDTH / 2 - 1;
    snake->body[1].y = HEIGHT / 2;
    snake->body[2].x = WIDTH / 2 - 2;
    snake->body[2].y = HEIGHT / 2;
    
    snake->dx = 1;
    snake->dy = 0;
    
    // 初始化食物
    srand(time(NULL));
    food->x = rand() % WIDTH;
    food->y = rand() % HEIGHT;
    
    score = 0;
}

void draw(Snake *snake, Food *food) {
    system("clear");
    
    // 绘制边框和游戏区域
    for (int i = 0; i < WIDTH + 2; i++) {
        printf("=");
    }
    printf("\n");
    
    for (int y = 0; y < HEIGHT; y++) {
        printf("|");
        for (int x = 0; x < WIDTH; x++) {
            int printed = 0;
            
            // 绘制蛇
            for (int i = 0; i < snake->length; i++) {
                if (snake->body[i].x == x && snake->body[i].y == y) {
                    printf("%c", i == 0 ? '@' : '*');
                    printed = 1;
                    break;
                }
            }
            
            // 绘制食物
            if (!printed && food->x == x && food->y == y) {
                printf("F");
                printed = 1;
            }
            
            // 空白
            if (!printed) {
                printf(" ");
            }
        }
        printf("|\n");
    }
    
    for (int i = 0; i < WIDTH + 2; i++) {
        printf("=");
    }
    printf("\n");
    printf("Score: %d | Length: %d\n", score, snake->length);
    printf("Controls: W(up) S(down) A(left) D(right) Q(quit)\n");
}

void input(Snake *snake) {
    if (kbhit()) {
        char ch = getch();
        switch (ch) {
            case 'w':
            case 'W':
                if (snake->dy == 0) {
                    snake->dx = 0;
                    snake->dy = -1;
                }
                break;
            case 's':
            case 'S':
                if (snake->dy == 0) {
                    snake->dx = 0;
                    snake->dy = 1;
                }
                break;
            case 'a':
            case 'A':
                if (snake->dx == 0) {
                    snake->dx = -1;
                    snake->dy = 0;
                }
                break;
            case 'd':
            case 'D':
                if (snake->dx == 0) {
                    snake->dx = 1;
                    snake->dy = 0;
                }
                break;
            case 'q':
            case 'Q':
                gameOver = 1;
                break;
        }
    }
}

void update(Snake *snake, Food *food) {
    // 蛇移动 - 添加新头部
    Point newHead;
    newHead.x = snake->body[0].x + snake->dx;
    newHead.y = snake->body[0].y + snake->dy;
    
    // 检查撞墙
    if (newHead.x < 0 || newHead.x >= WIDTH || newHead.y < 0 || newHead.y >= HEIGHT) {
        gameOver = 1;
        return;
    }
    
    // 检查撞自己
    for (int i = 0; i < snake->length; i++) {
        if (newHead.x == snake->body[i].x && newHead.y == snake->body[i].y) {
            gameOver = 1;
            return;
        }
    }
    
    // 把所有身体向后移动
    for (int i = snake->length; i > 0; i--) {
        snake->body[i] = snake->body[i - 1];
    }
    snake->body[0] = newHead;
    
    // 检查是否吃到食物
    if (newHead.x == food->x && newHead.y == food->y) {
        snake->length++;
        score += 10;
        
        // 生成新食物
        food->x = rand() % WIDTH;
        food->y = rand() % HEIGHT;
        
        // 检查食物是否在蛇身上
        int onSnake = 0;
        for (int i = 0; i < snake->length; i++) {
            if (food->x == snake->body[i].x && food->y == snake->body[i].y) {
                onSnake = 1;
                break;
            }
        }
        if (onSnake) {
            food->x = rand() % WIDTH;
            food->y = rand() % HEIGHT;
        }
    }
}

int main() {
    Snake snake;
    Food food;
    
    init(&snake, &food);
    
    printf("欢迎来到贪吃蛇游戏!\n");
    printf("按任意键开始...\n");
    getch();
    
    while (!gameOver) {
        draw(&snake, &food);
        input(&snake);
        update(&snake, &food);
        usleep(100000); // 100ms延迟
    }
    
    system("clear");
    printf("游戏结束!\n");
    printf("最终得分: %d\n", score);
    printf("蛇的长度: %d\n", snake.length);
    
    return 0;
}
