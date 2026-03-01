// js/speech.js
// Text-to-Speech and clipboard utilities

const SpeechSynth = window.speechSynthesis;

let voices = [];

// Load voices (they load async in some browsers)
function loadVoices() {
  voices = SpeechSynth.getVoices();
}
if (SpeechSynth) {
  SpeechSynth.onvoiceschanged = loadVoices;
  loadVoices();
}

function speak(text, langCode) {
  if (!SpeechSynth || !text.trim()) return;
  SpeechSynth.cancel(); // Stop any current speech

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = langCode === "auto" ? "en" : langCode;
  utterance.rate = 0.95;
  utterance.pitch = 1;

  // Try to find a matching voice
  const match = voices.find(v => v.lang.startsWith(langCode.substring(0, 2)));
  if (match) utterance.voice = match;

  SpeechSynth.speak(utterance);
}

function stopSpeech() {
  if (SpeechSynth) SpeechSynth.cancel();
}

async function copyToClipboard(text) {
  if (!text) return false;
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    // Fallback
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
    return true;
  }
}

function downloadText(text, filename = "translation.txt") {
  const blob = new Blob([text], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
