const form = document.getElementById('shortenForm');
const urlInput = document.getElementById('urlInput');
const customName = document.getElementById('customName');
const shortenBtn = document.getElementById('shortenBtn');
const btnText = shortenBtn.querySelector('.btn-text');
const btnLoader = shortenBtn.querySelector('.btn-loader');
const resultContainer = document.getElementById('resultContainer');
const shortUrlInput = document.getElementById('shortUrl');
const qrCode = document.getElementById('qrCode');
const copyBtn = document.getElementById('copyBtn');
const newBtn = document.getElementById('newBtn');
const toast = document.getElementById('toast');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const longUrl = urlInput.value.trim();
  const custom = customName.value.trim().replace(/\s+/g, "-");

  if (!longUrl) return showToast("Por favor, insira uma URL válida!");

  // Loading
  btnText.style.display = "none";
  btnLoader.style.display = "inline-block";
  shortenBtn.disabled = true;

  try {
    const response = await fetch(`https://tinyurl.com/api-create.php?url=${encodeURIComponent(longUrl)}`);
    const shortUrl = await response.text();

    // Simula link personalizado
    const finalUrl = custom ? `${shortUrl}-${custom}` : shortUrl;

    shortUrlInput.value = finalUrl;
    qrCode.src = `https://api.qrserver.com/v1/create-qr-code/?data=${encodeURIComponent(finalUrl)}&size=150x150`;

    form.style.display = 'none';
    resultContainer.classList.add('show');
    showToast("✅ URL encurtada com sucesso!");
  } catch {
    showToast("❌ Erro ao encurtar a URL!");
  } finally {
    btnText.style.display = "inline-block";
    btnLoader.style.display = "none";
    shortenBtn.disabled = false;
  }
});

copyBtn.addEventListener('click', () => {
  navigator.clipboard.writeText(shortUrlInput.value);
  showToast("🔗 Copiado para a área de transferência!");
});

newBtn.addEventListener('click', () => {
  urlInput.value = "";
  customName.value = "";
  resultContainer.classList.remove('show');
  form.style.display = 'flex';
});

function showToast(msg) {
  toast.textContent = msg;
  toast.style.display = 'block';
  setTimeout(() => toast.style.display = 'none', 3000);
}
