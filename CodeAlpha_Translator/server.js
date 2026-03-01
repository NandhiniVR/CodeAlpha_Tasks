// server.js — LinguaFlow proxy using @vitalets/google-translate-api

const express = require('express');
const path = require('path');
const app = express();

app.use(express.json({ limit: '1mb' }));

const staticDir = path.resolve(__dirname);
app.use(express.static(staticDir));

// Pre-load the ESM module once at startup
let translateFn = null;
(async () => {
  try {
    const pkg = await import('@vitalets/google-translate-api');
    // Log all exported keys so we can see exactly what's available
    console.log('Package exports:', Object.keys(pkg));

    // Try every possible export shape
    translateFn =
      pkg.translate ||
      pkg.default?.translate ||
      (typeof pkg.default === 'function' ? pkg.default : null);

    if (typeof translateFn !== 'function') {
      console.error('Could not find translate function. Exports were:', Object.keys(pkg));
    } else {
      console.log('translate function loaded successfully');
    }
  } catch (e) {
    console.error('Failed to load @vitalets/google-translate-api:', e.message);
  }
})();

app.get('/health', (req, res) => res.json({ ok: true }));

app.post('/api/translate', async (req, res) => {
  const { text, from = 'auto', to = 'en' } = req.body;
  if (!text?.trim()) return res.status(400).json({ error: 'No text provided' });
  if (!translateFn)   return res.status(500).json({ error: 'Translate module not ready' });

  try {
    const result = await translateFn(text, { from, to });
    res.json({ translated: result.text, detected: result.raw?.src || null });
  } catch (err) {
    console.error('Translation error:', err.message);
    if (err.name === 'TooManyRequestsError')
      return res.status(429).json({ error: 'Too many requests. Please wait a moment.' });
    res.status(500).json({ error: err.message || 'Translation failed' });
  }
});

app.post('/api/romanize', async (req, res) => {
  const { text, from = 'auto' } = req.body;
  if (!text?.trim()) return res.status(400).json({ error: 'No text provided' });
  if (!translateFn)   return res.status(500).json({ error: 'Translate module not ready' });

  try {
    const result = await translateFn(text, { from, to: 'en' });
    const romanized =
      result.raw?.pronunciation ||
      result.raw?.dict?.[0]?.terms?.[0] ||
      result.text;
    res.json({ romanized });
  } catch (err) {
    console.error('Romanize error:', err.message);
    res.status(500).json({ error: err.message || 'Romanization failed' });
  }
});

app.get('*', (req, res) => {
  res.sendFile(path.join(staticDir, 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () =>
  console.log(`LinguaFlow running → http://localhost:${PORT}`)
);
