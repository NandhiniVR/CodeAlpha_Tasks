# LinguaFlow — Free Google Translate powered app

No API key needed! This app uses [@vitalets/google-translate-api](https://github.com/vitalets/google-translate-api) — a free, unlimited Google Translate wrapper for Node.js.

## Quick Start

```bash
npm install
node server.js
```

Then open **http://localhost:3000** in your browser. That's it — no keys, no accounts, no cost.

## How it works

- The frontend (`index.html`, `app.js`, etc.) is served statically by the Express server.
- When you click Translate, the browser calls `/api/translate` on the local server.
- The server uses `@vitalets/google-translate-api` to query Google Translate for free.
- Results are returned to the browser and displayed instantly.

## Endpoints

| Method | Path            | Body                          | Description            |
|--------|-----------------|-------------------------------|------------------------|
| POST   | `/api/translate`| `{ text, from, to }`          | Translate text         |
| POST   | `/api/romanize` | `{ text, from }`              | Romanize/transliterate |
| GET    | `/health`       | —                             | Health check           |

## Notes

- `from: "auto"` lets Google auto-detect the source language.
- Rate limiting: Google may throttle if you send too many requests very quickly. The app handles `TooManyRequestsError` gracefully with a user-friendly message.
- For production use, consider adding your own rate limiting middleware.
- 100+ languages supported — see `languages.js` for the full list.

## Docker

```bash
docker build -t linguaflow .
docker run -p 3000:3000 linguaflow
```
