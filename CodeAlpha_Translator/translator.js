// translator.js — LinguaFlow
// Calls the local Node.js proxy which uses @vitalets/google-translate-api.
// No API key required!

const TONE_PREFIX = {
  standard: '',
  formal:   '',   // tone handled server-side if desired; Google Translate is neutral
  casual:   '',
};

let currentMode = 'standard';

async function translateText(text, sourceLang, targetLang /*, mode unused for Google */) {
  if (!text.trim()) return null;

  const from = sourceLang === 'auto' ? 'auto' : sourceLang;
  const to   = targetLang;

  const response = await fetch('/api/translate', {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ text, from, to }),
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.error || `Server error ${response.status}`);
  }

  const data = await response.json();

  return {
    translated: data.translated,
    detected:   data.detected || null,
    matches:    [],
  };
}

async function romanizeText(text, sourceLang) {
  const from = sourceLang === 'auto' ? 'auto' : sourceLang;

  const response = await fetch('/api/romanize', {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ text, from }),
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.error || `Server error ${response.status}`);
  }

  const data = await response.json();
  return data.romanized;
}

function setCurrentMode(mode) { currentMode = mode; }
function getCurrentMode()     { return currentMode; }
