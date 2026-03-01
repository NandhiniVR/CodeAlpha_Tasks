// js/history.js
// Manages translation history in localStorage

const HISTORY_KEY = "linguaflow_history";
const MAX_HISTORY = 50;

function getHistory() {
  try {
    return JSON.parse(localStorage.getItem(HISTORY_KEY)) || [];
  } catch {
    return [];
  }
}

function saveToHistory(entry) {
  // entry: { source, target, sourceLang, targetLang, timestamp }
  const history = getHistory();
  history.unshift({
    ...entry,
    id: Date.now(),
    timestamp: new Date().toISOString(),
  });
  // Cap history size
  if (history.length > MAX_HISTORY) history.splice(MAX_HISTORY);
  localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
}

function clearHistory() {
  localStorage.removeItem(HISTORY_KEY);
}

function renderHistory(listEl, emptyEl, onSelect) {
  const history = getHistory();
  listEl.innerHTML = "";

  if (history.length === 0) {
    emptyEl.style.display = "block";
    return;
  }
  emptyEl.style.display = "none";

  history.forEach(entry => {
    const li = document.createElement("li");
    li.className = "history-item";
    li.innerHTML = `
      <div class="hi-langs">${getLangName(entry.sourceLang)} → ${getLangName(entry.targetLang)}</div>
      <div class="hi-text">${escapeHTML(entry.source.substring(0, 80))}${entry.source.length > 80 ? "…" : ""}</div>
      <div class="hi-result">${escapeHTML(entry.target.substring(0, 80))}${entry.target.length > 80 ? "…" : ""}</div>
    `;
    li.addEventListener("click", () => onSelect(entry));
    listEl.appendChild(li);
  });
}

function escapeHTML(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
