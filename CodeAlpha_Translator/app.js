// js/app.js — LinguaFlow main controller

(function () {
  // ── DOM refs ────────────────────────────────────────────
  const sourceLangEl   = document.getElementById('sourceLang');
  const targetLangEl   = document.getElementById('targetLang');
  const sourceTextEl   = document.getElementById('sourceText');
  const translatedEl   = document.getElementById('translatedText');
  const charCountEl    = document.getElementById('charCount');
  const detectedEl     = document.getElementById('detectedLang');
  const loadingBar     = document.getElementById('loadingBar');
  const translateBtn   = document.getElementById('translateBtn');
  const swapBtn        = document.getElementById('swapBtn');
  const clearBtn       = document.getElementById('clearBtn');
  const pasteBtn       = document.getElementById('pasteBtn');
  const copyBtn        = document.getElementById('copyBtn');
  const downloadBtn    = document.getElementById('downloadBtn');
  const speakSrcBtn    = document.getElementById('speakSource');
  const speakTgtBtn    = document.getElementById('speakTarget');
  const themeToggle    = document.getElementById('themeToggle');
  const historyToggle  = document.getElementById('historyToggle');
  const historyPanel   = document.getElementById('historyPanel');
  const historyOverlay = document.getElementById('historyOverlay');
  const historyList    = document.getElementById('historyList');
  const historyEmpty   = document.getElementById('historyEmpty');
  const clearHistBtn   = document.getElementById('clearHistory');
  const modeChips      = document.querySelectorAll('.chip[data-mode]');
  const autoDetectBtn  = document.getElementById('autoDetectChip');
  const romanizeBtn    = document.getElementById('romanizeChip');
  const quickBtns      = document.querySelectorAll('.quick-btn');
  const toastEl        = document.getElementById('toast');

  let currentTranslation = '';
  let autoTimer = null;

  // ── Init ────────────────────────────────────────────────
  populateSelect(sourceLangEl, true, 'en');
  populateSelect(targetLangEl, false, 'fr');

  // Restore theme
  const savedTheme = localStorage.getItem('lf_theme');
  if (savedTheme === 'light') document.body.setAttribute('data-theme', 'light');

  // Initial history render
  refreshHistory();

  // ── Translate ───────────────────────────────────────────
  async function doTranslate() {
    const text = sourceTextEl.value.trim();
    if (!text) { showToast('Please enter some text', 'error'); return; }

    setLoading(true);
    detectedEl.textContent = '';

    try {
      const result = await translateText(
        text,
        sourceLangEl.value,
        targetLangEl.value,
        getCurrentMode()
      );

      if (!result) return;

      currentTranslation = result.translated;
      showTranslation(result.translated);

      if (result.detected) {
        const name = getLangName(result.detected.split('-')[0]);
        if (name) detectedEl.textContent = `Detected: ${name}`;
      }

      // Save & refresh history
      saveToHistory({
        source: text,
        target: result.translated,
        sourceLang: sourceLangEl.value,
        targetLang: targetLangEl.value,
      });
      refreshHistory();

    } catch (err) {
      showToast('Translation failed. ' + (err.message || ''), 'error');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  function setLoading(on) {
    translateBtn.classList.toggle('loading', on);
    if (on) {
      loadingBar.classList.add('active');
    } else {
      loadingBar.classList.remove('active');
      loadingBar.style.width = '';
    }
  }

  function showTranslation(text) {
    translatedEl.textContent = '';
    translatedEl.style.animation = 'none';
    requestAnimationFrame(() => {
      translatedEl.style.animation = 'fadeIn 0.3s ease';
      translatedEl.textContent = text;
    });
  }

  function refreshHistory() {
    renderHistory(historyList, historyEmpty, (entry) => {
      sourceTextEl.value = entry.source;
      populateSelect(sourceLangEl, true, entry.sourceLang);
      populateSelect(targetLangEl, false, entry.targetLang);
      showTranslation(entry.target);
      currentTranslation = entry.target;
      updateCharCount();
      closeHistory();
    });
  }

  // ── Char count ──────────────────────────────────────────
  function updateCharCount() {
    const len = sourceTextEl.value.length;
    charCountEl.textContent = `${len} / 5000`;
    charCountEl.classList.toggle('warn', len > 4500);
  }

  // ── Event listeners ─────────────────────────────────────

  // Translate button
  translateBtn.addEventListener('click', doTranslate);

  // Ctrl/Cmd+Enter shortcut
  sourceTextEl.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      doTranslate();
    }
  });

  // Auto-translate after pause
  sourceTextEl.addEventListener('input', () => {
    updateCharCount();
    clearTimeout(autoTimer);
    autoTimer = setTimeout(() => {
      if (sourceTextEl.value.trim().length > 3) doTranslate();
    }, 900);
  });

  // Swap
  swapBtn.addEventListener('click', () => {
    const srcVal = sourceLangEl.value;
    const tgtVal = targetLangEl.value;
    if (srcVal === 'auto') {
      showToast('Cannot swap Auto-Detect. Choose a source language first.', 'error');
      return;
    }
    populateSelect(sourceLangEl, true, tgtVal);
    populateSelect(targetLangEl, false, srcVal);

    const prevSrc = sourceTextEl.value;
    sourceTextEl.value = currentTranslation;
    currentTranslation = prevSrc;
    showTranslation(prevSrc);
    updateCharCount();
  });

  // Clear
  clearBtn.addEventListener('click', () => {
    sourceTextEl.value = '';
    currentTranslation = '';
    translatedEl.innerHTML = '<span class="placeholder">Translation will appear here…</span>';
    detectedEl.textContent = '';
    updateCharCount();
    sourceTextEl.focus();
  });

  // Paste
  pasteBtn.addEventListener('click', async () => {
    try {
      const text = await navigator.clipboard.readText();
      sourceTextEl.value = text;
      updateCharCount();
      doTranslate();
    } catch {
      showToast('Clipboard access denied', 'error');
    }
  });

  // Copy
  copyBtn.addEventListener('click', async () => {
    if (!currentTranslation) { showToast('Nothing to copy yet', 'error'); return; }
    const ok = await copyToClipboard(currentTranslation);
    if (ok) showToast('Copied ✓', 'ok');
  });

  // Download
  downloadBtn.addEventListener('click', () => {
    if (!currentTranslation) { showToast('Nothing to save yet', 'error'); return; }
    const src  = sourceTextEl.value;
    const tgt  = getLangName(targetLangEl.value);
    const blob = `ORIGINAL:\n${src}\n\nTRANSLATION (${tgt}):\n${currentTranslation}`;
    downloadText(blob, `translation_${targetLangEl.value}.txt`);
    showToast('File saved ↓', 'ok');
  });

  // TTS
  speakSrcBtn.addEventListener('click', () => {
    const t = sourceTextEl.value.trim();
    if (!t) return;
    speak(t, sourceLangEl.value);
    showToast('Playing…');
  });
  speakTgtBtn.addEventListener('click', () => {
    if (!currentTranslation) return;
    speak(currentTranslation, targetLangEl.value);
    showToast('Playing…');
  });

  // Theme
  themeToggle.addEventListener('click', () => {
    const isLight = document.body.getAttribute('data-theme') === 'light';
    if (isLight) {
      document.body.removeAttribute('data-theme');
      localStorage.setItem('lf_theme', 'dark');
    } else {
      document.body.setAttribute('data-theme', 'light');
      localStorage.setItem('lf_theme', 'light');
    }
  });

  // History open / close
  function openHistory()  { historyPanel.classList.add('open'); historyOverlay.classList.add('show'); }
  function closeHistory() { historyPanel.classList.remove('open'); historyOverlay.classList.remove('show'); }
  historyToggle.addEventListener('click', () => historyPanel.classList.contains('open') ? closeHistory() : openHistory());
  historyOverlay.addEventListener('click', closeHistory);

  // Clear history
  clearHistBtn.addEventListener('click', () => {
    clearHistory();
    refreshHistory();
    showToast('History cleared');
  });

  // Mode chips
  modeChips.forEach(chip => {
    chip.addEventListener('click', () => {
      modeChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      setCurrentMode(chip.dataset.mode);
      if (sourceTextEl.value.trim()) doTranslate();
    });
  });

  // Auto-Detect
  autoDetectBtn.addEventListener('click', () => {
    populateSelect(sourceLangEl, true, 'auto');
    showToast('Auto-detect enabled');
    if (sourceTextEl.value.trim()) doTranslate();
  });

  // Romanize
  romanizeBtn.addEventListener('click', async () => {
    const text = sourceTextEl.value.trim();
    if (!text) { showToast('Enter text to romanize', 'error'); return; }
    setLoading(true);
    try {
      const result = await romanizeText(text, sourceLangEl.value);
      showTranslation(result);
      currentTranslation = result;
      showToast('Romanized!', 'ok');
    } catch {
      showToast('Romanization failed', 'error');
    } finally {
      setLoading(false);
    }
  });

  // Quick-language buttons
  quickBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      populateSelect(targetLangEl, false, btn.dataset.lang);
      showToast(`Target → ${getLangName(btn.dataset.lang)}`);
      if (sourceTextEl.value.trim()) doTranslate();
    });
  });

  // ── Toast ────────────────────────────────────────────────
  let toastTimer;
  function showToast(msg, type = '') {
    clearTimeout(toastTimer);
    toastEl.textContent = msg;
    toastEl.className = `toast ${type} show`;
    toastTimer = setTimeout(() => toastEl.classList.remove('show'), 2600);
  }

  // Inject fadeIn keyframe
  const s = document.createElement('style');
  s.textContent = `@keyframes fadeIn { from{opacity:0;transform:translateY(5px)} to{opacity:1;transform:translateY(0)} }`;
  document.head.appendChild(s);

})();
