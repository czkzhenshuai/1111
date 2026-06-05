// Canvas setup
const canvas = document.getElementById('pongCanvas');
const ctx = canvas.getContext('2d');

// Game variables
const paddleWidth = 10;
const paddleHeight = 80;
const ballSize = 8;
const paddleSpeed = 6;
const ballSpeed = 4;

let playerScore = 0;
let computerScore = 0;

// Player paddle (left side)
const playerPaddle = {
    x: 10,
    y: canvas.height / 2 - paddleHeight / 2,
    width: paddleWidth,
    height: paddleHeight,
    dy: 0,
    maxSpeed: paddleSpeed
};

// Computer paddle (right side)
const computerPaddle = {
    x: canvas.width - paddleWidth - 10,
    y: canvas.height / 2 - paddleHeight / 2,
    width: paddleWidth,
    height: paddleHeight,
    dy: 0,
    maxSpeed: paddleSpeed * 0.8 // Slightly slower than player
};

// Ball
const ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    size: ballSize,
    dx: ballSpeed,
    dy: ballSpeed,
    maxSpeed: 7
};

// Input handling
const keys = {};
let mouseY = canvas.height / 2;

// Keyboard events
document.addEventListener('keydown', (e) => {
    keys[e.key] = true;
});

document.addEventListener('keyup', (e) => {
    keys[e.key] = false;
});

// Mouse movement
document.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouseY = e.clientY - rect.top;
});

// Update player paddle position
function updatePlayerPaddle() {
    // Arrow keys control
    if (keys['ArrowUp'] || keys['w'] || keys['W']) {
        playerPaddle.dy = -playerPaddle.maxSpeed;
    } else if (keys['ArrowDown'] || keys['s'] || keys['S']) {
        playerPaddle.dy = playerPaddle.maxSpeed;
    } else {
        // Mouse control
        const paddleCenter = playerPaddle.y + playerPaddle.height / 2;
        const diff = mouseY - paddleCenter;
        
        if (Math.abs(diff) > 5) {
            playerPaddle.dy = Math.sign(diff) * playerPaddle.maxSpeed;
        } else {
            playerPaddle.dy = 0;
        }
    }

    // Update paddle position
    playerPaddle.y += playerPaddle.dy;

    // Wall collision for player paddle
    if (playerPaddle.y < 0) {
        playerPaddle.y = 0;
    } else if (playerPaddle.y + playerPaddle.height > canvas.height) {
        playerPaddle.y = canvas.height - playerPaddle.height;
    }
}

// Update computer paddle position (AI)
function updateComputerPaddle() {
    const computerPaddleCenter = computerPaddle.y + computerPaddle.height / 2;
    const diff = ball.y - computerPaddleCenter;

    // AI difficulty: track the ball with slight delay
    if (Math.abs(diff) > 10) {
        computerPaddle.dy = Math.sign(diff) * computerPaddle.maxSpeed;
    } else {
        computerPaddle.dy = 0;
    }

    // Update paddle position
    computerPaddle.y += computerPaddle.dy;

    // Wall collision for computer paddle
    if (computerPaddle.y < 0) {
        computerPaddle.y = 0;
    } else if (computerPaddle.y + computerPaddle.height > canvas.height) {
        computerPaddle.y = canvas.height - computerPaddle.height;
    }
}

// Update ball position
function updateBall() {
    ball.x += ball.dx;
    ball.y += ball.dy;

    // Wall collision (top and bottom)
    if (ball.y - ball.size < 0 || ball.y + ball.size > canvas.height) {
        ball.dy *= -1;
        // Clamp ball position to prevent it from going too far
        if (ball.y - ball.size < 0) {
            ball.y = ball.size;
        } else {
            ball.y = canvas.height - ball.size;
        }
    }

    // Paddle collision - Player paddle
    if (
        ball.x - ball.size < playerPaddle.x + playerPaddle.width &&
        ball.y > playerPaddle.y &&
        ball.y < playerPaddle.y + playerPaddle.height
    ) {
        ball.dx *= -1;
        ball.x = playerPaddle.x + playerPaddle.width + ball.size;

        // Add spin based on where ball hits paddle
        const hitPos = (ball.y - (playerPaddle.y + playerPaddle.height / 2)) / (playerPaddle.height / 2);
        ball.dy += hitPos * 2;

        // Increase ball speed slightly with max limit
        if (Math.abs(ball.dx) < ball.maxSpeed) {
            ball.dx *= 1.05;
        }
        if (Math.abs(ball.dy) < ball.maxSpeed) {
            ball.dy *= 1.05;
        }
    }

    // Paddle collision - Computer paddle
    if (
        ball.x + ball.size > computerPaddle.x &&
        ball.y > computerPaddle.y &&
        ball.y < computerPaddle.y + computerPaddle.height
    ) {
        ball.dx *= -1;
        ball.x = computerPaddle.x - ball.size;

        // Add spin based on where ball hits paddle
        const hitPos = (ball.y - (computerPaddle.y + computerPaddle.height / 2)) / (computerPaddle.height / 2);
        ball.dy += hitPos * 2;

        // Increase ball speed slightly with max limit
        if (Math.abs(ball.dx) < ball.maxSpeed) {
            ball.dx *= 1.05;
        }
        if (Math.abs(ball.dy) < ball.maxSpeed) {
            ball.dy *= 1.05;
        }
    }

    // Scoring - left side (computer scores)
    if (ball.x - ball.size < 0) {
        computerScore++;
        updateScore();
        resetBall();
    }

    // Scoring - right side (player scores)
    if (ball.x + ball.size > canvas.width) {
        playerScore++;
        updateScore();
        resetBall();
    }
}

// Reset ball to center
function resetBall() {
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    ball.dx = ballSpeed * (Math.random() > 0.5 ? 1 : -1);
    ball.dy = ballSpeed * (Math.random() * 2 - 1);
}

// Update score display
function updateScore() {
    document.getElementById('playerScore').textContent = playerScore;
    document.getElementById('computerScore').textContent = computerScore;
}

// Draw functions
function drawPaddle(paddle) {
    ctx.fillStyle = '#00ff88';
    ctx.fillRect(paddle.x, paddle.y, paddle.width, paddle.height);
    ctx.shadowColor = '#00ff88';
    ctx.shadowBlur = 10;
    ctx.fillRect(paddle.x, paddle.y, paddle.width, paddle.height);
    ctx.shadowBlur = 0;
}

function drawBall() {
    ctx.fillStyle = '#ffeb3b';
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowColor = '#ffeb3b';
    ctx.shadowBlur = 15;
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;
}

function drawCenter() {
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.stroke();
    ctx.setLineDash([]);
}

function draw() {
    // Clear canvas
    ctx.fillStyle = '#1a1a2e';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw center line
    drawCenter();

    // Draw paddles and ball
    drawPaddle(playerPaddle);
    drawPaddle(computerPaddle);
    drawBall();
}

// Game loop
function gameLoop() {
    updatePlayerPaddle();
    updateComputerPaddle();
    updateBall();
    draw();

    requestAnimationFrame(gameLoop);
}

// Start game
resetBall();
gameLoop();
