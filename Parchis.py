import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Dino Cowboy 2D - Estilo Ilustrado",
    page_icon="🤠",
    layout="centered"
)

st.title("🤠 Dino Cowboy 360° (Diseño Realista) 🔫")
st.caption("Muévete con A/D, salta con ESPACIO/W, apunta con el ratón y dispara a los pterodáctilos.")

game_html = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            background-color: #f7f7f7;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            user-select: none;
        }
        .game-container {
            position: relative;
            background: #fff;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
            border: 2px solid #e0e0e0;
            margin-top: 10px;
            cursor: crosshair;
        }
        canvas {
            display: block;
            background-color: #fafafa;
        }
        .controls-hint {
            margin-top: 15px;
            display: flex;
            gap: 15px;
            font-size: 13px;
            color: #666;
            flex-wrap: wrap;
            justify-content: center;
        }
        .key {
            background: #eee;
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 2px 8px;
            font-weight: bold;
            color: #333;
        }
    </style>
</head>
<body>

    <div class="game-container">
        <canvas id="gameCanvas" width="750" height="420"></canvas>
    </div>

    <div class="controls-hint">
        <div><span class="key">A / D</span> Moverse</div>
        <div><span class="key">W</span> / <span class="key">ESPACIO</span> Saltar</div>
        <div><span class="key">RATÓN</span> Apuntar</div>
        <div><span class="key">CLIC</span> Disparar 🔫</div>
    </div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let score = 0;
let highScore = 0;
let gameOver = false;
let frameCount = 0;

const groundY = canvas.height - 48;

const dino = {
    x: canvas.width / 2,
    y: groundY - 25,
    vx: 0,
    vy: 0,
    speed: 5.5,
    gravity: 0.65,
    jumpForce: -12.5,
    grounded: false,
    aimAngle: 0
};

const keys = {};
let mouseX = 0;
let mouseY = 0;
let bullets = [];
let pteros = [];
let particles = [];
let spawnTimer = 0;

window.addEventListener('keydown', e => {
    keys[e.code] = true;
    if (gameOver && (e.code === 'Space' || e.code === 'KeyW')) {
        resetGame();
    }
});

window.addEventListener('keyup', e => {
    keys[e.code] = false;
});

canvas.addEventListener('mousemove', e => {
    const rect = canvas.getBoundingClientRect();
    mouseX = e.clientX - rect.left;
    mouseY = e.clientY - rect.top;
});

canvas.addEventListener('click', e => {
    if (gameOver) {
        resetGame();
        return;
    }
    shoot();
});

function shoot() {
    const speed = 16;
    const originX = dino.x;
    const originY = dino.y - 18;

    bullets.push({
        x: originX + Math.cos(dino.aimAngle) * 35,
        y: originY + Math.sin(dino.aimAngle) * 35,
        vx: Math.cos(dino.aimAngle) * speed,
        vy: Math.sin(dino.aimAngle) * speed,
        radius: 4,
        active: true
    });
}

function updateDino() {
    dino.vx = 0;
    if (keys['KeyA'] || keys['ArrowLeft']) dino.vx = -dino.speed;
    if (keys['KeyD'] || keys['ArrowRight']) dino.vx = dino.speed;

    dino.x += dino.vx;

    if (dino.x < 30) dino.x = 30;
    if (dino.x > canvas.width - 30) dino.x = canvas.width - 30;

    if ((keys['Space'] || keys['KeyW'] || keys['ArrowUp']) && dino.grounded) {
        dino.vy = dino.jumpForce;
        dino.grounded = false;
    }

    dino.vy += dino.gravity;
    dino.y += dino.vy;

    if (dino.y >= groundY - 20) {
        dino.y = groundY - 20;
        dino.vy = 0;
        dino.grounded = true;
    }

    const originX = dino.x;
    const originY = dino.y - 18;
    dino.aimAngle = Math.atan2(mouseY - originY, mouseX - originX);
}

