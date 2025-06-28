// Responsive Matrix Background
const canvas = document.getElementById('matrix');
const ctx = canvas.getContext('2d');

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}

resizeCanvas();
window.addEventListener('resize', resizeCanvas);

const letters = 'アァイィウエエオカガキギクグケゲコゴサザシジスズセゼソゾタダチッヂヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモヤユヨラリルレロワヲン'.split('');
const fontSize = 14;
let columns = canvas.width / fontSize;
const drops = Array(Math.floor(columns)).fill(1);

function drawMatrix() {
  ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = '#00ffaa';
  ctx.font = fontSize + 'px monospace';

  for (let i = 0; i < drops.length; i++) {
    const text = letters[Math.floor(Math.random() * letters.length)];
    ctx.fillText(text, i * fontSize, drops[i] * fontSize);
    if (drops[i] * fontSize > canvas.height || Math.random() > 0.975) {
      drops[i] = 0;
    }
    drops[i]++;
  }
}

setInterval(drawMatrix, 35);

// Phishing Check
function checkURL() {
  const url = document.getElementById("urlInput").value.trim();
  const resultBox = document.getElementById("resultBox");
  resultBox.innerHTML = "Checking...";

  fetch("http://localhost:8000/check_url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: url }),
  })
  .then(res => res.json())
  .then(data => {
    if (data.is_phishing) {
      resultBox.innerHTML = '⚠️ <span class="warning">Warning! This is a phishing link.</span>';
    } else {
      resultBox.innerHTML = '✅ <span class="safe">This URL seems safe.</span>';
    }
  })
  .catch(() => {
    resultBox.innerHTML = '❌ <span class="warning">Server is unreachable. Try again later.</span>';
  });
}
