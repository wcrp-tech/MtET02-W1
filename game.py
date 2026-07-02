<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>เกมงูคลาสสิก (Snake Game)</title>
    <style>
        body {
            background-color: #222;
            color: white;
            font-family: 'Arial', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        h1 {
            margin-bottom: 10px;
        }
        #scoreBoard {
            font-size: 24px;
            margin-bottom: 20px;
        }
        canvas {
            border: 4px solid #fff;
            background-color: #111;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
        }
        .controls {
            margin-top: 15px;
            font-size: 14px;
            color: #aaa;
        }
    </style>
</head>
<body>

    <h1>SNAKE GAME</h1>
    <div id="scoreBoard">คะแนน: <span id="score">0</span></div>
    <canvas id="gameCanvas" width="400" height="400"></canvas>
    <div class="controls">ใช้ปุ่มลูกศร (Arrow Keys) บนคีย์บอร์ดเพื่อบังคับเลี้ยว</div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreElement = document.getElementById("score");

        const gridSize = 20;
        const tileCount = canvas.width / gridSize;

        // ตัวแปรของงู
        let snake = [{x: 10, y: 10}];
        let dx = 1; // ความเร็วแนวแกน X (เริ่มจากวิ่งไปขวา)
        let dy = 0; // ความเร็วแนวแกน Y

        // ตัวแปรของอาหาร
        let foodX = Math.floor(Math.random() * tileCount);
        let foodY = Math.floor(Math.random() * tileCount);

        let score = 0;
        let gameInterval;
        const gameSpeed = 100; // ความเร็วเกม (มิลลิวินาที ยิ่งน้อยยิ่งเร็ว)

        // เริ่มรันเกม
        function startGame() {
            gameInterval = setInterval(updateGame, gameSpeed);
        }

        // ฟังก์ชันหลักที่ทำงานทุกๆ loop
        function updateGame() {
            moveSnake();

            if (checkGameOver()) {
                clearInterval(gameInterval);
                alert(`เกมจบแล้ว! คุณได้คะแนน: ${score}\nกดตกลงเพื่อเริ่มใหม่`);
                resetGame();
                return;
            }

            checkFoodCollision();
            drawGrid();
        }

        // วาดทุกอย่างลงบนหน้าจอ
        function drawGrid() {
            // ล้างหน้าจอเก่า
            ctx.fillStyle = "#111";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // วาดงู
            ctx.fillStyle = "#4CAF50"; // สีเขียว
            snake.forEach((part, index) => {
                // หัวงูให้สีเข้มกว่าหน่อย
                if (index === 0) ctx.fillStyle = "#2E7D32";
                else ctx.fillStyle = "#4CAF50";
                
                ctx.fillRect(part.x * gridSize, part.y * gridSize, gridSize - 2, gridSize - 2);
            });

            // วาดอาหาร
            ctx.fillStyle = "#FF5252"; // สีแดง
            ctx.fillRect(foodX * gridSize, foodY * gridSize, gridSize - 2, gridSize - 2);
        }

        // เคลื่อนที่งู
        function moveSnake() {
            const head = {x: snake[0].x + dx, y: snake[0].y + dy};
            snake.unshift(head); // เพิ่มหัวใหม่ไปข้างหน้า
            snake.pop(); // ตัดหางออกเพื่อให้ขนาดเท่าเดิม (ถ้าไม่ได้กินอาหาร)
        }

        // ตรวจสอบการชน (ชนกำแพง หรือ ชนตัวเอง)
        function checkGameOver() {
            const head = snake[0];

            // ชนกำแพง
            if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
                return true;
            }

            // ชนตัวเอง
            for (let i = 1; i < snake.length; i++) {
                if (head.x === snake[i].x && head.y === snake[i].y) {
                    return true;
                }
            }
            return false;
        }

        // ตรวจสอบว่างูกินอาหารหรือยัง
        function checkFoodCollision() {
            const head = snake[0];
            if (head.x === foodX && head.y === foodY) {
                score += 10;
                scoreElement.innerText = score;
                
                // ขยายตัวงู (โดยการเพิ่มส่วนหางจำลองกลับเข้าไป)
                snake.push({}); 
                
                // สุ่มตำแหน่งอาหารใหม่
                generateFood();
            }
        }

        // สุ่มอาหารใหม่โดยไม่ให้ทับตัวงู
        function generateFood() {
            foodX = Math.floor(Math.random() * tileCount);
            foodY = Math.floor(Math.random() * tileCount);
            
            // ถ้าสุ่มโดนตัวงู ให้สุ่มใหม่
            snake.forEach(part => {
                if (part.x === foodX && part.y === foodY) {
                    generateFood();
                }
            });
        }

        // รีเซ็ตเกมเพื่อเล่นใหม่
        function resetGame() {
            snake = [{x: 10, y: 10}];
            dx = 1;
            dy = 0;
            score = 0;
            scoreElement.innerText = score;
            generateFood();
            startGame();
        }

        // ดักจับการกดปุ่มบนคีย์บอร์ด
        window.addEventListener("keydown", e => {
            switch(e.key) {
                case "ArrowUp":
                    if (dy !== 1) { dx = 0; dy = -1; } // ห้ามหักหลบกลับลำทันที
                    break;
                case "ArrowDown":
                    if (dy !== -1) { dx = 0; dy = 1; }
                    break;
                case "ArrowLeft":
                    if (dx !== 1) { dx = -1; dy = 0; }
                    break;
                case "ArrowRight":
                    if (dx !== -1) { dx = 1; dy = 0; }
                    break;
            }
        });

        // เริ่มเกมครั้งแรก
        startGame();
    </script>
</body>
</html>