function spawnPtero() {
    spawnTimer++;
    const spawnRate = Math.max(20, 55 - Math.floor(score / 5));

    if (spawnTimer > spawnRate) {
        let x, y;
        const side = Math.floor(Math.random() * 3);

        if (side === 0) {
            x = -40;
            y = Math.random() * (canvas.height - 150);
        } else if (side === 1) {
            x = canvas.width + 40;
            y = Math.random() * (canvas.height - 150);
        } else {
            x = Math.random() * canvas.width;
            y = -40;
        }

        const angle = Math.atan2((dino.y - 18) - y, dino.x - x);
        const speed = 1.8 + Math.random() * 1.5 + (score * 0.02);

        pteros.push({
            x: x,
            y: y,
            vx: Math.cos(angle) * speed,
            vy: Math.sin(angle) * speed,
            angle: angle,
            radius: 20,
            active: true
        });

        spawnTimer = 0;
    }
}

// DIBUJO REALISTA DEL DINOSAURIO COWBOY CON CURVAS
function drawDinoRealistic() {
    ctx.save();
    ctx.translate(dino.x, dino.y);

    const facingRight = mouseX >= dino.x;
    const dir = facingRight ? 1 : -1;

    // --- COLA ANATÓMICA ---
    ctx.fillStyle = '#4a5568';
    ctx.beginPath();
    ctx.moveTo(-5 * dir, -5);
    ctx.quadraticCurveTo(-25 * dir, -10, -32 * dir, 5);
    ctx.quadraticCurveTo(-22 * dir, 8, 0 * dir, 12);
    ctx.closePath();
    ctx.fill();

    // --- PIERNAS Y PATAS ---
    ctx.fillStyle = '#374151';
    const legSwing = (dino.grounded && Math.abs(dino.vx) > 0) ? Math.sin(frameCount * 0.3) * 10 : 0;

    // Pierna trasera
    ctx.beginPath();
    ctx.ellipse(-8 * dir + legSwing, 15, 6, 12, 0.2 * dir, 0, Math.PI * 2);
    ctx.fill();

    // Pierna delantera
    ctx.fillStyle = '#4a5568';
    ctx.beginPath();
    ctx.ellipse(6 * dir - legSwing, 15, 7, 13, -0.2 * dir, 0, Math.PI * 2);
    ctx.fill();

    // Garras
    ctx.fillStyle = '#1a202c';
    ctx.fillRect((4 - legSwing) * dir, 24, 6 * dir, 3);
    ctx.fillRect((-10 + legSwing) * dir, 24, 6 * dir, 3);

    // --- CUERPO PRINCIPAL ---
    ctx.fillStyle = '#535353';
    ctx.beginPath();
    ctx.ellipse(0, 0, 16, 22, (dir * 0.2), 0, Math.PI * 2);
    ctx.fill();

    // Pecho claro
    ctx.fillStyle = '#718096';
    ctx.beginPath();
    ctx.ellipse(6 * dir, 2, 8, 14, (dir * 0.2), 0, Math.PI * 2);
    ctx.fill();

    // --- CABEZA DE T-REX ---
    ctx.fillStyle = '#4a5568';
    ctx.beginPath();
    ctx.moveTo(2 * dir, -18);
    ctx.quadraticCurveTo(8 * dir, -35, 24 * dir, -30); // Hocico superior
    ctx.quadraticCurveTo(28 * dir, -20, 22 * dir, -15); // Mandíbula
    ctx.quadraticCurveTo(10 * dir, -12, 2 * dir, -15);
    ctx.closePath();
    ctx.fill();

    // Dientes
    ctx.fillStyle = '#ffffff';
    for (let i = 0; i < 3; i++) {
        ctx.beginPath();
        ctx.moveTo((14 + i * 3) * dir, -17);
        ctx.lineTo((15 + i * 3) * dir, -13);
        ctx.lineTo((16 + i * 3) * dir, -17);
        ctx.fill();
    }

    // Ojo y ceja furiosa
    ctx.fillStyle = '#f6ad55';
    ctx.beginPath();
    ctx.arc(12 * dir, -26, 3.5, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#1a202c';
    ctx.beginPath();
    ctx.arc(12.5 * dir, -26, 1.8, 0, Math.PI * 2);
    ctx.fill();

    ctx.strokeStyle = '#2d3748';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(8 * dir, -29);
    ctx.lineTo(16 * dir, -27);
    ctx.stroke();

    // Brazo pequeño de T-Rex
    ctx.fillStyle = '#374151';
    ctx.beginPath();
    ctx.ellipse(10 * dir, -5, 3, 7, Math.PI / 4 * dir, 0, Math.PI * 2);
    ctx.fill();

    // --- SOMBRERO DE VAQUERO DETALLADO 🤠 ---
    const hatX = 10 * dir;
    const hatY = -31;

    // Ala doblada del sombrero
    ctx.fillStyle = '#7c2d12';
    ctx.beginPath();
    ctx.ellipse(hatX, hatY, 22, 6, -0.1 * dir, 0, Math.PI * 2);
    ctx.fill();

    ctx.strokeStyle = '#451a03';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Copa del sombrero con hendidura
    ctx.fillStyle = '#9a3412';
    ctx.beginPath();
    ctx.moveTo(hatX - 11, hatY - 3);
    ctx.quadraticCurveTo(hatX - 10, hatY - 20, hatX - 4, hatY - 18);
    ctx.quadraticCurveTo(hatX, hatY - 16, hatX + 4, hatY - 18);
    ctx.quadraticCurveTo(hatX + 10, hatY - 20, hatX + 11, hatY - 3);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    // Cinta roja del sombrero
    ctx.fillStyle = '#dc2626';
    ctx.beginPath();
    ctx.ellipse(hatX, hatY - 3, 11, 3, -0.1 * dir, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();

    // --- ESCAPARATE / ARMA 360° ---
    ctx.save();
    ctx.translate(dino.x, dino.y - 18);
    ctx.rotate(dino.aimAngle);

    // Cuerpo de la escopeta
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, -3, 30, 6);
    // Cañón doble
    ctx.fillStyle = '#475569';
    ctx.fillRect(15, -4, 16, 3);
    ctx.fillRect(15, 1, 16, 3);
    // Culata de madera
    ctx.fillStyle = '#7c2d12';
    ctx.fillRect(-8, -2, 10, 6);

    ctx.restore();
}

// DIBUJO REALISTA DEL PTERODÁCTILO CON ALAS CURVAS
function drawPteroRealistic(p) {
    ctx.save();
    ctx.translate(p.x, p.y);
    ctx.rotate(p.angle);

    ctx.fillStyle = '#2d3748';

    // Pico largo y afilado
    ctx.beginPath();
    ctx.moveTo(10, -2);
    ctx.lineTo(30, 0);
    ctx.lineTo(10, 3);
    ctx.closePath();
    ctx.fill();

    // Cabeza y Cresta Posterior
    ctx.beginPath();
    ctx.moveTo(10, -4);
    ctx.lineTo(-18, -12); // Cresta
    ctx.lineTo(-5, 4);
    ctx.closePath();
    ctx.fill();

    // Ojo brillante
    ctx.fillStyle = '#e53e3e';
    ctx.beginPath();
    ctx.arc(6, -2, 2, 0, Math.PI * 2);
    ctx.fill();

    // Cuerpo aerodinámico
    ctx.fillStyle = '#3a4a5e';
    ctx.beginPath();
    ctx.ellipse(-4, 2, 14, 5, 0, 0, Math.PI * 2);
    ctx.fill();

    // Alas de membrana animadas
    const wingFlap = Math.sin(frameCount * 0.25) * 18;
    ctx.fillStyle = '#1a202c';

    // Ala Superior
    ctx.beginPath();
    ctx.moveTo(-2, -2);
    ctx.quadraticCurveTo(-8, -25 + wingFlap, 12, -35 + wingFlap);
    ctx.quadraticCurveTo(0, -15, -12, 0);
    ctx.closePath();
    ctx.fill();

    // Ala Inferior
    ctx.beginPath();
    ctx.moveTo(-2, 2);
    ctx.quadraticCurveTo(-8, 25 - wingFlap, 12, 35 - wingFlap);
    ctx.quadraticCurveTo(0, 15, -12, 0);
    ctx.closePath();
    ctx.fill();

    ctx.restore();
}

function createExplosion(x, y) {
    for (let i = 0; i < 12; i++) {
        const angle = Math.random() * Math.PI * 2;
        const speed = Math.random() * 6;
        particles.push({
            x: x, y: y,
            vx: Math.cos(angle) * speed,
            vy: Math.sin(angle) * speed,
            life: 22
        });
    }
}

function updateExplosions() {
    particles.forEach((p, index) => {
        p.x += p.vx;
        p.y += p.vy;
        p.life--;
        ctx.fillStyle = (p.life % 2 === 0) ? '#e53e3e' : '#dd6b20';
        ctx.beginPath();
        ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
        ctx.fill();
        if (p.life <= 0) particles.splice(index, 1);
    });
}

function checkCollisions() {
    bullets.forEach(b => {
        pteros.forEach(p => {
            if (b.active && p.active) {
                const dist = Math.hypot(b.x - p.x, b.y - p.y);
                if (dist < b.radius + p.radius) {
                    b.active = false;
                    p.active = false;
                    score += 10;
                    createExplosion(p.x, p.y);
                }
            }
        });
    });

    pteros.forEach(p => {
        if (p.active) {
            const dist = Math.hypot(dino.x - p.x, (dino.y - 18) - p.y);
            if (dist < 24 + p.radius) {
                gameOver = true;
            }
        }
    });
}

function resetGame() {
    score = 0;
    gameOver = false;
    bullets = [];
    pteros = [];
    particles = [];
    dino.x = canvas.width / 2;
    dino.y = groundY - 20;
    dino.vy = 0;
    spawnTimer = 0;
    loop();
}

function drawEnvironment() {
    // Suelo con sombras
    ctx.strokeStyle = '#4a5568';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(0, groundY);
    ctx.lineTo(canvas.width, groundY);
    ctx.stroke();

    ctx.fillStyle = '#cbd5e0';
    for (let i = 15; i < canvas.width; i += 60) {
        ctx.beginPath();
        ctx.ellipse(i, groundY + 12, 10, 2, 0, 0, Math.PI * 2);
        ctx.fill();
    }
}

function drawScore() {
    ctx.fillStyle = '#2d3748';
    ctx.font = 'bold 16px monospace';
    ctx.textAlign = 'right';
    ctx.fillText(`HI ${Math.floor(highScore).toString().padStart(5, '0')}  PUNTOS ${Math.floor(score).toString().padStart(5, '0')}`, canvas.width - 20, 30);
}

function loop() {
    if (gameOver) {
        if (score > highScore) highScore = score;
        ctx.fillStyle = 'rgba(15, 23, 42, 0.75)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#fff';
        ctx.font = 'bold 28px monospace';
        ctx.textAlign = 'center';
        ctx.fillText('¡GAME OVER!', canvas.width / 2, canvas.height / 2 - 10);
        ctx.font = '14px monospace';
        ctx.fillText('Presiona ESPACIO o haz clic para reiniciar', canvas.width / 2, canvas.height / 2 + 25);
        return;
    }

    frameCount++;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    updateDino();
    drawEnvironment();
    drawDinoRealistic();
    spawnPtero();

    bullets.forEach((b, index) => {
        b.x += b.vx;
        b.y += b.vy;
        ctx.fillStyle = '#f59e0b';
        ctx.beginPath();
        ctx.arc(b.x, b.y, b.radius, 0, Math.PI * 2);
        ctx.fill();

        if (b.x < 0 || b.x > canvas.width || b.y < 0 || b.y > canvas.height) {
            b.active = false;
        }
        if (!b.active) bullets.splice(index, 1);
    });

    pteros.forEach((p, index) => {
        p.x += p.vx;
        p.y += p.vy;
        drawPteroRealistic(p);

        if (!p.active) pteros.splice(index, 1);
    });

    updateExplosions();
    checkCollisions();
    drawScore();

    requestAnimationFrame(loop);
}

loop();
</script>
</body>
</html>
"""

components.html(game_html, height=500)